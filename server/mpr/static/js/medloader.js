var map = {
    // 0 was name
    0 : "sep",
    1 : "regno",
    2 : "schedule",
    3 : "dosage_form",
    4 : "pack_size",
    5 : "num_packs",
    6 : "is_generic",
}
var process_ingredient = function(js) {

    $("#search-container").toggleClass("js-loading");
    d3.selectAll(".template").classed("template", true);
    $(".products .product").remove();

    if (js.length > 0) {
        $("#resultsheader").show();
        $('.products').removeClass("template");

        var row = d3.select(".products .template")[0][0];

        d3.selectAll(".products").selectAll("div.product")
            .data(js)
            .enter()
            .append("div")
            .classed("product", true)
            .html(function(el, i) {
                return row.innerHTML;
            })
            .each(function(el, i) {
                var data = el;
                d3.select(this).selectAll(".product-name").html(function(){
                    return data.name;
                });
                d3.select(this).selectAll(".details dd").text(function(el, i) {
                    var key = map[i];
                    return data[key];
                })
                d3.select(this).selectAll(".ingredients dt, .ingredients dd").remove()
                d3.select(this).selectAll(".ingredients").selectAll("div")
                    .data(data.ingredients) 
                    .enter()
                    .append("div")
                    .html(function(el, i) {
                        return "<dt>" + el.name + ":</dt><dd>" + el.strength + el.unit + "</dd>"
                    })
                // need to find a better way to generate the ingredient definition list
            })
        
    }
}

var timer;
var entermedicine = function(el) {
    var text = d3.event.target.value;

    var load = function() {
        $("#search-container").toggleClass("js-loading");
        $("#resultsheader").hide();
        d3.json("/api/?ingredient=" + text, process_ingredient)
    }

    clearTimeout(timer)
    timer = setTimeout(load, 500);

}
