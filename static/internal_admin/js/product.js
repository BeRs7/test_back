function count_forms() {
    return document.querySelectorAll('[id^=product_trade_offer_form]').length - 1 // one is empty form
}

function create_block() {
    const raw_tpl = $("#empty_product_trade_offer_form").html();
    const block_containers = $("#trade_offers_container");
    const prefix = block_containers.data("prefix");
    const total_forms = $(`#id_${prefix}-TOTAL_FORMS`);
    let compiled_tmpl = raw_tpl.replace(/__prefix__/g, total_forms.val());
    block_containers.append(compiled_tmpl);
    total_forms.val(this.count_forms());
}

function handle_sort() {
    const items = $(".js-draggable-gallery").children(".js-gallery__card");
    for (let i = 0; i < items.length; i++) {
        let item = items.eq(i);

        let inputs = item.children(".js-hidden");
        let order_field = inputs.children(".js-order-field");
        order_field.val(i);
    }
}

// CLICK TRIGGERS
$(document).on("click",  "#add_trade_offer", function(e){
   e.preventDefault();
   create_block();
   $('.select2-container').remove();

   $('.django-select2').djangoSelect2("destroy");
   $('.django-select2').djangoSelect2();
   // setTimeout(() => {
   //     $('.django-select2').each(function (){
   //         $(this).djangoSelect2();
   //     })
   // }, 800);
});

$(document).on("click", "#js-submit-product-form", function(e) {
    handle_sort();
    $("#empty_product_trade_offer_form").remove()
    $(".js-product-form").submit();
});
