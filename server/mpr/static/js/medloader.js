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

var loading_data = function() {
    $("#search-container").addClass("js-loading");
}

var loaded_data = function() {
    $("#search-container").removeClass("js-results");
}

var process_request = function(result) {
    //log(result);
    loaded_data();
    $(".products .product").remove();

    var resultLength = result.length;
    if (resultLength) {
        $("#resultsheader span").html(resultLength);
        $("#search-container").addClass("js-results");

        var $templateRow = $(".products .template");

        for (var i = 0; i < resultLength; i++) {
            var $product = $templateRow.clone().removeClass('template').addClass('product');        
            var productItemData = result[i];

            // Set the product name
            $(".product-name", $product).html(productItemData.name);

            // Add the product details to each product item
            $(".details dd", $product).each(function(idx){
                var key = map[idx];
                $(this).html(productItemData[key]);
            });

            // Add ingredients to each product item
            $product.find(".ingredients dt, .ingredients dd").remove();
            var $ingredientsList = $(".ingredients dl", $product);
            var productIngredients = productItemData.ingredients;
            var productIngredientsLength = productIngredients.length;
            for (var j=0; j<productIngredientsLength; j++) {
                $ingredientsList.append("<dt>" + productIngredients[j].name + ":</dt>");
                $ingredientsList.append("<dd>" + productIngredients[j].strength + productIngredients[j].unit + "</dd>");
            }

            $('.products').append($product);
        }
    }
    $("#search-container").removeClass("js-loading");
}
var timer;
var searchTerm = '';
var delay = 500;
var api_url = "/api/search";

var entermedicine = function(e) {
    searchTerm = e.target.value;

    var load_data = function() {
        var query = api_url + "?q=" + searchTerm;
        loading_data();
        $.getJSON(query, process_request);
    }

    var reset_delay_before_requesting = function() {
        clearTimeout(timer);
        timer = setTimeout(load_data, delay);
    }

    reset_delay_before_requesting();
};
