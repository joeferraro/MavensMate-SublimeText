require "test/unit"
require  File.join(File.expand_path(File.dirname(__FILE__)), './test_helper.rb')

# require_relative '../../constants.rb'
require  File.join(File.expand_path(File.dirname(__FILE__)), '../../constants.rb')
include Constants

require LIB_ROOT + '/mavensmate.rb'
require LIB_ROOT + '/keychain.rb'
require LIB_ROOT + '/os.rb'

class KeyChainTests < Test::Unit::TestCase
  def test_keychain
    projectname = 'testprojectthatdoesnotexist-mm'
    pw = 'testpassword'
    KeyChain::add_generic_password(projectname, projectname, pw)
    assert_equal(pw, KeyChain::find_generic_password(projectname, projectname))
  end

  def test_keychain_no_password
    assert_equal(nil, KeyChain::find_generic_password('testaccountwhichdoesnotexist', 'testservicewhichdoesnotexist'))
  end

  def test_keychain_internet_password
    projectname = 'testprojectthatdoesnotexist-mm'
    username = 'user@exampledomainthatdoesnotexist.com'
    pw = 'testpassword'
    aname = "#{projectname}-#{username}"
    KeyChain::add_generic_password(aname, aname, pw)
    assert_equal(pw, KeyChain::find_internet_password(aname))
  end
end
