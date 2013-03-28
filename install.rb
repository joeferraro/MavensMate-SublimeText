require 'rbconfig'
require 'fileutils'

module OS
  def OS.windows?
    (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
  end

  def OS.mac?
   (/darwin/ =~ RUBY_PLATFORM) != nil
  end

  def OS.unix?
    !OS.windows?
  end

  def OS.linux?
    OS.unix? and not OS.mac?
  end
end

if (OS.mac?) then
  @packages_path = File.expand_path("~/Library/Application Support/Sublime Text 2/Packages")
  @origin = 'joeferraro'
  @branch = 'master'
elsif (OS.linux?) then
  @packages_path = File.expand_path("~/.config/sublime-text-2/Packages")
  @origin = 'amtrack'
  @branch = 'linux_windows'
elsif (OS.windows?) then
  @packages_path = File.expand_path("~/AppData/Roaming/Sublime Text 2/Packages")
  @origin = 'amtrack'
  @branch = 'linux_windows'
end
@install_path = File.join(@packages_path, "MavensMate")
@user_settings_path = File.join(@packages_path, "User")
@github_uri = "https://github.com/#{@origin}/MavensMate-SublimeText.git"

def check_requirements
  if OS.mac? then
    # nothing so far?
  elsif OS.windows? or OS.linux? then
    puts "please make sure 'google chrome' (http://www.google.com/chrome) is installed!"
    puts "please make sure 'doxygen' (http://www.doxygen.org/) is installed!"
    puts "please make sure 'keyring' (http://pypi.python.org/pypi/keyring) is installed"
  end
end

def install_package
  puts "installing MavensMate Sublime Text 2 package to '#{@install_path}'"
  FileUtils.mkdir_p(@packages_path)
  %x{git clone -b #{@branch} --origin #{@origin} #{@github_uri} "#{@install_path}"}
end

def install_user_settings
  #update_user_config if File.exist?("#{@user_settings_path}/mavensmate.sublime-settings"
  FileUtils.copy("#{@install_path}/mavensmate.sublime-settings", @user_settings_path) unless File.exist?("#{@user_settings_path}/mavensmate.sublime-settings")
end

# def update_user_config
#   begin
#     require 'json'
#     json = File.read("#{@user_settings_path}/mavensmate.sublime-settings")
#     existing_config = JSON.parse(json)
#     json = File.read("#{@install_path}/mavensmate.sublime-settings")
#     new_config = JSON.parse(json)
#     new_config.each_pair do |k,v|
#       next if existing_config.has_key?(k)
#       existing_config[k] = v
#     end
#     updated_config = JSON.pretty_generate(existing_config)
#     f = File.open("#{@user_settings_path}/mavensmate.sublime-settings","w")
#     f.write(updated_config)
#     f.close
#   rescue Exception => e
#     puts "error updating user config: " + e.message
#   end
# end

def install
	if OS.mac? or OS.linux? or OS.windows?
    check_requirements
    install_package
    install_user_settings
  else
    puts "Could not install MavensMate. Your Operating System is not supported."
	end
end

def uninstall
  puts "uninstalling MavensMate Sublime Text 2 package"
  FileUtils.rm_rf(@install_path)
end

uninstall
install