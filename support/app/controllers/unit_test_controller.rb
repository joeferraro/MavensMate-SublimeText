# encoding: utf-8
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'

class UnitTestController < ApplicationController
    
  layout "base", :only => [:index]
            
  def index
    render "_index", :locals => { :classes => class_list }
  end
  
  def run_tests
    if ! params[:selected_tests]
      TextMate::UI.alert(:warning, "MavensMate", "Please select at least 1 Apex unit test to run")
      abort
    end
    selected_tests = params[:selected_tests].split(",")
    begin
      result = MavensMate.run_tests(selected_tests)
      render "_test_result", :locals => { :result => result }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message + e.backtrace.join("\n"))
    end
  end
  
  private
    
    def class_list
      classes = []
      pd = ENV['TM_PROJECT_DIRECTORY']
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