require "test/unit"
require  File.join(File.expand_path(File.dirname(__FILE__)), './test_helper.rb')

# require_relative '../../constants.rb'
require  File.join(File.expand_path(File.dirname(__FILE__)), '../../constants.rb')
include Constants

require LIB_ROOT + '/mavensmate.rb'
require LIB_ROOT + '/lsof.rb'
require LIB_ROOT + '/local_server_thin.rb'


class LocalServerTests < Test::Unit::TestCase
    def setup
        @RUBY = MM_USER_CONFIG['mm_ruby'] || MM_DEFAULT_CONFIG['mm_ruby'] || 'ruby'
        start_server
    end

    def teardown
        stop_server
    end

    def test_start_stop
        assert Lsof::running? 7777
        stop_server
        assert !(Lsof::running? 7777)
        stop_server
        assert !(Lsof::running? 7777)
        start_server
        assert Lsof::running? 7777
    end

    def test_respond
        body_contents = "Test Body Contents"
        content_type = "Test Content Type"
        response = MavensMate::LocalServerThin.respond(body_contents, content_type)
        assert response.include?(200), "response code should be 200"
        assert response.include?(body_contents), "response should contain body contents"
        assert response.to_s.include?(content_type), "response should have correct content type"
    end

    def test_respond_with_async_request_id
        id = 42
        response = MavensMate::LocalServerThin.respond_with_async_request_id(id)
        assert response.is_a?(Array), "response should be an array"
        assert response.to_s.include?(id.to_s), "response should contain the correct request id"
    end

    def test_prepare_response
        options = {
            :status  => "test status",
            :success => "test success",
            :id      => "test id",
            :foo     => "foo"
        }
        response = MavensMate::LocalServerThin.prepare_response(options)
        assert response.is_a?(String)
        assert response.include?(options[:status]), "response should include correct status"
        assert response.include?(options[:success]), "response should include correct success"
        assert response.include?(options[:id]), "response should include correct id"
        assert !response.include?(options[:foo]), "response should not include invalid options"
    end

    private

    def start_server
        sin, sout = IO.pipe
        pid = Process.spawn("#{@RUBY} -r '#{LIB_ROOT}/local_server_thin.rb' -e 'MavensMate::LocalServerThin.start'", :out => sout)
        Process.detach pid
        sleep 1
        sin.close
        sout.close
    end

    def stop_server
        MavensMate::LocalServerThin::stop
        sleep 1
    end
end
