$(document).ready(function() {
  $("#medicine-search").on("keyup", function(e) {
    entermedicine(e);
  });
  $(function() {
    // Bind the event.
    $(window).on('hashchange', function() {
      load_medicines(location.hash);
    })
    // Trigger the event (useful on page load).
    load_medicines(location.hash);
  });
});

var timer, delay = 500;
var search_url = function(term) { return 'https://mpr.code4sa.org/api/v2/search-lite?q=' + term; }
var related_url = function(id) { return 'https://mpr.code4sa.org/api/v2/related?nappi=' + id };
var product_detail_url = function(id) { return 'https://mpr.code4sa.org/api/v3/detail?nappi=' + id };


var entermedicine = function(e) {
    searchTerm = e.target.value;
    if (searchTerm.length < 4) {
      $(".search-button").click(function() {
        var load_data = function() {
          location.hash = 'search:' + searchTerm;
        }
        var reset_delay_before_requesting = function() {
            clearTimeout(timer);
            timer = setTimeout(load_data, delay);
        }
        reset_delay_before_requesting();
      })
    } else {
      var load_data = function() {
        location.hash = 'search:' + searchTerm;
      }
      var reset_delay_before_requesting = function() {
          clearTimeout(timer);
          timer = setTimeout(load_data, delay);
      }
      reset_delay_before_requesting();
    }
};
var load_medicines = function(value) {
    if (value.indexOf(':') >= 0) {
        var s = value.split(':')
        var key = s[0]
        var value = s[1]
        if (key == '#related') {
            load_data(related_url(value), process_request_for_generics);
        } else if (key == '#search') {
            load_data(search_url(value), process_request);
        }
    }
}
var process_request = function(result) {
  $('.listing').hide();
  $(".search-results").css("display", "block");
  $('#results-state', res).text('results');
  $('.home-title-wrapper').css({'margin-top': 0, 'height': 0, 'opacity': 0, 'transition': 'height 0.1s ease-out, opacity 0.1s ease-out, margin-top 0.1s ease-out'});
  $('.hero-image').css({'height': 0, 'opacity': 0, 'transition': 'height 0.1s ease-out, opacity 0.1s ease-out'});
  $('#results-number', res).text(result.length);
  for (var i = 0; i < result.length; i++) {
    var datum = result[i];
    var res = $(".listing")[i]
    res = $(res)
    if (res != undefined) {
      $('.cc-listing-name', res).text(datum.name);
      $('.listing-price', res).text(datum.sep);  
      $('.generics-link', res).text(`${datum.number_of_generics} generics`);
      $('.listing-accordion-trigger', res).data('data-nappi', datum.nappi_code);     
      $('.generics-link', res).data('data-id', datum.nappi_code);     
      res.show();
      
      $('.generics-link', res).click(createClickGenericCallBack(res));
      $('.listing-accordion-trigger', res).click(createClickCallBack(res, datum.nappi_code));
      }
  }
}

function createClickGenericCallBack(res) {
  return function(event) {
    event.stopImmediatePropagation();
    event.preventDefault();
    var id = $(this).data('data-id');
    load_data(related_url(id), process_request_for_generics, res);
    location.hash = '#related:' + id;
  }
}

function createClickCallBack(res, nappiCode) {
  return function() {
    $(this).data('data-nappi', nappiCode);
    var id =  $(this).data('data-nappi');
    load_data(product_detail_url(id), function(resultObject) {
      return process_request_for_details(resultObject, res)
    });
  }
}

function createClickCallBackTwo(res, nappiCode) {
  return function() {
    $(this).data('data-nappi', nappiCode);
    var id =  $(this).data('data-nappi');
    load_data(product_detail_url(id), function(resultObject) {
      return process_request_for_details(resultObject, res)
    });
  }
}

