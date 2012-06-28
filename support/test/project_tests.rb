require "test/unit"
require 'rubygems'
require 'fileutils'

MM_ROOT = File.dirname(__FILE__)
ENV['TM_BUNDLE_SUPPORT'] = MM_ROOT + "/.."
require ENV['TM_BUNDLE_SUPPORT'] + '/environment.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/app/controllers/project_controller.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'

class ProjectTests < Test::Unit::TestCase
 
  def test_new_project
    params = {}
    params[:pn]         = "mavensmate - new_test1"
    params[:un]         = "mm@force.com"
    params[:pw]         = "force"
    params[:server_url] = "https://www.salesforce.com"
    params[:package]    = {"ApexClass" => "*", "CustomObject" => "Account"}    
    params[:vc_un]      = "mavens"
    params[:vc_pw]      = "mavens123"
    params[:vc_url]     = ""
    params[:vc_type]    = "SVN"
    params[:vc_branch]  = "master"      
    FileUtils.rm_r "#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}" if File.exist?("#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}")     
    MavensMate.new_project(params)
  end
  
  def test_checkout_svn_project
    params = {}
    params[:pn]         = "mavensmate - checkout_test1"
    params[:un]         = "mm@force.com"
    params[:pw]         = "force"
    params[:server_url] = "https://www.salesforce.com"
    params[:package]    = {"ApexClass" => "*", "CustomObject" => "Account"}    
    params[:vc_un]      = "mavens"
    params[:vc_pw]      = "mavens123"
    params[:vc_url]     = "https://wearemavens.svn.beanstalkapp.com/test/branches/mysandbox10"
    params[:vc_type]    = "SVN"
    params[:vc_branch]  = ""      
    FileUtils.rm_r "#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}" if File.exist?("#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}")     
    MavensMate.checkout_project(params)
  end
  
  def test_checkout_git_project
    params = {}
    params[:pn]         = "mavensmate - checkout_test2"
    params[:un]         = "mm@force.com"
    params[:pw]         = "force"
    params[:server_url] = "https://www.salesforce.com"
    params[:package]    = {"ApexClass" => "*", "CustomObject" => "Account"}    
    params[:vc_un]      = "mavens"
    params[:vc_pw]      = "mavens123"
    params[:vc_url]     = "git@wearemavens.beanstalkapp.com:/testgit2.git"
    params[:vc_type]    = "Git"
    params[:vc_branch]  = "staging"      
    FileUtils.rm_r "#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}" if File.exist?("#{ENV['FM_PROJECT_FOLDER']}/#{params[:pn]}")     
    MavensMate.checkout_project(params)
  end
end