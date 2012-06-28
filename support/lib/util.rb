module MavensMate
  module Util
    class << self
      
      #include MetadataHelper
      
      def get_random_string(len=8)
        o =  [('a'..'z'),('A'..'Z')].map{|i| i.to_a}.flatten;  
        string = (0..len).map{ o[rand(o.length)]  }.join;
      end

      def set_project_directory(search_path)
        found = false
        while found == false
          if ! Dir.entries(search_path).include?(".sublime-project")
            search_path = File.dirname(search_path)
            next
          else
            ENV["MM_CURRENT_PROJECT_DIRECTORY"] = search_path
            found = true
          end
        end
      end
      
      def get_sfdc_endpoint(url)
         endpoint = (url.include? "test") ? "https://test.salesforce.com/services/Soap/u/#{MM_API_VERSION}" : "https://www.salesforce.com/services/Soap/u/#{MM_API_VERSION}"  
      end
      
      def parse_deploy_response(response)
        response = response[:check_deploy_status_response][:result]
        test_failures = []
        test_successes = []
        coverage_warnings = []
        coverage = []
        messages = []
        
        if response[:run_test_result][:failures]
          if ! response[:run_test_result][:failures].kind_of? Array
            test_failures.push(response[:run_test_result][:failures])
          else
            test_failures = response[:run_test_result][:failures]
          end
        end
        
        if response[:run_test_result][:successes]
          if ! response[:run_test_result][:successes].kind_of? Array
            test_successes.push(response[:run_test_result][:successes])
          else
            test_successes = response[:run_test_result][:successes]
          end
        end
        
        if response[:run_test_result][:code_coverage_warnings]
          if ! response[:run_test_result][:code_coverage_warnings].kind_of? Array
            coverage_warnings.push(response[:run_test_result][:code_coverage_warnings])
          else
            coverage_warnings = response[:run_test_result][:code_coverage_warnings]
          end
        end
        
        if response[:run_test_result][:code_coverage]
          if ! response[:run_test_result][:code_coverage].kind_of? Array
            coverage.push(response[:run_test_result][:code_coverage])
          else
            coverage = response[:run_test_result][:code_coverage]
          end
        end
        
        if response[:messages]
          if ! response[:messages].kind_of? Array
            messages.push(response[:messages])
          else
            messages = response[:messages]
          end
        end
        
        return {
          :is_success => response[:success],
          :test_failures => test_failures,
          :test_successes => test_successes,
          :coverage_warnings => coverage_warnings,
          :coverage => coverage,
          :messages => messages
        }

      end
        
    end
  end
end