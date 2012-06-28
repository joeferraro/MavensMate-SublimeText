require 'erb'   

class TestHelper

  class << self

    def put_project(name)
      project_folder = ENV['FM_PROJECT_FOLDER']
      project_folder +='/' unless project_folder.end_with?("/")
      Dir.mkdir(project_folder) unless File.exists?(project_folder)
      Dir.mkdir(project_folder+"/"+name)
      Dir.mkdir(project_folder+"/"+name+"/src")
      Dir.mkdir(project_folder+"/"+name+"/src/classes")
      api_name = "foo"
      template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/templates/ApexClass.html.erb").read, nil, "%"
      erb = template.result(binding)        
      src = File.new(project_folder+"/"+name+"/src/classes/foo.cls", "w")
      src.puts(erb)
      src.close       
    end
  
  end  
    
end