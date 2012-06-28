require File.dirname(__FILE__) + "/spec_helper.rb"

describe Hash do
  it "should stringify_keys" do
    h = {:author => 1, "date" => 1}
    h.stringify_keys!
    h.keys.sort.should == ["author", "date"]
  end
  
  it "should filter the keys" do
    {:a => 1, :b => 2}.filter(:a).should == {:a => 1}
  end
  
  it "should reject specified keys" do
    {:a => 1, :b => 2}.reject(:b).should == {:a => 1}
  end
end