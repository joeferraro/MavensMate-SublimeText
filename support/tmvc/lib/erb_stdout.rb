require 'erb'

class ERBStdout < ERB
  def set_eoutvar(compiler, eoutvar = 'STDOUT')
    compiler.put_cmd = "#{eoutvar} << "
    compiler.insert_cmd = "#{eoutvar} << " if compiler.respond_to?(:insert_cmd)
    compiler.pre_cmd = "#{eoutvar}.flush"
    compiler.post_cmd = "#{eoutvar}.flush; ''"
    
    if RUBY_VERSION >= "1.9" 
      # in Ruby1.9.x, ERB wants pre_cmd/post_cmd wrapped in Array
      compiler.pre_cmd = [compiler.pre_cmd]
      compiler.post_cmd = [compiler.post_cmd]
    end
  end
  
  def run(b=TOPLEVEL_BINDING)
    self.result(b)
  end
end

