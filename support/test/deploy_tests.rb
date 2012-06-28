require "test/unit"
require 'rubygems'
require 'fileutils'

MM_ROOT = File.dirname(__FILE__)
ENV['TM_BUNDLE_SUPPORT'] = MM_ROOT + "/.."
require ENV['TM_BUNDLE_SUPPORT'] + '/environment.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/app/controllers/project_controller.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/tests/test_helper.rb'

class ProjectTests < Test::Unit::TestCase
 
  def test_deploy
    params = {}
    params[:un]         = "mm@force.com"
    params[:pw]         = "force"
    params[:server_url] = "https://www.salesforce.com"
    params[:package]    = {"ApexClass" => "foo"}       
    #FileUtils.rm_r "#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}" if File.exist?("#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}")     
    TestHelper.put_project("unit_test_project")
  end
  
end