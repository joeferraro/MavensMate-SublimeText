module MetadataHelper
  
  MM_API_VERSION = MM_USER_CONFIG['mm_api_version'] || MM_DEFAULT_CONFIG['mm_api_version'] || ENV['MM_API_VERSION'] || "26.0" 
  CORE_METADATA_TYPES = [ "ApexClass", "ApexComponent", "ApexPage", "ApexTrigger", "StaticResource" ]  
  META_DICTIONARY = eval(File.read("#{SUPPORT}/conf/metadata_dictionary"))
  CHILD_META_DICTIONARY = eval(File.read("#{SUPPORT}/conf/metadata_children_dictionary"))
  MM_TIMEOUT = MM_USER_CONFIG['mm_timeout'] || MM_DEFAULT_CONFIG['mm_timeout'] || ENV['MM_TIMEOUT'] || 3600
  
  META_LABEL_MAP = { 
    "ApexClass" => "Apex Class", 
    "ApexComponent" => "Visualforce Component", 
    "ApexPage" => "Visualforce Page", 
    "ApexTrigger" => "Apex Trigger", 
    "StaticResource" => "Static Resource" 
  }
  
  META_DIR_MAP = { 
    "ApexClass" => "classes", 
    "ApexComponent" => "components", 
    "ApexPage" => "pages", 
    "ApexTrigger" => "triggers", 
    "StaticResource" => "staticresources" 
  }
  
  META_EXT_MAP = { 
    "ApexClass" => ".cls", 
    "ApexComponent" => ".component", 
    "ApexPage" => ".page", 
    "ApexTrigger" => ".trigger", 
    "StaticResource" => ".resource" 
  }
  
  EXT_META_MAP = { 
    ".cls" => "ApexClass", 
    ".component" => "ApexComponent", 
    ".page" => "ApexPage", 
    ".trigger" => "ApexTrigger", 
    ".resource" => "StaticResource" 
  }

  class << self
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
  end   
end
