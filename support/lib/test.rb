#!/usr/bin/env ruby -W0
MM_ROOT = File.dirname(__FILE__)
require MM_ROOT + '/test_helper'

`osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/growl.scpt' 'Hello PhillyForce!!!!'`





# ENV['TM_PROJECT_DIRECTORY'] = '/Users/josephferraro/Projects/joe_ferraro_3'
#                       
# params = {
#   :package => { "ApexClass" => ["CompileAndTest"], "Layout" => ["Account-Account Layout"] },
#   :orgs => [
#     { :un => "joeferraro@force.com", 
#       :pw => "352198",
#       :endpoint => "https://www.salesforce.com" 
#     },
#     { :un => "joeferraro2@force.com", 
#       :pw => "352198",
#       :endpoint => "https://www.salesforce.com" 
#     }
#   ]
# }
# MavensMate.diff(params)   

#puts Dir["/private/var/folders/m3/kt10_j3j5417w5xvxxywdj080000gp/T/.org.mavens.mavensmate.ZztZGSiLL/**/*CompileAndTestss.cls"].inspect

# is_match = false
# begin  
#   is_match = FileUtils.compare_file('/Users/josephferraro/Desktop/joeferraro@force.com/unpackaged/classes/CompileAndTest.cls', '/Users/josephferraro/Desktop/joeferraro2@force.com/unpackaged/classes/CompileAndTest.cls')
# rescue Exception => e
#    is_match = false if e.message.include? "No such file or directory"
# end  
# 
# puts is_match 
  
#puts Diffy::Diff.new(
#  '/Users/josephferraro/Desktop/joeferraro@force.com/unpackaged/classes/CompileAndTest.cls', 
#  '/Users/josephferraro/Desktop/joeferraro2@force.com/unpackaged/classes/CompileAndTest.cls', 
#  :source => 'files')



