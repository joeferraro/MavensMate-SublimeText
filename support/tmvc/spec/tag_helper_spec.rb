require File.dirname(__FILE__) + "/spec_helper.rb"
describe FormatHelpers::TagHelper do
  include SpecHelpers
  
  it "should return a formatted tag in non-block notation" do
    content_tag(:script, "", :type => "javascript", :src => "prototype.js").should == "<script src=\"prototype.js\" type=\"javascript\"></script>"
  end
  
  it "should output the tag with the block contents in the middle" do
    output = capture_output do 
      content_tag(:p) do
        STDOUT << "Content"
      end
    end
    
    output.should == "<p>Content</p>"
  end
end