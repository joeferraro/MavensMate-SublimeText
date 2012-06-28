require 'rubygems'
require 'savon'
require 'httpi'
require 'fileutils'
require 'base64'
require 'yaml'
require 'json'
require SUPPORT + '/lib/factory'
require SUPPORT + '/lib/util'
require SUPPORT + '/lib/keychain'
require SUPPORT + '/lib/metadata_helper'

module MavensMate
  
  class Client 
    
    include MetadataHelper
    
    # sfdc username
    attr_accessor :username
    # sfdc password
    attr_accessor :password
    # partner endpoint
    attr_accessor :endpoint
    # partner client
    attr_accessor :pclient
    # metadata client
    attr_accessor :mclient
    # session id
    attr_accessor :sid
    # current user id
    attr_accessor :user_id
    # metadata api endpoint url
    attr_accessor :metadata_server_url
    
    is_retry = false
           
    def initialize(creds={})
      HTTPI.log = false
      Savon.configure do |config|
        config.log = false
      end      
      if creds[:sid].nil? && creds[:metadata_server_url].nil?        
        creds = (creds[:username].nil? || creds[:password].nil? || creds[:endpoint].nil?) ? get_creds : creds
        self.username = creds[:username]
        self.password = creds[:password]
        if ! creds[:endpoint].include? "Soap"
          creds[:endpoint] = (creds[:endpoint].include? "test") ? "https://test.salesforce.com/services/Soap/u/#{MM_API_VERSION}" : "https://www.salesforce.com/services/Soap/u/#{MM_API_VERSION}"
        end
        self.endpoint = creds[:endpoint] 
        self.pclient = get_partner_client
        login
      else
        self.sid = creds[:sid]
        self.metadata_server_url = creds[:metadata_server_url]
      end
    end
    
    #logs into SFDC, sets metadata server url & sessionid
    def login
      #puts "logging in with: "+self.password
      begin
        response = self.pclient.request :login do
          soap.body = { :username => self.username, :password => self.password }
        end
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s)
        # TODO: handle incorrect password gracefully
        # if fault.to_s.include? "INVALID_LOGIN"
        #   self.password = TextMate::UI.request_secure_string(
        #     :title => "MavensMate", 
        #     :prompt => 'Your login attempt failed. Please re-enter your password',
        #     :button2 => 'Cancel'
        #   )
        #   TextMate.exit_discard if self.password == nil
        #   is_retry = true
        #   login
        # else
        #   raise Exception.new(fault.to_s)
        # end 
      end
      
      # if is_retry == true
      #   MavensMate.add_to_keychain(MavensMate.get_project_name, self.password)
      # end 
      
      begin
        res = response.to_hash
        self.metadata_server_url = res[:login_response][:result][:metadata_server_url]
        self.sid = res[:login_response][:result][:session_id].to_s
        self.user_id = res[:login_response][:result][:user_id].to_s
        self.pclient.wsdl.endpoint = res[:login_response][:result][:server_url] 
      rescue Exception => e
        #puts e.message 
      end
    end
    
    #retrieves metadata in zip format. :path => retrieve specific file  
    def retrieve(options={})
      self.mclient = get_metadata_client
          
      begin
        response = mclient.request :retrieve do |soap|
          soap.header = get_soap_header
          soap.body = options[:body] || get_retrieve_body(options)                       
        end
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s)
      end
      
      retrieve_hash = response.to_hash
      retrieve_id = retrieve_hash[:retrieve_response][:result][:id]
      
      is_finished = false
      while is_finished == false
        sleep 2
        response = self.mclient.request :check_status do |soap|
          soap.header = get_soap_header  
          soap.body = { :id => retrieve_id  }
        end
        status_hash = response.to_hash
        is_finished = status_hash[:check_status_response][:result][:done]
      end
      
      begin
        retrieve_response = self.mclient.request :check_retrieve_status do |soap|
          soap.header = get_soap_header 
          soap.body = { :id => retrieve_id  }
        end
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s)
      end
      
      retrieve_request_hash = retrieve_response.body
      #puts "RETRIEVE: " + retrieve_request_hash.inspect
      zip_file = retrieve_request_hash[:check_retrieve_status_response][:result][:zip_file]
    end
    
    #deploy/delete base64 encoded metadata to salesforce    
    def deploy(options={})
      self.mclient = get_metadata_client      
      soapbody = "<zipFile>#{options[:zip_file]}</zipFile>"
      soapbody << "<DeployOptions>#{options[:deploy_options]}</DeployOptions>" unless options[:deploy_options].nil?
      begin
        response = self.mclient.request :deploy do |soap|
          soap.header = get_soap_header
          soap.body = soapbody
        end
        #puts "raw deploy response: " + response.inspect
        create_hash = response.to_hash
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s)
      end
            
      update_id = create_hash[:deploy_response][:result][:id]
      is_finished = false
      timer = 0
      is_timeout = false
      
      while ! is_finished
        sleep 1
        timer += 1
        response = self.mclient.request :check_status do |soap|
          soap.header = get_soap_header
          soap.body = { :id => update_id }
        end
        check_status_hash = response.to_hash
        is_finished = check_status_hash[:check_status_response][:result][:done]        

        if timer == ENV['FM_TIMEOUT'].to_i
          is_timeout = true
          break
        end
      end
      
      if is_timeout == true
        return { 
          :is_success => false,
          :message => "TIMEOUT"
        }
      end
            
      response = self.mclient.request :check_deploy_status do |soap|
        soap.header = get_soap_header
        soap.body = { :id => update_id  }
      end
      
      deploy_hash = response.to_hash
      #deploy_hash = response.to_xml
      #puts "deploy result is: " + deploy_hash.inspect
            
      return deploy_hash            
    end
    
    #describes an org's metadata
    def describe
      self.mclient = get_metadata_client
      begin
        response = self.mclient.request :describe_metadata do |soap|
          soap.header = get_soap_header  
          soap.body = "<apiVersion>#{MM_API_VERSION}</apiVersion>"
        end
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s)
      end
      #puts "<br/><br/> describe response: " + response.to_hash.inspect
      hash = response.to_hash
      folders = Array.new
      hash[:describe_metadata_response][:result][:metadata_objects].each { |object| 
        children = []
        if object[:child_xml_names] and object[:child_xml_names].kind_of? String
          children.push(object[:child_xml_names])
        else
          children = object[:child_xml_names]
        end
        folders.push({
          :title => object[:directory_name],
          :isLazy => true,
          :isFolder => true,
          :directory_name => object[:directory_name],
          :meta_type => object[:xml_name],
          :select => CORE_METADATA_TYPES.include?(object[:xml_name]) ? true : false,
          :child_metadata => children,
          :has_child_metadata => ! children.nil?,
          :in_folder => object[:in_folder]
        })
      }
      folders.sort! { |a,b| a[:title] <=> b[:title] }
      #puts "\n\n\n\n\n"
      #puts folders.to_json
      return folders.to_json
    end
    
    #queries ApexClass, ApexTrigger, ApexPage, ApexComponent, StaticResource to determine
    #whether server copy has been updated by a different user than the current
    def has_server_conflict(files)
      begin
        files.each do |key, value|
          next unless CORE_METADATA_TYPES.include?(key)
          response = nil
          filter = ""
          value.each_with_index do |v, i|
             filter << "Name = '#{v}'"  
             filter << " OR " unless i == value.length - 1
          end
          #puts filter
          begin
            response = self.pclient.request :query do |soap|
              soap.header = get_soap_header
              soap.body = { :queryString => "select count() from #{key} Where LastModifiedById != '#{self.user_id}' and (#{filter})" }
            end
          rescue Savon::SOAP::Fault => fault
            raise Exception.new(fault.to_s)
          end
        
          #puts "\n\nquery response: " + response.to_hash.inspect
          if response[:query_response][:result][:size] == "0"
            return false
          else
            return true
          end
          #query response: {:query_response=>{:result=>{:done=>true, :query_locator=>nil, :size=>"1", :"@xsi:type"=>"QueryResult"}}}          
        end
      rescue Exception => e
        #puts "exception: " + e.message
        return false
      end
    end
    
    #list metadata for a specific type
    def list(type="",raw=false,format="json")
      
      metadata_type = MavensMate::FileFactory.get_meta_type_by_name(type) || {}
      has_children_metadata = false
      if ! metadata_type[:child_xml_names].nil? and metadata_type[:child_xml_names].kind_of? Array
        has_children_metadata = true
      end
      is_folder_metadata = metadata_type[:in_folder]
            
      metadata_request_type = (is_folder_metadata == true) ? "#{type}Folder" : type
      if metadata_request_type == "EmailTemplateFolder"
        metadata_request_type = "EmailFolder"
      end
      
      #puts metadata_type.inspect + "\n\n"
      
      self.mclient = get_metadata_client
      begin
        response = self.mclient.request :list_metadata do |soap|
          soap.header = get_soap_header  
          soap.body = "<ListMetadataQuery><type>#{metadata_request_type}</type></ListMetadataQuery>"
        end
      rescue Savon::SOAP::Fault => fault
        raise Exception.new(fault.to_s) if fault.to_s.not.include? "sf:INVALID_TYPE"
      end 
      
      begin
        #puts "beginning"
        return response unless ! raw
        
        if response.nil?
          return []
        end
        
        #puts "RESPONSE HASH: " + response.to_hash.inspect + "<br/><br/>"
            
        #if theres nothing there, return an empty array
        if response.to_hash[:list_metadata_response].nil? or response.to_hash[:list_metadata_response] == nil
          return []
        end
        
        hash = response.to_hash
        
        els = Array.new
        result_elements = []      
        if hash[:list_metadata_response][:result].kind_of? Hash
          result_elements.push(hash[:list_metadata_response][:result])
        else
          result_elements = hash[:list_metadata_response][:result]
        end
        #puts "result_elements: " + hash.inspect
                
        #if this type has children, make a retrieve request for the type
        #parse the response as appropriate
        object_hash = {} #=> {"Account" => [ {"fields" => ["foo", "bar"]}, "listviews" => ["foo", "bar"] ], "Contact" => ... }
        
        if has_children_metadata == true && result_elements.length > 0
          #testing stuff
          require 'zip/zipfilesystem'
          require 'fileutils'
          retrieve_body = "<RetrieveRequest><unpackaged><types><name>#{metadata_request_type}</name>"
          result_elements.each { |el| 
            retrieve_body << "<members>#{el[:full_name]}</members>"
          }
          retrieve_body << "</types></unpackaged><apiVersion>#{MM_API_VERSION}</apiVersion></RetrieveRequest>"
          zip_file = retrieve({ :body => retrieve_body })
          
          tmp_dir = Dir.tmpdir           
          random = MavensMate::Util.get_random_string
          mm_tmp_dir = "#{tmp_dir}/.org.mavens.mavensmate.#{random}" 
          
          Dir.mkdir(mm_tmp_dir)
          File.open("#{mm_tmp_dir}/metadata.zip", "wb") {|f| f.write(Base64.decode64(zip_file))}
          Zip::ZipFile.open("#{mm_tmp_dir}/metadata.zip") { |zip_file|
              zip_file.each { |f|
              f_path=File.join(mm_tmp_dir, f.name)
              FileUtils.mkdir_p(File.dirname(f_path))
              zip_file.extract(f, f_path) unless File.exist?(f_path)
            }
          }
          require 'nokogiri'
          # [{"Account" => [ {"fields" => ["foo", "bar"]}, "listviews" => ["foo", "bar"] ] }, ]
          
          Dir.foreach("#{mm_tmp_dir}/unpackaged/#{metadata_type[:directory_name]}") do |entry| #iterate the metadata folders
            #entry => Account.object
            
            next if entry == '.' || entry == '..' || entry == '.svn' || entry == '.git'
            #puts "processing: " + entry + "\n"
            
            doc = Nokogiri::XML(File.open("#{mm_tmp_dir}/unpackaged/#{metadata_type[:directory_name]}/#{entry}"))
            doc.remove_namespaces!
            
            c_hash = {}
            metadata_type[:child_xml_names].each { |c|
              tag_name = c[:tag_name]
              items = []
              doc.xpath("//#{tag_name}/fullName").each do |node|
                items.push(node.text)
              end 
              c_hash[tag_name] = items
            }
            base_name = entry.split(".")[0]
            object_hash[base_name] = c_hash
          end                         
          FileUtils.rm_rf mm_tmp_dir
        end

        result_elements.each { |el| 
          #puts "RESULT ELEMENT: " + el.inspect + "<br/>"
          #el => "Account"
          children = []
          full_name = el[:full_name]
          
          full_name = "Account" if full_name == "PersonAccount"
          object_detail = object_hash[full_name]
          
          #if this type has child metadata, we need to add the details
          if has_children_metadata == true
            #puts "OBJECT DETAIL: " + object_detail.inspect + "<br/><br/>" 
            next if object_detail.nil?
            metadata_type[:child_xml_names].each { |child_xml|
              #puts child_xml.inspect
              #puts child_xml[:tag_name]
              
              tag_name = child_xml[:tag_name]
              #puts object_detail.inspect
              if object_detail[tag_name].size > 0
                gchildren = []
                object_detail[tag_name].each do |gchild_el|
                  gchildren.push({
                    :title => gchild_el,
                    :key => gchild_el,
                    :isLazy => false,
                    :isFolder => false,
                    :selected => false
                  })
                end
                
                children.push({
                  :title => child_xml[:tag_name],
                  :key => child_xml[:tag_name],
                  :isLazy => false,
                  :isFolder => true,
                  :children => gchildren,
                  :selected => false
                })
              end
            } 
          end
          
          #if this type has folders, run queries to grab all metadata in the folders
          if is_folder_metadata == true          
            next if el[:manageable_state] != "unmanaged"
            folders = "<folder>#{el[:full_name]}</folder>"
            begin
              response = self.mclient.request :list_metadata do |soap|
                soap.header = get_soap_header  
                soap.body = "<ListMetadataQuery><type>#{type}</type>#{folders}</ListMetadataQuery>"
              end
            rescue Savon::SOAP::Fault => fault
              raise Exception.new(fault.to_s)
            end
            
            folder_elements = []  
            folder_hash = response.to_hash    
            if folder_hash[:list_metadata_response] && folder_hash[:list_metadata_response][:result]
              if folder_hash[:list_metadata_response][:result].kind_of? Hash
                folder_elements.push(folder_hash[:list_metadata_response][:result])
              else
                folder_elements = folder_hash[:list_metadata_response][:result]
              end 
            end
            
            folder_elements.each { |folder_el|
              children.push({
                :title => folder_el[:full_name].split("/")[1],
                :key => folder_el[:full_name],
                :isLazy => false,
                :isFolder => false,
                :selected => false
              })
            }           
          end
          
          els.push({
            :title => el[:full_name],
            :key => el[:full_name],
            :isLazy => is_folder_metadata || has_children_metadata,
            :isFolder => is_folder_metadata || has_children_metadata,
            :children => children,
            :selected => false
          })
        }
        els.sort! { |a,b| a[:title].downcase <=> b[:title].downcase }
        
        if format == "json"
          return els.to_json
        else
          return els
        end
      rescue Exception => e
        puts "\n\n\n" + e.message + "\n" + e.backtrace.join("\n")
      end
    end
                                                                
    private
            
      #ensures json is properly formatted for the dynatree control
      def to_json(what)
        what.to_hash.to_json
      end
      
      #returns header for soap calls with valid sessionid
      def get_soap_header
        return { "ins0:SessionHeader" => { "ins0:sessionId" => self.sid } } 
      end
      
      #returns body for soap calls with requested metadata specified
      def get_retrieve_body(options)
        types_body = ""
        if ! options[:package].nil?
          require 'rexml/document'
          xml_data = File.read(options[:package])
          doc = REXML::Document.new(xml_data)
          types_body = ""
          doc.elements.each('Package/types') do |el|
            types_body << "<types>"
            types_body << "<name>#{el.elements["name"].text}</name>"
            el.each_element do |member|
              if member.to_s.include? "<members>"
                types_body << "<members>#{member.text}</members>"
              end
            end
            types_body << "</types>"
          end
          #puts types_body
          return "<RetrieveRequest><unpackaged>#{types_body}</unpackaged><apiVersion>#{MM_API_VERSION}</apiVersion></RetrieveRequest>"
        else        
          if ! options[:path].nil? #grab path only
            path = options[:path]
            ext = File.extname(path).gsub(".","") #=> "cls"
            mt = MavensMate::FileFactory.get_meta_type_by_suffix(ext)
            file_name_no_ext = File.basename(path, File.extname(path)) #=> "myclass" 
            types_body << "<types><members>#{file_name_no_ext}</members><name>#{mt[:xml_name]}</name></types>"
          elsif ! options[:meta_types].nil? #custom built project	(using project wizard)
      			options[:meta_types].each { |meta_type, selected_children| 
      			    types_body << "<types>"
      			    if selected_children.length == 0
      			      types_body << "<members>*</members>"
      			    else
      			      selected_children.each { |child|  
        			      types_body << "<members>#{child}</members>"
      			      }
      			    end
      			    types_body << "<name>"+meta_type+"</name>"
      			    types_body << "</types>"
      			}    			
          else #grab from default package
            CORE_METADATA_TYPES.each { |type|  
              types_body << "<types><members>*</members><name>"+type+"</name></types>"
            }
          end     
          return "<RetrieveRequest><unpackaged>#{types_body}</unpackaged><apiVersion>#{MM_API_VERSION}</apiVersion></RetrieveRequest>"
        end
      end
      
      #returns salesforce credentials from keychain
      def get_creds 
        yml = YAML::load(File.open(ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/config/settings.yaml"))
        project_name = yml['project_name']
        username = yml['username']
        environment = yml['environment']
        password = KeyChain::find_internet_password("#{project_name}-mm")
        endpoint = environment == "sandbox" ? "https://test.salesforce.com/services/Soap/u/#{MM_API_VERSION}" : "https://www.salesforce.com/services/Soap/u/#{MM_API_VERSION}"
        return { :username => username, :password => password, :endpoint => endpoint }
      end
      
      #returns partner connection
      def get_partner_client
        client = Savon::Client.new do |wsdl, http|
          wsdl.document = File.expand_path(ENV['TM_BUNDLE_SUPPORT']+"/wsdl/partner.xml", __FILE__)
          http.proxy = ENV["http_proxy"] if ENV["http_proxy"]
        end
        client.wsdl.endpoint = self.endpoint        
        return client
      end
      
      #returns metadata connection
      def get_metadata_client
        client = Savon::Client.new do |wsdl, http|
          wsdl.document = File.expand_path(ENV['TM_BUNDLE_SUPPORT']+"/wsdl/metadata.xml", __FILE__)
          http.proxy = ENV["http_proxy"] if ENV["http_proxy"]
        end
        client.wsdl.endpoint = self.metadata_server_url
        return client
      end
      
  end
end