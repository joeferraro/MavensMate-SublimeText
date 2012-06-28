module FormatHelpers
  module TagHelper
    # Adapted from RubyOnRails
    BOOLEAN_ATTRIBUTES = %w(disabled readonly multiple)
    SELF_CLOSABLE_TAGS = %w(img br hr)
    def content_tag_string(name, content = nil, options = {}, escape = true, close = true)
      if content || ! SELF_CLOSABLE_TAGS.include?(name.to_s)
        "#{content_tag_string_open(name, options)}#{content}#{content_tag_string_close(name)}"
      else
        content_tag_string_open(name, options, true, :self_closing => true)
      end
    end
    
    def content_tag_string_open(name, options, escape = true, self_closing = false)
      tag_option_string = tag_options(options, escape) if options
      "<#{name}#{tag_option_string}#{self_closing ? ' /' : ''}>"
    end
    
    def content_tag_string_close(name)
      "</#{name}>"
    end
    
    def content_tag(name, content_or_options_with_block = nil, options = nil, escape = true, &block)
      if block_given?
        options = content_or_options_with_block if content_or_options_with_block.is_a?(Hash)
        STDOUT << content_tag_string_open(name, options, escape)
        yield
        STDOUT << content_tag_string_close(name)
      else
        if content_or_options_with_block.is_a?(Hash)
          content = nil
          options = content_or_options_with_block
        else
          content = content_or_options_with_block.to_s
        end
        content_tag_string(name, content, options, escape)
      end
    end
    
    def tag_options(options, escape = true)
      unless options.blank?
        attrs = []
        if escape
          options.each do |key, value|
            next unless value
            key = key.to_s
            value = BOOLEAN_ATTRIBUTES.include?(key) ? key : escape_once(value)
            attrs << %(#{key}="#{value}")
          end
        else
          attrs = options.map { |key, value| %(#{key}="#{value}") }
        end
        " #{attrs.sort * ' '}" unless attrs.empty?
      end
    end
    
    def htmlize_attr(str)
      str.to_s.gsub(/&/, "&amp;").gsub(/"/, "&quot;").gsub("<", "&lt;").gsub(">", "&gt;")
    end

    alias :escape_once :htmlize_attr
    
  end
end