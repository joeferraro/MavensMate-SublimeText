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

@install_path = File.expand_path("~/Library/Application Support/Sublime Text 2/Packages/MavensMate")

def install
	if OS.windows?
		#future functionality
	elsif OS.mac?
		`git clone git://github.com/joeferraro/MavensMate-SublimeText.git '#{@install_path}'`
	elsif OS.linux?
		#future functionality
	end
end

def uninstall
	`rm -rf '#{@install_path}'`
end

uninstall
install