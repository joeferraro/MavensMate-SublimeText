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
  @install_path = File.expand_path("~/Library/Application Support/Sublime Text 2/Packages/MavensMate")
  @user_settings_path = File.expand_path("~/Library/Application Support/Sublime Text 2/Packages/User")
elsif (OS.linux?) then
  @install_path = File.expand_path("~/.config/sublime-text-2/Packages/MavensMate")
  @user_settings_path = File.expand_path("~/.config/sublime-text-2/Packages/User")
end

def install_package
  `git clone git://github.com/joeferraro/MavensMate-SublimeText.git '#{@install_path}'`
end

def install_user_settings
  #update_user_config if File.exist?("#{@user_settings_path}/mavensmate.sublime-settings"
  `cp '#{@install_path}/mavensmate.sublime-settings' '#{@user_settings_path}'` unless File.exist?("#{@user_settings_path}/mavensmate.sublime-settings")
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
	if OS.windows?
    #future functionality
	elsif OS.mac?
    install_package
    install_user_settings
  elsif OS.linux?
    %x{pip install gkeyring}
    install_package
    install_user_settings
	end
end

def uninstall
	`rm -rf '#{@install_path}'`
end

uninstall
install