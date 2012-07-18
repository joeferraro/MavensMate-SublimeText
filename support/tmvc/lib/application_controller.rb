require 'stringio'
require 'thread'

class StringIO
  def retrieve_and_clear
    s = self.string
    self.string = ""
    s
  end
end

class ApplicationController
  include ApplicationHelper
  attr_accessor :params
  class << self
    attr_writer :layouts_conditions
    
    def filters
      @filters ||= {:before => [], :after => []}
    end
    
    def before_filter(method)
      filters[:before] << [method, nil]
    end
    
    def layouts_conditions
      @layouts_conditions ||= []
    end
    
    def layout(layout, conditions = {})
      layout = "/layouts/#{layout}" if layout && !layout.to_s.include?("/")
      raise "bad params!" unless conditions.is_a?(Hash)
      layouts_conditions << [layout, conditions]
    end
    
    def layout_for_action(action)
      return "/layouts/application" if layouts_conditions.empty?
      
      layouts_conditions.each do |layout, condition|
        if condition[:except]
          next if [condition[:except]].flatten.map{|c| c.to_s}.include?(action.to_s)
        end
        
        if condition[:only]
          next unless [condition[:only]].flatten.map{|c| c.to_s}.include?(action.to_s)
        end
        
        return layout
      end
      nil
    end
  end
  
  def initialize
    @output_buffer = StringIO.new
    @params = {}
  end
  
  def puts(*args)
    @output_buffer.puts(*args)
  end
  
  def flush
    return if @capturing
    start_layout
    Object::STDOUT << @output_buffer.string
    Object::flush
    @output_buffer.truncate(0)
  end
  
  def start_layout
    return if @layout_rendered
    @layout_rendered = true
    this_actions_layout = self.class.layout_for_action(params[:action])
    return unless this_actions_layout
    
    current_body_output = @output_buffer.retrieve_and_clear
    render(this_actions_layout) { @layout_text_begin = @output_buffer.retrieve_and_clear }
    @layout_text_end = @output_buffer.retrieve_and_clear
    @output_buffer << @layout_text_begin << current_body_output
    @layout_text_begin = nil
  end
  
  def end_layout
    return unless @layout_rendered && @layout_text_end
    @output_buffer << @layout_text_end
    @layout_text_end = nil
  end
  
  def with_filters(&block)
    self.class.filters[:before].each do |method, options|
      return false unless send(method)
    end
    yield
    self.class.filters[:after].each do |method, options|
      return false unless send(method)
    end
  end
  
  def call(action, _params = {})
    at_exit {       
      flush       
    }
    self.params = _params
    params[:action] = action.to_s
    @output_buffer = params.delete(:__output_buffer__) if params[:__output_buffer__]
    with_filters { send(action) }
    flush
    end_layout
    flush
  end
  
  def self.call(action, params = {})
    new.call(action, params)
  end
  
  def render(__name__, __options__ = {}, &block)
    __name__ = "#{__name__}.html.erb" unless __name__.include?(".")
    __sub_dir__ = __name__.include?("/") ? "" : self.class.template_root
    __template_path__ = File.join( VIEWS_ROOT, __sub_dir__, __name__)
    ___template___ = File.read( __template_path__)
    
    __binding__ = binding
    if __options__[:locals]
      __v__ = __options__[:locals].values
      __binding__.send(:eval, __options__[:locals].keys * ", " + ", = *__v__")
    end
    
    __erb__ = ERBStdout.new(___template___, nil, "-", "@output_buffer")
    __erb__.filename = __template_path__
    __erb__.run(__binding__)         
  end

  def render_to_string(__name__, __options__ = {}, &block)
    __name__ = "#{__name__}.html.erb" unless __name__.include?(".")
    __sub_dir__ = __name__.include?("/") ? "" : self.class.template_root
    __template_path__ = File.join( VIEWS_ROOT, __sub_dir__, __name__)
    ___template___ = ERB.new File.read( __template_path__), nil, "-"

    __binding__ = binding
    if __options__[:locals]
      __v__ = __options__[:locals].values
      __binding__.send(:eval, __options__[:locals].keys * ", " + ", = *__v__")
    end

    __erb__ = ___template___.result(__binding__)        
    #puts "erb is: " + __erb__
    #__erb__ = ERBStdout.new(___template___, nil, "-", "@output_buffer")
    #__erb__.filename = __template_path__
    #__erb__.run(__binding__)  
    return __erb__       
  end

  
  def render_component(_params = {})
    flush
    _params[:controller] ||= params[:controller]
    dispatch(_params.merge(:layout => false, :__output_buffer__  => @output_buffer))
  end
  
  def self.template_root
    to_s.gsub("::", "/").underscore.gsub(/_controller$/, "")
  end
  
  def content_for(name, &block)
    var_name = "@content_for_#{name}"
    content = instance_variable_get(var_name) || ""
    @capturing = true
    previous_content = @output_buffer.retrieve_and_clear
    yield
    content << @output_buffer.retrieve_and_clear
    @output_buffer << previous_content
    instance_variable_set(var_name, content)
    @capturing = false
    ""
  end
  
  def output_discard
    $exit_status = EXIT_DISCARD
  end
  
  def output_show_html
    $exit_status = EXIT_SHOW_HTML
  end
  
  def output_show_tool_tip
    $exit_status = EXIT_SHOW_TOOL_TIP
  end
end