var process_request_for_generics = function(result, listing) {
  $('.listing').hide();
  $(".search-results").css("display", "block");
  $('#results-state', res).text('generics');
  $('.listing-accordion-trigger').css({'background-color': 'rgb(241,241,241)', 'border-color': 'rgba(0,0,0,0)'});
  $('.show-more > img').css({'transform': 'translate3d(0px, 0px, 0px) scale3d(1, 1, 1) rotateX(0deg) rotateY(0deg) rotateZ(0deg) skew(0deg, 0deg)',
    'transform-style': 'preserve-3d'});
  $('.listing-accordion-content').css({'display': 'none'});
  $('.home-title-wrapper').css({'margin-top': 0, 'height': 0, 'opacity': 0, 'transition': 'height 0.1s ease-out, opacity 0.1s ease-out, margin-top 0.1s ease-out'});
  $('.hero-image').css({'height': 0, 'opacity': 0, 'transition': 'height 0.1s ease-out, opacity 0.1s ease-out'});
  if (result.length > 0) {
    $('#results-number', res).text(result.length);
  	for (var i = 0; i < result.length; i++) {
    	var datum = result[i];
      var res = $($(".listing")[i], listing)
      res = $(res)
      if (res != undefined) {
        $('.cc-listing-name', res).text(datum.name);
        $('.listing-price', res).text(datum.sep);
        $('.generics-link', res).data('data-id', datum.nappi_code);
        res.show();
        $('.listing-accordion-trigger', res).click(createClickCallBackTwo(res, datum.nappi_code));
       }
    }
  }
}


var process_request_for_details = function(resultObject, listing) {
  if (resultObject) {
    var res = $('.listing-accordion-content', listing);
    res = $(res);
    if (res != undefined) {
      if(resultObject.dosage_form !== "tablet" && resultObject.dosage_form !== "capsule") {
        $('.cost-per-unit-wrapper', res).remove();
      }
      $('.single-exit-price', res).text(resultObject.sep);
      $('.max-dispensing-fee', res).text(resultObject.dispensing_fee);
      $('.price-range', res).text(`${resultObject.min_price} - ${resultObject.max_price}`);
      if( $('.cost-per-unit', res)) {
        $('.cost-per-unit', res).text(`${resultObject.min_cost_per_unit} / ${resultObject.dosage_form} - ${resultObject.max_cost_per_unit} / ${resultObject.dosage_form}`);
      }
      $('.schedule', res).text(resultObject.schedule);
      $('.dosage-form', res).text(resultObject.dosage_form);
      $('.tablets-doses', res).text(resultObject.pack_size);
      $('.number-packs', res).text(resultObject.num_packs);
      $('.generic', res).text(resultObject.is_generic);
      $('.registration', res).text(`Registration Number: ${resultObject.regno}`);
      var ingredientsWrapper = $('.ingredients-wrapper', res);
      var $ingredient = $('.ingredient', res);
      $ingredient.hide();
      var ingredientsArray = resultObject.ingredients;
      if (ingredientsArray) {
        for(var i = 0; i < ingredientsArray.length; i++) {
          var clone = $ingredient.clone();
          clone.show();

          var $product = new Product(ingredientsArray[i], clone);
          
          $('.ingredients-wrapper div:nth-child(2)', res).remove();
          ingredientsWrapper.append($product.build_product());


          clone.find('.row-title').text(ingredientsArray[i].name)
          clone.find('.row-value').text(`${ingredientsArray[i].strength}${ingredientsArray[i].unit}`);
        }
      }
    }
  }
}

var load_data = function(url, foo) {
    return $.getJSON(url, function(data) {
        foo(data);
    });
}

Product = function(data, block) { 
  this.data = data;
  this.block = block;
}

Product.prototype = {

  set_title : function() {
      $('.row-title', this.block).html('href', '#product-detail-' + this.data.name);
  },

  set_value : function() {
      $('.row-value', this.block).html(`${this.data.strength}${this.data.unit}`);
  },

  build_product : function() {
      this.set_title();
      this.set_value();

      return this.block;
  }
}
