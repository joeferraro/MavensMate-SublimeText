$dispatch_loaded = true
require File.dirname(__FILE__) + "/environment.rb"

dispatch(ARGV) if $0 == __FILE__ && ! $dispatched
