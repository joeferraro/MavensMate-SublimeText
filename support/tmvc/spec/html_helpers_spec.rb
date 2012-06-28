require File.dirname(__FILE__) + "/spec_helper.rb"
describe HtmlHelpers do
  def resource_url(arg); arg; end
  it "should output a javascript_include_tag" do
    javascript_include_tag("prototype.js").should == ["<script src=\"prototype.js\" type=\"text/javascript\"></script>"]
  end
  
  it "should format options_for_javascript, escaping appropriately" do
    options_for_javascript(:controller => "log", :action => "index", :param => 'Grand "old" time').should == %q!{action: "index", controller: "log", param: "Grand \"old\" time"}!
  end
  
  it "should use dispatch_streaming when update_streaming is passed" do
    remote_function(:update_streaming => "iframe", :params => {:controller => "submodule", :action => "create"}, :on_complete => "alert('done')").should == 
      %q(dispatch_streaming('iframe', {params: {action: "create", controller: "submodule"}, on_complete: function() { alert('done') }}))
  end
  
  it "should, when called without an :update parameter, render link_to_remote just using dispatch " do
    link_to_remote("link", :params => {:controller => "log", :action => "index", :param => 'Grand "old" time'}).should == 
      %q(<a href="javascript:void(0)" onclick="dispatch({action: &quot;index&quot;, controller: &quot;log&quot;, param: &quot;Grand \&quot;old\&quot; time&quot;})">link</a>)
  end
  
  it "should link to javascript" do
    link_to_function("click", "alert('Hi!');").should == %q(<a href="javascript:void(0)" onclick="alert('Hi!');">click</a>)
  end
  
  it "should nest options_for_javascript" do
    options_for_javascript({:a => {:b => 1}}).should == "{a: {b: \"1\"}}"
  end
  
  it "should render a button_tag" do
    button_tag("Commit", :class => "commit_button").should == %q{<input class="commit_button" name="Commit" type="button" value="Commit" />}
  end
  
  it "should create a link with a url" do
    link_to_textmate("text", "/hello", 10).should == %q{<a href="txmt://open?url=file:///hello&line=10">text</a>}
  end
  
  it "should create a button to a remote" do
    button_to_remote("Add", :params => {:controller => "log"}).should include("button")
  end
end