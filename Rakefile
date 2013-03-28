require 'rake/testtask'

desc "run all unit tests"
Rake::TestTask.new do |t|
	t.libs = []
	t.name = "test_all"
	t.test_files = FileList['support/test/*test.rb']
end

desc "run all unit tests and generate test coverage"
task :coverage do
	ENV['COVERAGE'] = 'true'
	Rake::Task["test_all"].execute
end

task :default => [:test_all]
