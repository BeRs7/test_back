/* global define, jQuery */
(function (factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory)
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('jquery'))
  } else {
    // Browser globals
    factory(jQuery)
  }
}(function ($) {
  'use strict'
  var init = function ($element, options) {
    var settings = $.extend({
      templateResult: formatData,
      templateSelection: formatData,
      closeOnSelect: false,
    }, options)
    $element.select2(settings)
  }

  function formatDataSelect (data) {
      if (!data.id) { return data.text; }
      let obj = JSON.parse(data.text);
      const selectedValue = data.selected ? ' checked ' : ''
      const img_link = obj.img ? obj.img : "";
      let $result= $(
        '<label class="card-item__product"><input class="form-check-input product-check"' + selectedValue + 'type="checkbox" value="' + data.id + `"><div class="card-img"><img width="48px" height="48px" src="${img_link}" alt="" onerror="this.style.visibility = 'hidden'"></div><p class="card-item__description">` + obj.title + '</p></label>'
      );
      return $result;
  }
  function formatDataDisplay (data) {
      if (!data.id) { return data.text; }
      const selectedValue = data.selected ? ' checked ' : ''
      const obj = JSON.parse(data.text);
      const img_link = obj.img ? obj.img : "";
      let $result= $(
        '<label class="card-item__product"><input class="form-check-input product-check"' + selectedValue + 'type="checkbox" value="' + data.id + `"><div class="card-img"><img width="48px" height="48px" src="${img_link}" alt="" onerror="this.style.visibility = 'hidden'"></div><p class="card-item__description">` + obj.title + '</p></label>'
      );
      return $result;
  }
  var initHeavy = function ($element, options) {
    console.log("INIT HEAVY!", options);
    var settings = {
      ajax: {
        data: function (params) {
          var result = {
            term: params.term,
            page: params.page,
            field_id: $element.data('field_id')
          }

          var dependentFields = $element.data('select2-dependent-fields')
          if (dependentFields) {
            dependentFields = dependentFields.trim().split(/\s+/)
            $.each(dependentFields, function (i, dependentField) {
              result[dependentField] = $('[name=' + dependentField + ']', $element.closest('form')).val()
            })
          }

          return result
        },
        processResults: function (data, page) {
          return {
            results: data.results,
            pagination: {
              more: data.more
            }
          }
        },
      },
      templateResult: formatDataSelect,
      templateSelection: formatDataDisplay,
      closeOnSelect: false,
    }

    $element.select2(settings)
  }

  $.fn.djangoSelect2 = function (options) {
    var settings = $.extend({}, options)
    $.each(this, function (i, element) {
      var $element = $(element)
      if ($element.hasClass('django-select2-heavy')) {
        initHeavy($element, settings)
      } else {
        init($element, settings)
      }
      // $element.on('select2:select', function (e) {
      //   var name = $(e.currentTarget).attr('name')
      //   $('[data-select2-dependent-fields=' + name + ']').each(function () {
      //     $(this).val('').trigger('change')
      //   })
      // })
    })
    return this
  }

  $(function () {
    $('.django-select2').djangoSelect2()
  })

  return $.fn.djangoSelect2
}))



/* global define, jQuery */
(function (factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory)
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('jquery'))
  } else {
    // Browser globals
    factory(jQuery)
  }
}(function ($) {
  'use strict'
  var init = function ($element, options) {
    $element.select2(options)
  }

  var initHeavy = function ($element, options) {
    var settings = $.extend({
      ajax: {
        data: function (params) {
          var result = {
            term: params.term,
            page: params.page,
            field_id: $element.data('field_id')
          }

          var dependentFields = $element.data('select2-dependent-fields')
          if (dependentFields) {
            dependentFields = dependentFields.trim().split(/\s+/)
            $.each(dependentFields, function (i, dependentField) {
              result[dependentField] = $('[name=' + dependentField + ']', $element.closest('form')).val()
            })
          }

          return result
        },
        processResults: function (data, page) {
          return {
            results: data.results,
            pagination: {
              more: data.more
            }
          }
        }
      }
    }, options)

    $element.select2(settings)
  }

  $.fn.djangoSelect2 = function (options) {
    var settings = $.extend({}, options)
    $.each(this, function (i, element) {
      var $element = $(element)
      if ($element.hasClass('django-select2-heavy')) {
        initHeavy($element, settings)
      } else {
        init($element, settings)
      }
      $element.on('select2:select', function (e) {
        var name = $(e.currentTarget).attr('name')
        $('[data-select2-dependent-fields=' + name + ']').each(function () {
          $(this).val('').trigger('change')
        })
      })
    })
    return this
  }

  $(function () {
    $('.dj-select2').djangoSelect2()
  })

  return $.fn.djangoSelect2
}))
