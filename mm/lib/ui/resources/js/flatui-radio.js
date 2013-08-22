/* =============================================================
 * flatui-radio.js v0.0.1
 * ============================================================ */

!function ($) {

 /* RADIO PUBLIC CLASS DEFINITION
  * ============================== */

  var Radio = function (element, options) {
    this.init(element, options);
  }

  Radio.prototype.setState = function () {    
    var d = 'disabled'
      , ch = 'checked' 
      , $el = this.$element
      , $parent = $el.closest('.radio');
      
      $el['prop'](d) && $parent.addClass(d);   
      $el['prop'](ch) && $parent.addClass(ch);
  }

  Radio.prototype.toggle = function () {    
    var d = 'disabled'
      , ch = 'checked'
      , $el = this.$element
      , checked = $el['prop'](ch)
      , $parent = this.$element.closest('.radio')      
      , $parentWrap = $el.closest('form').length ? $el.closest('form') : $el.closest('body')
      , $elemGroup = $parentWrap.find(':radio[name="' + $el['attr']('name') + '"]');
      
      $elemGroup.each(function () {
        var $el = $(this)
          , $parent = $(this).closest('.radio');
          
          !$el['prop'](d) && $parent.removeClass('checked') && $el.attr('checked', false);
      });
    
      !$el['prop'](d) && $parent.addClass(ch) && $el.attr(ch, true); 
      $el.trigger("toogle");      
  }
  
  Radio.prototype.init = function (element, options) {      
    var $el = this.$element = $(element)
    
    this.options = $.extend({}, $.fn.radio.defaults, options);
      
    $el.before(this.options.template);
    
    this.setState();  
    
    return this
  }


 /* RADIO PLUGIN DEFINITION
  * ======================== */

  var old = $.fn.radio

  $.fn.radio = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('radio')
        , options = $.extend({}, $.fn.radio.defaults, $this.data(), typeof option == 'object' && option);
      if (!data) $this.data('radio', (data = new Radio(this, options)));
      if (option == 'toggle') data.toggle()
      else if (option) data.setState(); 
    });
  }
  
  $.fn.radio.defaults = {
    template: '<span class="icons"><span class="first-icon fui-radio-unchecked"></span><span class="second-icon fui-radio-checked"></span></span>'
  }

  $.fn.radio.Constructor = Radio


 /* RADIO NO CONFLICT
  * ================== */

  $.fn.radio.noConflict = function () {
    $.fn.radio = old;
    return this;
  }


 /* RADIO DATA-API
  * =============== */

  $(document).on('click.radio.data-api', '[data-toggle^=radio], .radio', function (e) {
    var $radio = $(e.target);
    e && e.preventDefault() && e.stopPropagation();
    if (!$radio.hasClass('radio')) $radio = $radio.closest('.radio');
    $radio.find(':radio').radio('toggle');
  });

}(window.jQuery);