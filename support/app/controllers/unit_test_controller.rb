# encoding: utf-8
require SUPPORT + '/lib/mavensmate.rb'

class UnitTestController < ApplicationController
    
  layout "base", :only => [:index]
            
  def index
    render "_index", :locals => { :classes => class_list }
  end
  
  def run_tests(tests)
    result = MavensMate.run_tests(tests)
    #return result
    #puts "run test result: " + result.inspect
    #return render "_test_result", :locals => { :result => result }
  end

  def show_test_result
    #render "_test_result", :locals => { :result => params[:result] }
    return render_to_string "_foo_bar"
  end
  
  private
    
    def class_list
      classes = []
      pd = ENV['MM_CURRENT_PROJECT_DIRECTORY']
      Dir.foreach("#{pd}/src/classes") do |cls| 
        next if cls == "." or cls == ".." or cls.include? "-meta.xml" or cls == ".svn"
        begin
          if File.readlines("#{pd}/src/classes/#{cls}").grep(/@istest/i).size > 0 or File.readlines("#{pd}/src/classes/#{cls}").grep(/testmethod/i).size > 0
            classes.push(cls.split(".")[0])
          end
        rescue
          next
        end
      end
      return classes
    end
end