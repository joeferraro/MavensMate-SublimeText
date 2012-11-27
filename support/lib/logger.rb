module MavensMate

  require 'logger'
  require 'singleton'

  class Log
    include Singleton

    def error message
      logger.error message
    end

    def info message
      logger.info message
    end

    def fatal message
      logger.fatal message
    end

    def debug message
      logger.debug message
    end

    private
    def logger
      @logger ||= instantiate_logger
    end

    def instantiate_logger
      logger = nil
      begin
        logger = Logger.new(MM_WORKSPACE+'/.logs/mm.log', 5, 500000)
      rescue Exception => e
        if e.message.include?('No such file or directory')
          Dir.mkdir(MM_WORKSPACE+'/.logs')
          logger = Logger.new(MM_WORKSPACE+'/.logs/mm.log', 5, 500000)
        end
      end
      logger.level = Logger.const_get MM_LOG_LEVEL
      return logger
    end
  end
end