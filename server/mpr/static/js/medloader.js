/**
 * medloader - code4sa.org
 */

var log = function(obj) {
    if (window.console) {
        window.console.log(obj);
    }
};

var map = {
    // 0 was name
    0 : "sep",
    1 : "regno",
    2 : "schedule",
    3 : "dosage_form",
    4 : "pack_size",
    5 : "num_packs",
    6 : "is_generic"
};

var on_loading = function() {
    $("#search-container").addClass("js-loading");
}

var on_loaded = function() {
    $("#search-container").removeClass("js-loading");
}

Product = function(data, block) { 
    this.data = data;
    this.block = block.addClass("product");
}

Product.prototype = {

    set_name : function() {
        $(".product-name", this.block).html(this.data.name);
    },

    add_details : function() {
        var data = this.data;
        $(".details dd", this.block).each(function(idx) {
            var key = map[idx];
            $(this).html(data[key]);
        });
    },

    add_ingredients : function() {
        this.block.find(".ingredients dt, .ingredients dd").remove();
        var $ingredientsList = $(".ingredients dl", this.block);
        var productIngredients = this.data.ingredients;
        var productIngredientsLength = productIngredients.length;
        for (var j = 0; j < productIngredientsLength; j++) {
            $ingredientsList.append("<dt>" + productIngredients[j].name + ":</dt>");
            $ingredientsList.append("<dd>" + productIngredients[j].strength + productIngredients[j].unit + "</dd>");
        }
    },

    build_product : function() {
        this.set_name();
        this.add_details();
        this.add_ingredients();
        return this.block;
    }
}

var process_request = function(result) {
    $(".products .product").remove();
    $("#search-container").removeClass("js-results");

    var resultLength = result.length;
    if (resultLength) {
        $("#resultsheader span").html(resultLength);
        $("#search-container").addClass("js-results");

        var $templateRow = $(".products .template");

        for (var i = 0; i < resultLength; i++) {
            $product = new Product(result[i], $templateRow.clone().removeClass("template"));
            $product.build_product();

            $('.products').append($product.build_product());
        }
    }
    on_loaded();
}

var timer;
var searchTerm = '';
var delay = 500;
var api_url = "/api/search";

var entermedicine = function(e) {
    searchTerm = e.target.value;

    var load_data = function() {
        var query = api_url + "?q=" + searchTerm;
        on_loading();
        $.getJSON(query, process_request);
    }

    var reset_delay_before_requesting = function() {
        clearTimeout(timer);
        timer = setTimeout(load_data, delay);
    }

    reset_delay_before_requesting();
};
