require 'rubygems'
require 'zip/zipfilesystem'
require 'fileutils'   
require 'tmpdir'
require 'base64'
require SUPPORT + '/lib/metadata_helper.rb' 
require SUPPORT + '/lib/util.rb'
require SUPPORT + '/environment.rb'
require 'erb'

module MavensMate
  module FileFactory
       
      class << self
      
      include MetadataHelper
      
      #updates package xml based on the current contents of the file system
      def update_package_xml
        project_package = Nokogiri::XML(File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/package.xml"))
        project_package.remove_namespaces!
        project_package.xpath("//types/name").each do |node| 
           if CORE_METADATA_TYPES.include?(node.text) && node.previous_element.text != "*"
               meta_type = get_meta_type_by_name(node.text)                
               node.parent.children.each do |n|
                 n.remove if n.name == "members"
               end
               Dir.foreach("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/#{meta_type[:directory_name]}") do |entry|    
                 next if entry == "." or entry == ".." or entry.include? "-meta"
                 entry = entry.split(".")[0]
                 node.add_previous_sibling("\t\t<members>#{entry}</members>\n")
               end
               node.add_previous_sibling("\t\t")
               node.parent.children.each_with_index do |n, i|
                 next if i == 0
                 break if n.name != "text"  
                 n.remove
               end
           end
        end
        File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/package.xml", 'w') {|f| f.write(project_package.to_xml) }
      end
      
      #puts spec
      def put_spec_tests(project_name, server_url, is_sandbox)
        Dir.mkdir("#{MavensMate.get_project_folder}#{project_name}/spec/")
        login_url = (is_sandbox) ? "https://test.salesforce.com" : "https://login.salesforce.com"
        subdomain = server_url.match(/\/\/(.*?)-/)[1]        
        file_name = "spec_helper.rb"
        project_directory = "#{MavensMate.get_project_folder}#{project_name}"
        template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/spec_helper.erb").read, nil, "-"
        erb = template.result(binding)        
        src = File.new("#{MavensMate.get_project_folder}#{project_name}/spec/#{file_name}", "w")
        src.puts(erb)
        src.close
        
        Dir.foreach("#{MavensMate.get_project_folder}#{project_name}/src/pages") do |page|
          next unless page.end_with?(".page")
          page_name = page.split(".")[0]
          file_name = "#{page_name}_spec.rb"
          template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/spec_vf_page.erb").read, nil, "-"
          erb = template.result(binding)        
          src = File.new("#{MavensMate.get_project_folder}#{project_name}/spec/#{file_name}", "w")
          src.puts(erb)
          src.close
        end  
      end
      
      #puts single spec upon vf page creation
      def put_spec_test(page_name)
        file_name = "#{page_name}_spec.rb"
        template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/spec_vf_page.erb").read, nil, "-"
        erb = template.result(binding)        
        src = File.new("#{MavensMate.get_project_folder}#{MavensMate.get_project_name}/spec/#{file_name}", "w")
        src.puts(erb)
        src.close  
      end
           
      #puts settings.yaml in the project config directory
      def put_project_config(username, project_name, endpoint, namespace)
        project_folder = MavensMate.get_project_folder
        project_folder +='/' unless project_folder.end_with?("/")
        Dir.mkdir(project_folder+project_name+"/config") unless File.exists?(project_folder+project_name+"/config")
        file_name = "settings.yaml"
        if ! File.exists?(project_folder+project_name+"/config/settings.yaml")
          src = File.new(project_folder+project_name+"/config/settings.yaml", "w")
          src.puts("project_name: " + project_name)
          src.puts("username: " + username)
          src.puts("environment: " + MavensMate::Util.get_endpoint_type_by_url(endpoint))
          src.puts("namespace: " + namespace) if namespace
          src.close
        else
          src = File.open(project_folder+project_name+"/config/settings.yaml", "w") 
          src.puts("project_name: " + project_name)
          src.puts("username: " + username)
          src.puts("environment: " + MavensMate::Util.get_endpoint_type_by_url(endpoint))
          src.puts("namespace: " + namespace) if namespace
          src.close
        end
      end

      def put_sublime_text_project_file(project_name)
        project_folder = MavensMate.get_project_folder
        file_name = "settings.yaml"
        src = File.new(project_folder+project_name+"/"+project_name+".sublime-project", "w")
        src.puts('{"folders":[{"path": "'+project_folder+project_name+'"}],"settings":{"mm_project_directory":"'+project_folder+project_name+'"}}')
        src.close
      end
      
      #puts the base project directory on the drive
      def put_project_directory(project_name)
        project_folder = MavensMate.get_project_folder
        project_folder +='/' unless project_folder.end_with?("/")
        Dir.mkdir(project_folder) unless File.exists?(project_folder)
        Dir.mkdir(project_folder+"/"+project_name)
      end
      
      def put_project_metadata(project_name, project_zip)
        project_folder = MavensMate.get_project_folder
        Dir.chdir(project_folder+"/"+project_name)
        File.open('metadata.zip', 'wb') {|f| f.write(Base64.decode64(project_zip))}
        Zip::ZipFile.open('metadata.zip') { |zip_file|
            zip_file.each { |f|
              f_path=File.join(project_folder+"/"+project_name, f.name)
              FileUtils.mkdir_p(File.dirname(f_path))
              zip_file.extract(f, f_path) unless File.exist?(f_path)
            }
          }
        FileUtils.rm_r project_folder+"/"+project_name+"/metadata.zip"
        FileUtils.mv project_folder+"/"+project_name+"/unpackaged", project_folder+"/"+project_name+"/src"        
      end
      
      #puts retrieved object metadata in "config" project directory
      def put_object_metadata(project_name, object_zip)
        #clean_directory("#{ENV["MM_WORKSPACE"]}/#{project_name}/config/objects", ".object") 
        extract(object_zip, "#{ENV["MM_WORKSPACE"]}/#{project_name}/config")  
        if File.exist?("#{ENV["MM_WORKSPACE"]}/#{project_name}/config/objects")
          mv_c("#{ENV["MM_WORKSPACE"]}/#{project_name}/config/unpackaged/objects", "#{ENV["MM_WORKSPACE"]}/#{project_name}/config/objects")          
        else
          FileUtils.mv "#{ENV["MM_WORKSPACE"]}/#{project_name}/config/unpackaged/objects", "#{ENV["MM_WORKSPACE"]}/#{project_name}/config"          
        end
        FileUtils.rm_r "#{ENV["MM_WORKSPACE"]}/#{project_name}/config/unpackaged"
      end
      
      #extracts a zip file to the specified location
      def extract(zip_file, where)
        File.open(where+'/metadata.zip', 'wb') {|f| f.write(Base64.decode64(zip_file))}
        Zip::ZipFile.open(where+'/metadata.zip') { |zip_file|
          zip_file.each { |f|
            f_path=File.join(where, f.name)
            FileUtils.mkdir_p(File.dirname(f_path))
            zip_file.extract(f, f_path) unless File.exist?(f_path)
          } 
        }
        FileUtils.rm_r where+'/metadata.zip'
      end
      
      def finish_clean(project_name, project_zip)
        #project_folder = ENV['MM_WORKSPACE']
        File.open("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/metadata.zip", 'wb') {|f| f.write(Base64.decode64(project_zip))}
        Zip::ZipFile.open("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/metadata.zip") { |zip_file|
            zip_file.each { |f|
              f_path=File.join("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}", f.name)
              FileUtils.mkdir_p(File.dirname(f_path))
              zip_file.extract(f, f_path) unless File.exist?(f_path)
            }
          }
        FileUtils.rm_r "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/metadata.zip"
        
        Dir.foreach("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/unpackaged") do |meta_folder| #iterate the retrieve data
          next if meta_folder.include? "." #ignore hidden items or package.xml
          
          #create the metadata folder if it's new to the project
          FileUtils.mkdir "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{meta_folder}" unless File.directory? "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{meta_folder}"
          
          #iterate each metadata folder
          Dir.foreach("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/unpackaged/#{meta_folder}") do |meta_file|
            next if meta_file == '.' || meta_file == '..'            
            FileUtils.mv "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/unpackaged/#{meta_folder}/#{meta_file}", "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{meta_folder}/#{meta_file}"
          end
        end
        
        Dir.foreach("#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src") do |meta_folder| #iterate the fresh project folder
          next if meta_folder.include? "." #ignore hidden items or package.xml
          FileUtils.rm_rf "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{meta_folder}" if Dir["#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{meta_folder}/*"].empty?
        end
        
        FileUtils.rm_rf "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/unpackaged"
      end
      
      def replace_file(file_path, project_zip)
        File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/metadata.zip", 'wb') {|f| f.write(Base64.decode64(project_zip))}
        Zip::ZipFile.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/metadata.zip") { |zip_file|
           zip_file.each { |f|
             f_path=File.join(ENV['MM_CURRENT_PROJECT_DIRECTORY'], f.name)
             FileUtils.mkdir_p(File.dirname(f_path))
             zip_file.extract(f, f_path) unless File.exist?(f_path)
           }
         }
         meta_type_ext = File.extname(file_path) #=> ".cls"
         meta_type_no_ext = meta_type_ext.gsub(".","")
         mt = get_meta_type_by_suffix(meta_type_no_ext)
         copy_to_dir = "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/#{mt[:directory_name]}" #=> "/Users/username/Projects/myproject/src/classes"
         FileUtils.cp_r "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/unpackaged/#{mt[:directory_name]}/.", "#{copy_to_dir}"
         FileUtils.rm_r "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/unpackaged"
         FileUtils.rm_r "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/metadata.zip"
      end
      
      def put_delete_metadata(hash)
        cleanup_tmp        
        put_package(Dir.getwd, binding, true)
        put_empty_package(Dir.getwd)        
        return zip_tmp_directory
      end
      
      def put_empty_metadata
        cleanup_tmp        
        put_empty_package(Dir.getwd)        
        return zip_tmp_directory
      end
            
      def put_tmp_metadata(hash)
        cleanup_tmp
        put_tmp_directories(hash)
        put_package(Dir.getwd, binding, false)
        put_files_in_tmp_directories(hash)
        return zip_tmp_directory                       
      end
             
      def copy_project_to_tmp
        tmp_dir = Dir.tmpdir
        FileUtils.rm_rf("#{tmp_dir}/mmzip")
        Dir.mkdir("#{tmp_dir}/mmzip")
        Dir.mkdir("#{tmp_dir}/mmzip/unpackaged")
        unpackaged_dir = "#{tmp_dir}/mmzip/unpackaged"
        %x{cp -R '#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/' '#{unpackaged_dir}'}      
        return zip_tmp_directory
      end 
       
      #puts metadata in a specified directory
      #if [:dir] is nil, it's assumed you want to put it in the project folder              
      def put_local_metadata(options = { })
        api_name        = options[:api_name]
        meta_type       = options[:meta_type]
        object_name     = options[:object_name]        
        dir             = options[:dir]
        apex_class_type = options[:apex_class_type]
        
        if dir.nil?       
          dir = ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/src/" + META_DIR_MAP[meta_type]
          if ! File.directory?(dir)
        	  Dir.mkdir(dir)
          end
          Dir.chdir(dir)
        elsif dir == "tmp"
          tmp_dir = Dir.tmpdir
          FileUtils.rm_rf("#{tmp_dir}/mmzip")
          Dir.mkdir("#{tmp_dir}/mmzip")
          Dir.mkdir("#{tmp_dir}/mmzip/unpackaged")
          Dir.mkdir("#{tmp_dir}/mmzip/unpackaged/"+META_DIR_MAP[meta_type])
          Dir.chdir("#{tmp_dir}/mmzip/unpackaged/"+META_DIR_MAP[meta_type])
        else
          Dir.chdir(dir)
        end

        file_name = put_src_file(:api_name => api_name, :meta_type => meta_type, :object_name => object_name, :apex_class_type => apex_class_type)
        put_meta_file(:api_name => api_name, :meta_type => meta_type, :object_name => object_name)
        
        if ! options[:dir].nil?
          Dir.chdir('..')
          put_new_package(Dir.getwd, binding, false)
        end
        
        if dir == "tmp"
          Dir.chdir("#{tmp_dir}/mmzip")
          path = "#{tmp_dir}/mmzip"

          Zip::ZipFile.open("deploy.zip", 'w') do |zipfile|
            Dir["#{path}/**/**"].each do |file|
              zipfile.add(file.sub(path+'/',''),file)
            end
          end

          Dir.chdir("#{tmp_dir}/mmzip")
          file_contents = File.read("deploy.zip")
          base64Package = Base64.encode64(file_contents)
        else
          
        end
      end
                
      #returns the metadata definition by suffix (.cls, .trigger, .object, etc.)
      def get_meta_type_by_suffix(suffix)
        return META_DICTIONARY.detect {|f| f[:suffix] == suffix }
      end
      
      #returns the metadata definition by directory (classes, objects, etc.)
      def get_meta_type_by_dir(dir)
        return META_DICTIONARY.detect {|f| f[:directory_name] == dir }
      end
      
      #returns the metadata definition by name
      def get_meta_type_by_name(name)
        return META_DICTIONARY.detect {|f| f[:xml_name] == name }
      end
      
      #returns the metadata definition by name - child types (customfield, listview, etc.)
      def get_child_meta_type_by_name(name)
        return CHILD_META_DICTIONARY.detect {|f| f[:xml_name] == name }
      end
      
      #puts an erb generated package.xml file in the specified location
      def put_package(where, binding, delete=false)
        Dir.mkdir(where) unless File.exists?(where)
        Dir.chdir(where)
        file_name = delete ? "destructiveChanges.xml" : "package.xml"
        template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/package.html.erb").read, nil, "-"
        erb = template.result(binding)        
        src = File.new(file_name, "w")
        src.puts(erb)
        src.close
      end
      
      def put_tmp_directory
        tmp_dir = Dir.tmpdir
        random = MavensMate::Util.get_random_string
        mmzip_folder = "#{tmp_dir}/.org.mavens.mavensmate.#{random}"
        Dir.mkdir mmzip_folder
        return mmzip_folder
      end

      def get_request_id_and_put_tmp_directory
        tmp_dir = Dir.tmpdir
        random = MavensMate::Util.get_random_string
        mmzip_folder = "#{tmp_dir}/.org.mavens.mavensmate.#{random}"
        Dir.mkdir mmzip_folder
        return random, mmzip_folder
      end

      def get_tmp_response_file(id)
        tmp_dir = Dir.tmpdir
        return "#{tmp_dir}/.org.mavens.mavensmate.#{id}/.response"
      end

      def response_ready?(id)
        tmp_dir = Dir.tmpdir
        if File.exist?("#{tmp_dir}/.org.mavens.mavensmate.#{id}/.response")
          return true
        else
          return false
        end
      end
      
      def remove_directory(dir)
        FileUtils.rm_rf dir if File.exist?(dir)
      end
            
      #removes files with the specified extension from a directory
      def clean_directory(dir, extension="")
        begin
          FileUtils.rm Dir.glob("#{dir}/*#{extension}") if File.exist?(dir)
        rescue
        end
      end
                  
      private
        
        #moves files from source directory to destination directory
        def mv_c(source, destination)
          destination = destination + "/" unless destination.end_with?("/")
          files = Dir.glob("#{source}/*");
          files.each { |file|
            FileUtils.mv(file, destination + File.basename(file))
          }
        end
                        
        def cleanup_tmp
          FileUtils.rm_rf("#{Dir.tmpdir}/mmzip")
          Dir.mkdir("#{Dir.tmpdir}/mmzip")
          Dir.mkdir("#{Dir.tmpdir}/mmzip/unpackaged")
          Dir.chdir("#{Dir.tmpdir}/mmzip/unpackaged")
        end
      
        def put_files_in_tmp_directories(hash)
          hash.each { |key, value|
            mt = get_meta_type_by_name(key)
            Dir.chdir("#{Dir.tmpdir}/mmzip/unpackaged/#{mt[:directory_name]}")
            value.each do |f|
              FileUtils.copy_file(
                "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/#{mt[:directory_name]}/#{f}.#{mt[:suffix]}",
                "#{Dir.getwd}/#{f}.#{mt[:suffix]}"
              )
              if mt[:meta_file]
              FileUtils.copy_file(
                "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/#{mt[:directory_name]}/#{f}.#{mt[:suffix]}-meta.xml",
                "#{Dir.getwd}/#{f}.#{mt[:suffix]}-meta.xml"
              )
              end
            end
          }
        end
      
        def put_tmp_directories(hash)
          hash.each { |key, value|
            mt = get_meta_type_by_name(key)
            Dir.mkdir("#{Dir.tmpdir}/mmzip/unpackaged/#{mt[:directory_name]}")
            if mt[:in_folder]
              value.each do |v|
                arr = v.split("/")
                if arr.length && arr.length == 2
                  Dir.mkdir("#{Dir.tmpdir}/mmzip/unpackaged/#{mt[:directory_name]}/#{arr[0]}") unless File.exists?("#{Dir.tmpdir}/mmzip/unpackaged/#{mt[:directory_name]}/#{arr[0]}")
                end
              end
            end
          }
        end
      
        def zip_tmp_directory
          tmp_dir = Dir.tmpdir
          #Dir.chdir("#{tmp_dir}/mmzip")
          Zip::ZipFile.open("#{tmp_dir}/mmzip/deploy.zip", 'w') do |zipfile|
            Dir["#{tmp_dir}/mmzip/**/**"].each do |file|
              zipfile.add(file.sub("#{tmp_dir}/mmzip/",""),file)
            end
          end
          #Dir.chdir("#{tmp_dir}/mmzip")
          file_contents = File.read("#{tmp_dir}/mmzip/deploy.zip")
          return Base64.encode64(file_contents)
        end
        
        def put_new_package(where, binding, delete=false)
          Dir.chdir(where)
          file_name = delete ? "destructiveChanges.xml" : "package.xml"
          template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/new_package.html.erb").read, nil, "-"
          erb = template.result(binding)        
          src = File.new(file_name, "w")
          src.puts(erb)
          src.close
        end
                      
        def put_empty_package(where)
          Dir.chdir(where)
          template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/empty_package.html.erb").read, nil, "-"
          erb = template.result(binding)       
          src = File.new("package.xml", "w")
          src.puts(erb)
          src.close
        end
        
        #puts a new source file on the drive (apexclass, apextrigger, apexpage, etc.)    
        def put_src_file(options = { })
          api_name = options[:api_name]
          meta_type = options[:meta_type]
          object_name = options[:object_name]
          apex_class_type = options[:apex_class_type]
          file_name = "#{api_name}" + META_EXT_MAP[meta_type]
          template = nil
          if meta_type == "ApexClass" && ! apex_class_type.nil?
            template_name = ""
            if apex_class_type == "test"
              template_name = "UnitTestApexClass"
            elsif apex_class_type == "batch"
              template_name = "BatchApexClass"
            elsif apex_class_type == "schedulable"
              template_name = "SchedulableApexClass"
            elsif apex_class_type == "email"
              template_name = "EmailServiceApexClass"
            elsif apex_class_type == "url"
              template_name = "UrlRewriterApexClass"
            elsif apex_class_type == "empty"
              template_name = "ApexClassNoConstructor"
            elsif apex_class_type == "exception"
              template_name = "ApexExceptionClass"
            else
              template_name = "ApexClass"
            end
            template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/#{template_name}.html.erb").read, nil, "%"            
          else
            template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/#{meta_type}.html.erb").read, nil, "%"            
          end               
          erb = template.result(binding)        
          src = File.new(file_name, "w")
          src.puts(erb)
          src.close       
          return file_name
        end
      
        #puts a new .meta-xml file on the drive    
        def put_meta_file(options = { })
          api_name = options[:api_name]
          meta_type = options[:meta_type]
          object_name = options[:object_name]
        
          src_meta_file_name = api_name + META_EXT_MAP[meta_type] + "-meta.xml"
        
          template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/meta.html.erb").read, nil, "-"
          erb = template.result(binding)        
          src = File.new(src_meta_file_name, "w")
          src.puts(erb)
          src.close
        end
         
    end   
  end
end