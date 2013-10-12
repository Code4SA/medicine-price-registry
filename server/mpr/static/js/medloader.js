var map = {
    0 : "name",
    1 : "sep",
    2 : "regno",
    3 : "schedule",
    4 : "dosage_form",
    5 : "pack_size",
    6 : "num_packs",
    7 : "is_generic",
}

var process_ingredient = function(js) {
    d3.select("#loading-indicator").style("display", "none");
    d3.selectAll(".template").classed("template", true);
    d3.selectAll(".products .product").remove();

    if (js.length > 0) {
        d3.select("#resultsheader").style("display", "block");
        d3.selectAll(".products").classed("template", false);

        var row = d3.select(".products .template")[0][0];

        d3.selectAll(".products").selectAll("div.product")
            .data(js)
            .enter()
            .append("div")
            .classed("product", true)
            .classed("row", true)
            .html(function(el, i) {
                return row.innerHTML;
            })
            .each(function(el, i) {
                var data = el;
                d3.select(this).selectAll("div.details span").text(function(el, i) {
                    var key = map[i];
                    return data[key];
                })
                d3.select(this).selectAll("div.ingredients div").remove()
                d3.select(this).selectAll("div.ingredients").selectAll("div")
                    .data(data.ingredients) 
                    .enter()
                    .append("div")
                    .html(function(el, i) {
                        return "<div>" + el.name + ": <span>" + el.strength + el.unit + "</span></div>"
                    })
            })
        
    }
}

var timer;
var entermedicine = function(el) {
    var text = d3.event.target.value;

    var load = function() {
        d3.select("#loading-indicator").style("display", "block");
        d3.select("#resultsheader").style("display", "none");
        d3.json("/api/?ingredient=" + text, process_ingredient)
    }

    clearTimeout(timer)
    timer = setTimeout(load, 500);

}
