# Simple interface for reading and writing Internet passwords to
# the KeyChain.

module KeyChain
  class << self
    def add_internet_password(user, proto, host, path, pass)
      %x{security add-internet-password -a "#{user}" -s "#{host}" -r "#{proto}" -p "#{path}" -w "#{pass}"}
    end
    def find_internet_password(aname)
      result = %x{security find-generic-password -ga "#{aname}" 2>&1 >/dev/null}
      result =~ /^password: "(.*)"$/ ? $1 : nil
    end
  end
end
