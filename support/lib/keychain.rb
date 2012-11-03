# Simple interface for reading and writing Internet passwords to
# the KeyChain.
require SUPPORT + '/lib/os.rb'

module KeyChain
  class << self
    def add_generic_password(account, service, password)
      if MavensMate::OS.mac? then
        %x{security add-generic-password -a #{account} -s \"MavensMate: #{service}\" -w #{password} -U}
      elsif MavensMate::OS.linux? then
        %x(gkeyring -s -p account_name="#{account}" -n "MavensMate: #{service}" -w #{password})
      end
    end
    def find_generic_password(account, service)
      if MavensMate::OS.mac? then
        result = %x{security find-generic-password -ga "#{account}" -s \"MavensMate: #{service}\" 2>&1 >/dev/null}
        result =~ /^password: "(.*)"$/ ? $1 : nil
      elsif MavensMate::OS.linux? then
        pw = %x(gkeyring -p account_name="#{account}" -n "MavensMate: #{service}" -o "secret" 2>/dev/null).strip
      end
    end
    def add_internet_password(user, proto, host, path, pass)
      if MavensMate::OS.mac? then
        %x{security add-internet-password -a "#{user}" -s "#{host}" -r "#{proto}" -p "#{path}" -w "#{pass}"}
      elsif MavensMate::OS.linux? then
        %x(gkeyring -s -p account_name="#{user}" -n "#{host}" -w #{pass})
      end
    end
    def find_internet_password(aname)
      if MavensMate::OS.mac? then
        result = %x{security find-generic-password -ga "#{aname}" 2>&1 >/dev/null}
        result =~ /^password: "(.*)"$/ ? $1 : nil
      elsif MavensMate::OS.linux? then
        pw = %x(gkeyring -p account_name="#{aname}" -n "MavensMate: #{aname}" -o "secret" 2>/dev/null).strip
      end
    end
  end
end
