module SpecHelpers
  PUTS_CAPTURE_CLASSES = []
  def fixture_file(filename)
    File.read("#{FIXTURES_DIR}/#{filename}")
  end
  
  def set_constant_forced(klass, constant_name, constant)
    klass.class_eval do
      remove_const(constant_name) if const_defined?(constant_name)
      const_set(constant_name, constant)
    end
  end
  
  def capture_output(&block)
    old_stdout = Object::STDOUT
    io_stream = StringIO.new
    begin 
      set_constant_forced(Object, "STDOUT", io_stream)
      PUTS_CAPTURE_CLASSES.each do |klass| 
        klass.class_eval do 
          def puts(*args)
          args.each{ |arg| Object::STDOUT.puts arg}
          end
        end
      end
      yield
    ensure
      set_constant_forced(Object, "STDOUT", old_stdout)
    end
    io_stream.rewind
    io_stream.read
  end
  
  
  def branch_stub(options = {})
    branch = stub("branch", options)
    [:name, :tracking_branch_name].each do |key|
      next unless options[key]
      branch.stub!(key).with(:long).and_return(options[key])
      branch.stub!(key).with().and_return(options[key].gsub(/refs\/(heads|remotes)\//, ""))
    end
    if options.has_key?(:remote)
      branch.stub!(:remote).and_return(stub("remote", :name => options[:remote]))
      branch.stub!(:remote_name).and_return(options[:remote])
    end
    branch
  end
  
  def stub_current_branch(git, options = {})
    git.branch.stub!(:current).and_return(branch_stub(options))
    git.branch.stub!(:current_name).with(:long).and_return(git.branch.current.name(:long))
    git.branch.stub!(:current_name).with().and_return(git.branch.current.name)
  end
end
