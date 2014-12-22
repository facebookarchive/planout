require_relative 'experiment'

module PlanOut
  class SimpleExperiment < Experiment
    def configure_logger
      @logger = Logger.new(STDOUT)
      #@loger.level = Logger::WARN
      @logger.formatter = proc do |severity, datetime, progname, msg|
        "logged data: #{msg}\n"
      end
    end

    def log(data)
      @logger.info(JSON.dump(data))
    end
  end
end
