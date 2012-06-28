module HtmlHelpers
  include ERB::Util
  
  def path_for(default_path, path)
    if path.include?("/")
      path
    else
      default_path(path)
    end
  end
    
protected  
  def resource_url(filename)
    "file://#{SUPPORT}/resource/#{filename}"
  end
  
  def select_box(name, select_options = [], options = {})
    options[:name] ||= name
    options[:id] ||= name
    # puts select_options.inspect
    <<-EOF
      <select name='#{options[:name]}' id='#{options[:id]}' onchange="#{options[:onchange]}" style='width:100%'>
        #{select_options}
      </select>
    EOF
  end

  def options_for_select(select_options = [], selected_value = nil)
    output = ""
  
    select_options.each do |name, val|
      selected = (val == selected_value) ? "selected='true'" : ""
      output << "<option value='#{val}' #{selected}>#{htmlize(name)}</option>"
    end
  
    output
  end
  
  def make_non_breaking(output)
    htmlize(output.to_s.strip).gsub(" ", "&nbsp;")
  end
  
  
  def e_js(str)
    str.to_s.gsub(/"/, '\"').gsub("\n", '\n')
  end
  
  def javascript_include_tag(*params)
    file_names = []
    params = params.map {|p| p.include?(".js") ? p : "#{p}.js"}
    params.map do |p|
      content_tag :script, "", :type => "text/javascript", :src => resource_url("js/#{p}")
    end * ""
  end
  
  def style_include_tag(*params)
    file_names = []
    params = params.map {|p| p.include?(".css") ? p : "#{p}.css"}
    params.map do |p|
      content_tag :link, "", :type => "text/css", :href => resource_url("css/#{p}"), :rel => "stylesheet"
    end * ""
  end 
  
  def options_for_javascript(options = {})
    output = options.map { |key, value| "#{key}: " + (value.is_a?(Hash) ? options_for_javascript(value) : "\"#{e_js(value)}\"") }
    "{" + (output.sort * ", ") + "}"
  end
  
  def remote_function(options = {})
    case
    when options[:update]
      "$('#{options[:update]}').update(dispatch(#{options_for_javascript(options[:params])}))" 
    when target = options[:update_streaming]
      other_options = ""
      other_options << ", on_complete: function() { #{options[:on_complete]} }" if options[:on_complete]

      "dispatch_streaming('#{target}', {params: #{options_for_javascript(options[:params])}#{other_options}})" 
    else
      "dispatch(#{options_for_javascript(options[:params])})"
    end
  end
  
  def link_to_remote(name, options = {})
    link_to_function(name, remote_function(options))
  end
  
  def link_to_function(name, js, html_options = {})
    content_tag(:a, name, {:href => "javascript:void(0)", :onclick => js}.merge(html_options))
  end
  
  def button_tag(value, options = {})
    content_tag(:input, {:type => "button", :name => value, :value => value }.merge(options))
  end
  
  def link_to_textmate(name, file, line = nil)  
    content_tag(:a, name, :href => "txmt://open?url=file://#{e_url file}&line=#{line}")
  end
  
  def button_to_remote(name, options = {}, html_options = {})
    button_tag(name, {:onclick => remote_function(options)}.merge(html_options))
  end
  
  def link_to_mate(name, file)
    link_to_function(name, "exec('mate', [\"#{e_sh(file)}\"])")
  end
  
  include FormatHelpers::TagHelper
end

