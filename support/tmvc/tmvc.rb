#TMVC_ROOT = File.dirname(__FILE__)
# CONTROLLERS_ROOT = ROOT + "/app/controllers"
# HELPERS_ROOT = ROOT + '/app/helpers' 
# VIEWS_ROOT = ROOT + "/app/views"

%w[string hash erb_stdout ruby_tm_helpers format_helpers/tag_helper html_helpers application_helper application_controller].each do |filename|
  require TMVC_ROOT + "/lib/#{filename}.rb"
end

at_exit { 
  if $exit_status
    exit $exit_status
  end
}

module TMVC
  class << self
    attr_accessor :catch_exceptions
    def dispatch_streaming(params = {})
      require 'socket'
      streaming = params.delete(:streaming)
      try_count = 0
      port = 0
      begin
        port = 9999 + try_count
        server = TCPServer.new('', port)
      rescue => e
        try_count += 1
        retry if try_count < 10
        raise "Couldn't find a port!"
      end

      pid = fork do
        socket = server.accept
        Object.send :remove_const, 'STDOUT'
        Object.const_set("STDOUT", socket)
        dispatch_normal(params)
      end
      puts "#{port},#{pid}"
      flush
    end

    def dispatch_normal(params = {})
      # puts "hi"
      # return false
      begin
        raise "must supply a controller to use!" unless controller = params[:controller]
        params[:action] ||= "index"
        controller_class = "#{controller}_controller".classify.constantize
        
        #here's where html is generated
        controller_class.call(params[:action], params) 
        
      rescue => e        
        raise e unless $dont_catch_exceptions
        puts htmlize($!)
        puts htmlize($!.backtrace)
      end
    end

    def dispatch(params = {})
      $dispatched = true
      params = parse_dispatch_args(ARGV) if params.is_a?(Array)
      if debug_mode
        require 'logger'
        Logger.new(ROOT + "/log/dispatch.log").warn(params.inspect)
      end
      if params[:streaming]
        dispatch_streaming(params) 
      else
        dispatch_normal(params)
      end
    end

    def parse_dispatch_args(args = [])
      params = args.inject({}) do |hash, arg|
        parts = arg.scan(/(.+?)=(.+)/m).flatten
        next hash if parts.empty?
        key = parts.first.to_sym
        value = parts.last
        hash[key] = value
        hash
      end
    end
  end
  self.catch_exceptions = true
end

def debug_mode
  return $debug_mode unless $debug_mode.nil?
  $debug_mode = File.exist?(File.join(ROOT, "/DEBUG"))
end
def dispatch(params = {}); TMVC.dispatch(params); end