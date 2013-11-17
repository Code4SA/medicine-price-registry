/**
 * medloader - code4sa.org
 */

var timer,
    delay = 500,
    animate_speed = 750;
var search_url = function(term) { return "/api/search-lite?q=" + term; }
var related_url = function(id) { return "/api/related?product=" + id };
var product_detail_url = function(id) { return "/api/detail?product=" + id };


var log = function(obj) {
    if (window.console) {
        window.console.log(obj);
    }
};

var map = {
    0 : "sep",
    1 : "schedule",
    2 : "dosage_form",
    3 : "pack_size",
    4 : "num_packs",
    5 : "is_generic"
};

var load_data = function(key, value, url, foo) {
    on_loading(key, value);
    return $.getJSON(url, function(data) {
        on_loaded(data);
        foo(data);
    });
}

Product = function(data, block) { 
    this.data = data;
    this.block = block.addClass("product");
}

Product.prototype = {

    set_name : function() {
        $(".product-name", this.block).html(this.data.name).attr('href', '#product-detail-' + this.data.id);
    },

    set_price : function() {
        $(".product-price", this.block).html(this.data.sep);
    },

    set_class_names: function() {
        // We can't assume all data returned is of type: string :(
        if (typeof this.data.is_generic == 'string') {
            var classNameGeneric = 'type_' + this.data.is_generic.toLowerCase();
            $(this.block).addClass(classNameGeneric);
        }
        if (typeof this.data.dosage_form == 'string') {
            var classNameDosageForm = 'df_' + this.data.dosage_form.toLowerCase();
            $(this.block).addClass(classNameDosageForm);
        }
    },

    build_product : function() {
        this.set_name();
        this.set_price();
        this.set_class_names();
        return this.block;
    }
}

var on_loading = function(key, value) {
    $("#search-container").addClass("js-loading");
    mixpanel.track(key, {"query": value});

}

var on_loaded = function(result) {
    $("#search-container").removeClass("js-loading");
}


var process_request = function(result) {
    $(".products .product").remove();
    $("#search-container").removeClass("js-results");
    $("#noresults").hide();
    $("#resultsheader").hide();

    var resultLength = result.length;
    if (resultLength) {
        $("#resultsheader").show();
        $("#resultsheader span").html(resultLength);
        $("#search-container").addClass("js-results");

        var $templateRow = $(".products .template");
        for (var i = 0; i < resultLength; i++) {
            var $product = new Product(result[i], $templateRow.clone().removeClass("template"));
            $('.products').append($product.build_product());
        }
        
        $('.product .product-name').on('click', function(e){
            e.preventDefault();
            add_product_detail($(this));
        });
    } else {
        $("#noresults").show();
    }
    on_loaded(result);
}

var $templateDetail = $(".products .template-panel-body");
var add_product_detail = function(elem) {
    var target_id = elem.attr('href').split('#product-detail-')[1];
    load_data("#product-detail", target_id, product_detail_url(target_id), function(data) {
        // Switch off any further event bindings to the source anchor, so that we don't get two results
        elem.off();

        // Set up the template
        var $product_detail = $templateDetail.clone().removeClass('template-panel-body');

        // Add product detail
        $(".details dd", $product_detail).each(function(idx) {
            var key = map[idx];
            $(this).html(data[key]);
        });

        // Add ingredients
        var $ingredientsList = $(".ingredients dl", $product_detail);
        var productIngredients = data.ingredients;
        var productIngredientsLength = productIngredients.length;
        for (var j = 0; j < productIngredientsLength; j++) {
            $ingredientsList.append("<dt>" + productIngredients[j].name.trim() + ":</dt>");
            $ingredientsList.append("<dd>" + productIngredients[j].strength + productIngredients[j].unit + "</dd>");
        }

        // Add related products link
        var related_link = $(".related", $product_detail);
        related_link.attr("href", "#related:" + target_id);

        // Add meta data
        $('.product-reg-number', $product_detail).html(data.regno);

        // Add product-detail ID so that we have something to target with collapse()
        $product_detail.attr('id', 'product-detail-' + target_id);
        
        // Append the detail to the product in question
        elem.parents('.product').append($product_detail);

        // Add collapse toggle to the source anchor
        elem.on("click", function(){
            $(this).collapse();
        });
    })
    .error(function() {
        // What to do on error?
        alert('There was a problem getting the details for this medicine. :(\nPlease try again later.');
    });
    
}

var entermedicine = function(e) {
    searchTerm = e.target.value;
    if (searchTerm.length < 4) return;

    var load_data = function() {
        location.hash = "search:" + searchTerm;
    }

    var reset_delay_before_requesting = function() {
        clearTimeout(timer);
        timer = setTimeout(load_data, delay);
    }

    reset_delay_before_requesting();
};

var load_medicines = function(value) {
    if (value.indexOf(":") >= 0) {
        var s = value.split(":")
        var key = s[0]
        var value = s[1]

        if (key == "#related") {
            load_data(key, value, related_url(value), process_request);
        } else if (key == "#search") {
            load_data(key, value, search_url(value), process_request);
        }

        $('html, body').animate({
            scrollTop: $("#top").offset().top
        }, animate_speed);
    }
}
