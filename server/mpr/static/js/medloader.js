/**
 * medloader - code4sa.org
 */

var timer;
var delay = 500;
var animate_speed = 750;
var search_url = function(term) { return "/api/search?q=" + term; }
var related_url = function(id) { return "/api/related?product=" + id };


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

    add_related : function() {
        var related_link = $(".related", this.block);
        id = this.data.id;
        related_link.attr("href", "#related:" + id);
    },

    build_product : function() {
        this.set_name();
        this.add_details();
        this.add_ingredients();
        this.add_related();
        return this.block;
    }
}

var on_loading = function(key, value) {
    $("#search-container").addClass("js-loading");
    mixpanel.track(key, {"query": value});

    $('html, body').animate({
        scrollTop: $("#top").offset().top
    }, animate_speed);
}

var on_loaded = function(result) {
    $("#search-container").removeClass("js-loading");
}


var process_request = function(result) {
    $(".products .product").remove();
    $("#search-container").removeClass("js-results");
    $("#noresults").css("display", "none")
    $("#resultsheader").css("display", "none")

    var resultLength = result.length;
    if (resultLength) {
        $("#resultsheader").css("display", "block")
        $("#resultsheader span").html(resultLength);
        $("#search-container").addClass("js-results");

        var $templateRow = $(".products .template");

        for (var i = 0; i < resultLength; i++) {
            $product = new Product(result[i], $templateRow.clone().removeClass("template"));
            $product.build_product();

            $('.products').append($product.build_product());
        }
    } else {
        $("#noresults").css("display", "block")
    }
    on_loaded(result);
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

var handlehash = function(value) {
    if (value.indexOf(":") >= 0) {
        var s = value.split(":")
        var key = s[0]
        var value = s[1]

        if (key == "#related") {
            on_loading(key, value);
            $.getJSON(related_url(value), process_request);
        } else if (key == "#search") {
            on_loading(key, value);
            $.getJSON(search_url(value), process_request);
        }
    }
}
