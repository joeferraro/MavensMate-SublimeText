class String
  def constantize   
    # require "logger"
    # log = Logger.new(STDOUT)
    # log.level = Logger::DEBUG
    # log.debug("CLASS IS: " + c.inspect)
    begin
      Object.module_eval("::#{self}")
    rescue     
      begin
        Object.module_eval("::#{self}", __FILE__, __LINE__)
      rescue
        begin
          Object.module_eval(self)
        rescue
          eval(self)
        end  
      end
    end
  end
  
  def underscore
    gsub(/(^|\b)[A-Z]/) { |l| l.downcase}.gsub(/[A-Z]/) { |l| "_#{l.downcase}" }.gsub("::", "/")
  end
  
  def classify
    gsub(/^[a-z]/) { |l| l.upcase}.gsub(/_[a-z]/) { |l| l[1..1].upcase}.gsub(/\b[a-z]/) {|l| l.upcase}.gsub("/", "::")
  end
end