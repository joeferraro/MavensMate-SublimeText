require TMVC_ROOT + '/tmvc.rb'

%w[auto_load].each do |filename|
  require "#{LIB_ROOT}/#{filename}.rb"
end 

#require ROOT + '/lib/escape.rb'
require 'shellwords'
require 'set'
 
def shorten(path, base = nil)
  return if path.blank?
  base = base.gsub(/\/$/, "") if base
  project_path = 
  home_path = ENV['HOME']
  case
  when base && path =~ /^#{Regexp.escape base}\/(.+)$/
    $1
  when base && path =~ /^#{Regexp.escape base}\/?$/
    "./"
  when path == project_path
    File.basename(path)
  when ENV['TM_PROJECT_DIRECTORY'] && path =~ /^#{Regexp.escape ENV['TM_PROJECT_DIRECTORY']}\/(.+)$/
    $1
  when ENV['HOME'] && path =~ /^#{Regexp.escape ENV['HOME']}\/(.+)$/
    '~/' + $1
  else
    path
  end
end

class Module
  def alias_method_chain(target, feature)
    # Strip out punctuation on predicates or bang methods since
    # e.g. target?_without_feature is not a valid method name.
    aliased_target, punctuation = target.to_s.sub(/([?!=])$/, ''), $1
    yield(aliased_target, punctuation) if block_given?
  
    with_method, without_method = "#{aliased_target}_with_#{feature}#{punctuation}", "#{aliased_target}_without_#{feature}#{punctuation}"
  
    alias_method without_method, target
    alias_method target, with_method
  
    case
      when public_method_defined?(without_method)
        public target
      when protected_method_defined?(without_method)
        protected target
      when private_method_defined?(without_method)
        private target
    end
  end
end

class Array
  def with_this_at_front(front_matcher)
    case front_matcher
    when Array
      (front_matcher + self).uniq
    when String, Symbol
      ([front_matcher] + self).uniq
    when Regexp
      (self.grep(front_matcher) + self).uniq
    else
      self
    end
  end
end