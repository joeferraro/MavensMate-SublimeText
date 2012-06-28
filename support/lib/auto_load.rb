module AutoLoad
  def const_missing(name)
    name = name.to_s
    #puts "const_missing name: " + name
    case name
    when /Controller$/
      path = "/app/controllers"
    when /Helper$/
      path = "/app/helpers"
    else
      return super
    end
    
    @last_try||=nil
    super if @last_try==name
    @last_try = name
  
    file = File.join(ROOT, path, name.to_s.underscore + ".rb")
    require file
    name.constantize
    klass = const_get(name)
  rescue LoadError
    super
  end
end

Object.send :extend, AutoLoad