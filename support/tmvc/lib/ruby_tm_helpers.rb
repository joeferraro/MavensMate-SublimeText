# -*- encoding: UTF-8 -*0
# TextMate helpers
# Author: Tim Harper with Lead Media Partners.
# http://code.google.com/p/productivity-bundle/

# if ENV.has_key? 'TM_SUPPORT_PATH'
#   require "#{ENV["TM_SUPPORT_PATH"]}/lib/escape"
# else
#   abort(<<-PLAIN.gsub(/^\s{0,4}/, ''))
#     
#     \e[31mFail whale detected!\e[0m
#     
#     TM_SUPPORT_PATH is not set. This is probably because you are running
#     specs from outside of TextMate.
#     
#     You can set TM_SUPPORT_PATH using something like...
#     
#       export TM_SUPPORT_PATH='/Applications/TextMate.app/Contents/SharedSupport/Support'
#     
#   PLAIN
# end

public

EXIT_DISCARD = 200
EXIT_SHOW_HTML = 205
EXIT_SHOW_TOOL_TIP = 206

def exit_discard
  exit 200;
end

def exit_replace_text
  exit 201;
end

def exit_replace_document
  exit 202;
end

def exit_insert_text
  exit 203;
end

def exit_insert_snippet
  exit 204;
end

def exit_show_html
  exit 205
end

def exit_show_tool_tip
  exit 206;
end

def exit_create_new_document
  exit 207;
end

def flush; $>.flush; STDOUT.flush; end;

def tm_open(file, options = {})
  line = options[:line]
  wait = options[:wait]
  if line.nil? && /^(.+):(\d+)$/.match(file)
    file = $1
    line = $2
  end
  
  unless /^\//.match(file)
    file = File.join((ENV['TM_PROJECT_DIRECTORY'] || Dir.pwd), file)
  end
  
  args = []
  args << "-w" if wait
  args << e_sh(file)
  args << "-l #{line}" if line
  %x{"#{ENV['TM_SUPPORT_PATH']}/bin/mate" #{args * " "}}
end


def rescan_project
  %x{osascript &>/dev/null \
     -e 'tell app "SystemUIServer" to activate' \
     -e 'tell app "#{File.basename(ENV['TM_APP_PATH'], '.app')}" to activate' &
     }
end


# this method only applies when the whole document contents are sent in
def tm_expanded_selection(options = {})
  text=ENV['TM_SELECTED_TEXT'].to_s
  return text unless text.empty?
  
  options = {
    :input_type => :doc,
    :input => nil,
    :forward => /\w*/i,
    :backward => /\w*/i,
    :line_number => ENV['TM_LINE_NUMBER'].to_i,
    :col_number => ENV['TM_COLUMN_NUMBER'].to_i
  }.merge(options)
  
  col_number, line_number = options[:col_number], options[:line_number]
  
  doc = options[:input] ||= $stdin.read
  
  line = 
    case options[:input_type]
    when :doc  then doc.split("\n")[line_number - 1]
    when :line then doc
    else 
      raise "Can't handle input_type #{options[:input_type]} for tm_expanded_selection"
    end
  
  last_part = line[ (col_number - 1)..-1]
  first_part = line[ 0..col_number - 2]

  last_part.gsub!(/^(#{options[:forward]}){0,1}.*$/i) { $1 }

  first_part.reverse!
  first_part.gsub!(/^(#{options[:backward]}){0,1}.*$/i) { $1 }
  first_part.reverse!
  first_part + last_part
end



module Enumerable
  # TODO remove when 1.9 supports natively
  def map_with_index
    result = []
    each_with_index do |item, idx|
      result << yield(item, idx)
    end
    result
  end
end

class Object
  def blank?
    begin
      nil? || empty?
    rescue
    end
  end
end
