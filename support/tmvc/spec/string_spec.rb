require File.dirname(__FILE__) + "/spec_helper.rb"
describe String do
  it "should classify a string with a /" do
    "controllers/application_controller".classify.should == "Controllers::ApplicationController"
  end
  
  it "should classify a string" do
    "application_controller".classify.should == "ApplicationController"
  end
  
  it "should underscore a string" do
    "ApplicationController".underscore.should == "application_controller"
  end
  
  it "should underscore a string with a ::" do
    "Controllers::ApplicationController".underscore.should == "controllers/application_controller"
  end
  
  it "should constantize a string" do
    "String".constantize.should == String
  end
end