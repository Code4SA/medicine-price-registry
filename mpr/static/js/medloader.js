/**
 * medloader - openup.org.za
 */

var timer,
    delay = 500,
    animate_speed = 750;
var search_url = function(term) { return '/api/v2/search-lite?q=' + term; }
var related_url = function(id) { return '/api/v2/related?nappi=' + id };
var product_detail_url = function(id) { return '/api/v3/detail?nappi=' + id };


var log = function(obj) {
    if (window.console) {
        window.console.log(obj);
    }
};

var log_analytics = function(event, properties) {
    amplitude.getInstance().logEvent(event, properties);
}

var map = {
    0 : 'sep',
    1 : 'dispensing_fee',
    2 : 'price_range',
    3 : 'cost_per_unit',
    4 : 'schedule',
    5 : 'dosage_form',
    6 : 'pack_size',
    7 : 'num_packs',
    8 : 'is_generic',
};

var load_data = function(url, foo) {
    on_loading();
    return $.getJSON(url, function(data) {
        on_loaded(data);
        foo(data);
    });
}

Product = function(data, block) { 
    this.data = data;
    this.block = block.addClass('product');
}

Product.prototype = {

    set_name : function() {
        $('.product-name', this.block).html(this.data.name).attr('href', '#product-detail-' + this.data.nappi_code);
    },

    set_price : function() {
        $('.product-price', this.block).html(this.data.sep);
    },

    set_class_names : function() {
        // We can't assume all data returned is of type: string :(
        if (typeof this.data.is_generic == 'string') {
            var classNameGeneric = 'type_' + this.data.is_generic.toLowerCase();
            $(this.block).addClass(classNameGeneric);
        }
        if (typeof this.data.dosage_form == 'string') {
            var classNameDosageForm = 'df_' + this.data.dosage_form.toLowerCase().replace(' ', '_');
            $(this.block).addClass(classNameDosageForm);
        }
    },

    set_related_link : function() {
        related_link = $('.find-generic a', $(this.block));
        console.log(this.data)
        related_link.attr('href', '#related:' + this.data.nappi_code);
    },

    build_product : function() {
        this.set_name();
        this.set_price();
        this.set_class_names();
        this.set_related_link();

        return this.block;
    }
}

var on_loading = function() {
    $('#search-container').addClass('js-loading');
}

var on_loaded = function(result) {
    $('#search-container').removeClass('js-loading');
}


var process_request = function(result) {
    $('.products .product').remove();
    $('#noresults').hide();
    $('#resultsheader').hide();

    if (result.length) {
        $('#resultsheader').show();
        $('#resultsheader span').html(result.length);

        var $templateRow = $('.products .template');
        for (var i = 0; i < result.length; i++) {
            var $product = new Product(result[i], $templateRow.clone().removeClass('template'));
            $('.products').append($product.build_product());
        }
        
        $('.product .product-name').on('click', function(e) {
            e.preventDefault();
            add_product_detail($(this));
        });
    } else {
        $('#noresults').show();
    }
    on_loaded(result);
}

var $templateDetail = $('.products .template-panel-body');
var add_product_detail = function(elem) {
    var target_id = elem.attr('href').split('#product-detail-')[1];

    load_data(product_detail_url(target_id), function(data) {
        // Switch off any further event bindings to the source anchor, so that we don't get two results
        elem.off();
        console.log(data)
        log_analytics("product-detail", data);

        // Set up the template
        var $product_detail = $templateDetail.clone().removeClass('template-panel-body');

        // Add product detail
        $('.details dd', $product_detail).each(function(idx) {
            var key = map[idx];
            if (key == "cost_per_unit") {
                val = data["min_cost_per_unit"] + " / " + data["dosage_form"] + " - " + data["max_cost_per_unit"] + " / " + data["dosage_form"];
            } else if (key == "price_range") {
                val = data["min_price"] + " - " + data["max_price"]
            } else {
                val = data[key]
            }
            $(this).html(val)
        });

        if (data["dosage_form"] != "tablet" && data["dosage_form"] != "capsule")
            $('.details .cost-per-unit', $product_detail).remove();

        // Add ingredients
        var $ingredientsList = $('.ingredients dl', $product_detail);
        var productIngredients = data.ingredients;
        var productIngredientsLength = productIngredients.length;
        for (var j = 0; j < productIngredientsLength; j++) {
            $ingredientsList.append('<dt>' + productIngredients[j].name.trim() + ':</dt>');
            $ingredientsList.append('<dd>' + productIngredients[j].strength + productIngredients[j].unit + '</dd>');
        }

        // Add meta data
        $('.product-reg-number', $product_detail).html(data.regno);

        if (data.insert_url == undefined) {
            $('.package-insert', $product_detail).remove()
        } else {
            $('.product-package-insert', $product_detail).html(data.insert_url);
            $('.product-package-insert', $product_detail)[0]["href"] = data.insert_url;
        }

        // Add product-detail ID so that we have something to target with collapse()
        console.log(data)
        $product_detail.attr('id', 'product-detail-' + data.nappi_code);
        
        // Append the detail to the product in question
        elem.parents('.product').append($product_detail);

        // Add collapse toggle to the source anchor
        elem.on('click', function() {
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
        location.hash = 'search:' + searchTerm;
    }

    var reset_delay_before_requesting = function() {
        clearTimeout(timer);
        timer = setTimeout(load_data, delay);
    }

    reset_delay_before_requesting();
};

var load_medicines = function(value) {
    if (value.indexOf(':') >= 0) {
        var s = value.split(':')
        var key = s[0]
        var value = s[1]

        if (key == '#related') {
            load_data(related_url(value), process_request);
            log_analytics("product-related", {"id" : value});
        } else if (key == '#search') {
            load_data(search_url(value), process_request);
            log_analytics("product-search", {"query" : value});
        }

        $('html, body').animate({
            scrollTop: $('#top').offset().top
        }, animate_speed);
    }
}
