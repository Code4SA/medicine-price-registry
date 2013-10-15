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
    6 : "is_generic",
};

var process_ingredient = function(result) {
    //log(result);
    $("#search-container").removeClass("js-results");
    $(".products .product").remove();

    var resultLength = result.length;
    if (resultLength) {
        $("#resultsheader span").html(resultLength);
        $("#search-container").addClass("js-results");

        var $templateRow = $(".products .template");

        for (var i=0; i<resultLength; i++){
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
            $product.find(".ingredients dt, .ingredients dd").remove()
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
var entermedicine = function(e) {
    searchTerm = e.target.value;
    var load = function(){
        $("#search-container").addClass("js-loading");
        $.getJSON("/api/search?q=" + searchTerm, process_ingredient);
    }
    clearTimeout(timer);
    timer = setTimeout(load, 500);
}
