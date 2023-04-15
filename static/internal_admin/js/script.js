"use strict";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                let cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    let cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
});

const getPrevSiblings = (elem) => {
    let prevSiblings = [];
    let sibling = elem;
    while (sibling.previousSibling) {
        sibling = sibling.previousSibling;
        sibling.nodeType == 1 && prevSiblings.push(sibling);
    }
    return prevSiblings;
};

let checked_inputs_values = [];


if (document.querySelector(".table-list")) {
    // product disabled in table-list
    const toggleDisabledItem = (buttons) => {

        buttons.forEach(button => {
            button.addEventListener("click", function() {
                this.classList.toggle("active");
                let getElementsItem = getPrevSiblings(button.parentElement);

                getElementsItem.forEach(getElement => {
                    getElement.classList.toggle("disabled");
                });
            });
        });
    };

    const btnDisableds = document.querySelectorAll(".btn-disabled");

    toggleDisabledItem(btnDisableds);

    // all checkbox checked in table-list
    const checkAlls = document.querySelectorAll(".product-check-all");
    const checks = document.querySelectorAll(".product-check");
    const table = document.querySelector(".table-list");

    const checkedCheckAll = (check, checkList) => {
        for (let i = 0; i < checkList.length; i++) {
            if (check.checked) {
                checkList[i].checked = true;
            } else {
                checkList[i].checked = false;
            }
        }
    };

    const countedCheckeds = () => {
        let checks_all = [];
        let checks_checked = [];
        checked_inputs_values = [];

        checks.forEach(check => {
            checks_all.push(check);
        });

        document.querySelectorAll(".product-check:checked").forEach(item_check => {
            checks_checked.push(item_check);
            checked_inputs_values.push(item_check.value);
        });

        let count_all = checks_all.length;
        let count_checked = checks_checked.length;

        if (count_checked > 0) {
            table.classList.add("table-all-check");
        } else {
            table.classList.remove("table-all-check");
            checkAll.checked = false;
        }

        document.querySelector(".count-check").textContent = count_checked;
        document.querySelector(".count-all").textContent = count_all;
    };

    checks.forEach(check => {
        check.addEventListener("change", () => {
            countedCheckeds();
        });
    });

    checkAlls.forEach(checkAll => {
        checkAll.addEventListener("change", () => {
            checkedCheckAll(this, checks);
            countedCheckeds();
        });
    });
}


// переключение сортировки цены в таблице
if (document.querySelector(".btn-sort-price")) {
    const toggleSortPriceProducts = (btn) => {
        btn.addEventListener("click", function() {
            this.classList.toggle("with-more");
        });
    };

    const btnSortPrice = document.querySelector(".btn-sort-price");

    toggleSortPriceProducts(btnSortPrice);
}

// сброс чексбоксов в модалке с выбором колонок
if (document.querySelector(".btn-products-settings")) {
    const btnReset = document.querySelector("#reset");
    const settingCheckboxs = document.querySelectorAll(".modal-products-settings input");

    const resetAllCheckbox = (checkboxs) => {
        checkboxs.forEach(checkbox => {
            checkbox.checked = false;
        });
    };

    btnReset.addEventListener("click", () => {
        resetAllCheckbox(settingCheckboxs);
    });

    // top для модалки с выбором колонок
    const getPositionOpenModal = (e) => {
        let y = e.clientY;
        document.querySelector(".modal-products-settings .modal-dialog").style.top = y + 19 + "px";
    };


    try {
        document.querySelector(".btn-products-settings").addEventListener("click", (e) => {
            getPositionOpenModal(e);
        });
    } catch (e) {
    }
}

// resize textarea
if (document.querySelector("textarea")) {
    let textareas = document.querySelectorAll("textarea");

    textareas.forEach(textarea => {
        textarea.addEventListener("input", resizeHeight);
    });

    function resizeHeight(e) {
        let evt = e || evt || window.evt;
        let getElement = evt.target || evt.srcElement;
        getElement.style.height = Math.max(getElement.scrollHeight, getElement.offsetHeight) + "px";
    }
}

// связи select
if (document.querySelector("#connections")) {

    let colsSelects = document.querySelectorAll(".col-connections");

    colsSelects.forEach(colSelect => {
        colSelect.addEventListener("click", function() {
            let ul = colSelect.querySelector(".col-connections .select2-selection__rendered");

            if (document.querySelector(".select2-dropdown")) {
                document.querySelector(".select2-dropdown").addEventListener("click", function() {
                    let select = colSelect.querySelector(".col-connections .select2");

                    select.style.marginBottom = ul.offsetHeight + "px";
                });
            }

            colSelect.querySelector(".select2").addEventListener("click", function() {
                this.style.marginBottom = ul.offsetHeight + "px";
            });
        });
    });

}

// products group actions

$(document).on("click", "#disableProducts", function(e) {
    let url = $("#crmProductsList").data("disable-products-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#enableProducts", function(e) {
    let url = $("#crmProductsList").data("enable-products-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deleteProducts", function(e) {
    let url = $("#crmProductsList").data("delete-products-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#copyProducts", function(e) {
    let url = $("#crmProductsList").data("copy-products-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

// categories group actions

$(document).on("click", "#disableCategories", function(e) {
    let url = $("#crmCategoriesList").data("disable-categories-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#enableCategories", function(e) {
    let url = $("#crmCategoriesList").data("enable-categories-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deleteCategories", function(e) {
    let url = $("#crmCategoriesList").data("delete-categories-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#copyCategories", function(e) {
    let url = $("#crmCategoriesList").data("copy-categories-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

// orders group actions

$(document).on("click", "#deleteOrders", function(e) {
    let url = $("#crmOrdersList").data("delete-orders-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#sendToRetailOrders", function(e) {
    let url = $("#crmOrdersList").data("send-to-retail-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});


$(document).on("click", "#copyOrders", function(e) {
    let url = $("#crmOrdersList").data("copy-orders-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

// users group actions

$(document).on("click", "#deleteUsers", function(e) {
    let url = $("#crmUsersList").data("delete-users-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});


$(document).on("click", "#deleteBanners", function(e) {
    let url = $("#crmSecondbanner").data("delete-banners");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deleteThirdBanners", function(e) {
    let url = $("#crmThirdBanner").data("delete-banners");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});


$(document).on("click", ".js-submit-category-form", function(e) {
    $(".js-product-form").submit();
});

$(document).ready(function() {
    if ($('.form-control').hasClass('is-invalid')) {
        $('.form-control.is-invalid').on('input', function() {
            $(this).removeClass('is-invalid');
            if ($(this).prop("required", true) && $(this).val().length === 0) {
                $(this).addClass('is-invalid');
            }
        });
    }
});


// PROMOCODES group actions

$(document).on("click", "#disablePromocodes", function(e) {
    let url = $("#crmPromocodesList").data("disable-promocodes-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#enablePromocodes", function(e) {
    let url = $("#crmPromocodesList").data("enable-promocodes-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deletePromocodes", function(e) {
    let url = $("#crmPromocodesList").data("delete-promocodes-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#copyPromocodes", function(e) {
    let url = $("#crmPromocodesList").data("copy-promocodes-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

// SIZE SUBSCRIPTIONS group actions

$(document).on("click", "#disableSubscriptions", function(e) {
    let url = $("#crmSizeSubscriptionsList").data("disable-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#enableSubscriptions", function(e) {
    let url = $("#crmSizeSubscriptionsList").data("enable-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deleteSubscriptions", function(e) {
    let url = $("#crmSizeSubscriptionsList").data("delete-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#copySubscriptions", function(e) {
    let url = $("#crmSizeSubscriptionsList").data("copy-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

// EMAIL NESLETTER group actions

$(document).on("click", "#disableEmailSubscriptions", function(e) {
    let url = $("#crmEmailSubscriptionsList").data("disable-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#enableEmailSubscriptions", function(e) {
    let url = $("#crmEmailSubscriptionsList").data("enable-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#deleteEmailSubscriptions", function(e) {
    let url = $("#crmEmailSubscriptionsList").data("delete-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

$(document).on("click", "#copyEmailSubscriptions", function(e) {
    let url = $("#crmEmailSubscriptionsList").data("copy-subscriptions-url");
    $.ajax({
        url: url,
        method: "post",
        data: JSON.stringify({ "items_to_action": checked_inputs_values }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            location.reload();
        }
    });
});

function readURL(file) {
    var reader = new FileReader();

    reader.onload = function(e) {
        $("#blah").attr("src", e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
}

function showMyImage(fileInput) {
    let files = fileInput.files;
    for (let i = 0; i < files.length; i++) {
        var file = files[i];

        var img = document.getElementById("thumbnil");
        img.file = file;
        var reader = new FileReader();
        reader.onload = (function(aImg) {
            return function(e) {
                aImg.src = e.target.result;
            };
        })(img);
        reader.readAsDataURL(file);
    }
}

function create_form_gallery(data, file) {
    const empty_form = $(".js-gallery-empty_form");
    const formsets = $(".gallery__img");
    const prefix = formsets.data("prefix");
    const total_forms = $(`#id_${prefix}-TOTAL_FORMS`);
    const count_forms = parseInt(total_forms.val()) + 1;
    const html = empty_form.html();
    let compiled_tmpl = html.replace(/__prefix__/g, total_forms.val())
    let validImageTypes = ["image/gif", "image/jpeg", "image/png", "image/jpg"];
    console.log(compiled_tmpl)
    if (validImageTypes.includes(file)) {
        compiled_tmpl = compiled_tmpl.replace(/ <video src="__img_placeholder__" alt="">/g, `<img src=${data.file_url}>`);
    } else {
        compiled_tmpl = compiled_tmpl.replace(/ <video src="__img_placeholder__" alt="">/g, `<video src=${data.file_url}></video>`);
    }

    total_forms.val(count_forms);
    formsets.append(compiled_tmpl);
    const item = $(".js-gallery__card").last();
    const inputs = item.children(".js-hidden");
    const temp_file = inputs.children(".js-temp-file");
    temp_file.val(data.file_id);
}

function upload_file(file){
    const files = file.prop("files");
    for (const element of files) {
        let valid_types = [/image.*/, /video.*/];
        let fileObj = element;
        if (!(!(fileObj.type in valid_types))) {
            continue;
        }
        const url = "/crm/tmp-file-upload/";
        const data = new FormData();
        data.append("file", fileObj);
        let response_data = {};
        $.ajax({
            url: url,
            method: "post",
            data: data,
            enctype: "multipart/form-data",
            processData: false,
            contentType: false,
            success: function(data) {
                create_form_gallery(data, fileObj.type);
            },
            error: function(data) {
                console.error(data);
            }
        });
    }
}
$(document).on("change", "#file-img", function(e) {
    upload_file($(this))
});

function handle_sort() {
    const items = $(".js-draggable-gallery").children(".js-gallery__card");
    for (let i = 0; i < items.length; i++) {
        let item = items.eq(i);

        let inputs = item.children(".js-hidden");
        let order_field = inputs.children(".js-order-field");
        order_field.val(i);
    }
}

$(".js-draggable-gallery").sortable({
    container: ".js-draggable-gallery",
    nodes: ".js-gallery__card",
    update: handle_sort
});

$(document).on("click", ".js-card-video", function(e) {
    $(".jsfield-video").click();
});

$(document).on("change", ".jsfield-video", function(e) {
    const value = $(this).val().replace(/^.*[\\\/]/, "");
    $(".placeholder-name").text(value);
});

$(document).on("click", ".js-submit-user-form", function(e) {
    $(".js-user-form").submit();
});

function isEmpty(str) {
    return !str.trim().length;
}


$(document).on("click", "#crmChangePassword", function(e) {
    $("#passwordChangeCrmErrorSameAsEmail").hide();
    $("#passwordChangeCrmErrorTooShort").hide();
    $("#passwordChangeCrmError").hide();
    $("#passwordChangeCrmEmpty").hide();
    $("#passwordChangeCrmSuccess").hide();


    let password = $("#passwordChangeCrm").val();
    let repeat_password = $("#password_repeatCrm").val();
    let email = $("#id_email").val();
    let short_email = email.split("@")[0]

    if (repeat_password.length === 0 && password.length === 0) {
        $("#passwordChangeCrmEmpty").show()
        return;
    }

    if (password !== repeat_password || isEmpty(password) || isEmpty(repeat_password)) {
        $("#passwordChangeCrmError").show();
        return;
    }

    if (password.length < 8) {
        $("#passwordChangeCrmErrorTooShort").show();
        return;
    }

    if (password === email || password === short_email) {
        $("#passwordChangeCrmErrorSameAsEmail").show();
        return;
    }

    let userId = $(".js-user-form").data("user-id");
    $.ajax({
        url: `/crm/api/users/crm-change-password/${userId}/`,
        method: "post",
        data: JSON.stringify({ "password": password, "repeat_password": repeat_password }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        dataType: "json",
        success: function(data) {
            $("#passwordChangeCrmSuccess").show();
            $("#passwordChangeCrm").val(null);
            $("#password_repeatCrm").val(null);
        },
        error: function(data) {
            $("#passwordChangeCrmError").show();
        }
    });
});

$(document).on("keydown", "#crmGlobalSearchInput", function(e) {
    if (e.keyCode === 13) {
        location.href = location.origin + "/crm/global-search/" + `?search=${$("#crmGlobalSearchInput").val()}`;
    }
});

$(document).on("click", "#crmGlobalSearchButton", function(e) {
    location.href = location.origin + "/crm/global-search/" + `?search=${$("#crmGlobalSearchInput").val()}`;
});

$(document).on('contextmenu', '.js-delete-card ', function (e){
    e.preventDefault();
    const container = $(this).closest('.js-gallery__card');
    const input = container.find('input[id*=DELETE]');
    input.prop('checked', true);
    input.attr('checked', true);
    container.hide();
});


$('.table-list input').on('click', function(e) {
    e.stopPropagation();
});

$('.table-list a').on('click', function(e) {
    e.stopPropagation();
});

$(document).on('click', '.js-order-crm', function (e){
    const input = $(this);
    e.target.disabled = false;
    const button = input.parent().find('button');
    button.show();
});

$(document).on('keydown', '.product-id-form', function(e){
    if (e.which === 13) {
        const url = $(this).data('url');
        const value = $(this).val();
        let resultData;
        if ( $(this).data('field_form') === "order" ) {
            resultData = {
                "order": value
            }
        }
        $(this).attr('disabled', true);
        $.ajax({
            url: url,
            method: 'post',
            data: JSON.stringify(resultData),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            dataType: "json",
            success: function (data){
            },
            error: function (data) {
            }
        })
    }
});


$(document).on('change', '.js-crm-select', function(e) {
        const url = $(this).data('url');
        const value = $(this).val();
        let resultData;
        if ( $(this).data('field') === "is_new" ) {
            if (value === "true") {
                resultData = {
                "is_new": true
                }
            } else if (value === "false") {
                resultData = {
                "is_new": false
                }
            }
        } else if ($(this).data('field') === "is_soon") {
            if (value === "true") {
                resultData = {
                "is_soon": true
                }
            } else if (value === "false") {
                resultData = {
                "is_soon": false
                }
            }
        }
        $(this).attr('disabled', true);
        $.ajax({
            url: url,
            method: 'post',
            data: JSON.stringify(resultData),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            dataType: "json",
            success: function (data){
            },
            error: function (data) {
            }
        })
    // }
});


if (document.querySelector(".input-search-filters")) {
    const myModal = document.querySelector(".modal-search-filters");
    const input = document.querySelector(".input-search-filters");
    const reset = document.querySelector(".btn-search-reset");
    const titles = document.querySelectorAll(".filter-title");
    const subBoxs = document.querySelectorAll(".filters-sub-box");
    const subBoxsInputs = myModal.querySelectorAll(".form-control");
    const count = document.querySelector(".search-filters_count");
    const myModalChecks = myModal.querySelectorAll(".form-check-input");
    let myModalChecked;

    input.addEventListener('click', function() {
        myModal.classList.toggle("show");
    });

    document.addEventListener('click', function(e) {
        const target = e.target;
        const its_modal = target == myModal || myModal.contains(target);
        const its_input = target == input;
        const modal_show = myModal.classList.contains("show");

        if (!its_modal && !its_input && modal_show) {
            myModal.classList.remove("show");
        }
    });

    titles.forEach((title) => {

        title.addEventListener('mousedown', function(e) {

            const thisSubBox = this.nextElementSibling;
            const check = this.querySelector("input");
            const label = this.querySelector("label");
            const target = e.target;
            const itsTarget = target == check || target == label;

            if (!itsTarget) {
                titles.forEach((title) => {
                    if (title.classList.contains("open") && title != this) {
                        title.classList.remove("open");
                    }
                });

                subBoxs.forEach((subBox) => {
                    if (subBox.classList.contains("active") && subBox != thisSubBox) {
                        subBox.classList.remove("active");
                    }
                });

                thisSubBox.classList.toggle("active");
                this.classList.toggle("open");
            } else {
                check.addEventListener('change', function() {
                    const thisSubBox = this.parentNode.nextElementSibling;
                    const subChecks = thisSubBox.querySelectorAll(".form-check-input");
                    const subInputs = thisSubBox.querySelectorAll(".form-control");

                    titles.forEach((title) => {
                        if (title.classList.contains("open")) {
                            title.classList.remove("open");
                        }
                    });

                    subBoxs.forEach((subBox) => {
                        if (subBox.classList.contains("active")) {
                            subBox.classList.remove("active");
                        }
                    });

                    if (this.checked) {
                        thisSubBox.classList.toggle("active");
                        this.parentNode.classList.toggle("open");

                        subChecks.forEach((subCheck) => {
                            subCheck.checked = true;
                        });
                    }  else {
                        subChecks.forEach((subCheck) => {
                            subCheck.checked = false;
                        });

                        subInputs.forEach((subInput) => {
                            subInput.value = '';
                        });
                    }
                });
            }
        }, false);
    });

    myModalChecks.forEach((myModalCheck) => {
        myModalCheck.addEventListener("change", function() {
            if (myModalCheck.parentElement.classList.contains("filter-title") && myModalCheck.parentElement.nextElementSibling.children[0].classList.contains("sub-box-row")) {
                myModalCheck.parentElement.classList.add("next-form");
            }

            setTimeout(() => {
                const countChecked = myModal.querySelectorAll(".filters-sublist .form-check-input:checked").length;
                let countCheckedTitle = myModal.querySelectorAll(".next-form .form-check-input:checked").length;
                let countNumber = countChecked + countCheckedTitle;

                count.setAttribute("data-count", countNumber)
                count.innerHTML = countNumber;

                if (countNumber > 0) {
                    input.parentNode.classList.add("filt");
                } else {
                    input.parentNode.classList.remove("filt");
                }
            });
        });
    });

    subBoxs.forEach((subBox) => {
        const subBoxChecks = subBox.querySelectorAll(".form-check-input");
        let subBoxChecked;

        subBoxChecks.forEach((subBoxCheck) => {
            subBoxCheck.addEventListener("change", function() {
                subBoxChecked = subBox.querySelectorAll(".form-check-input:checked");

                if (subBoxChecked.length > 0) {
                    subBox.previousElementSibling.querySelector(".form-check-input").checked = true;
                } else {
                    subBox.classList.remove("active");
                    subBox.previousElementSibling.classList.remove("open");
                    subBox.previousElementSibling.querySelector(".form-check-input").checked = false;
                }
            });
        });
    });

    subBoxsInputs.forEach((subBoxsInput) => {
        subBoxsInput.addEventListener("change", function(e) {

            if (subBoxsInput.value.length > 0) {
                const target = e.target;
                const parent = target.closest('.filters-sub-box');
                parent.previousElementSibling.classList.add("next-form");
                parent.previousElementSibling.querySelector(".form-check-input").click();
                parent.previousElementSibling.querySelector(".form-check-input").checked = true;
            }
        });
    });

    reset.addEventListener("click", function() {
        input.value = '';
        input.parentNode.classList.remove("filt");

        myModalChecks.forEach((myModalCheck) => {
            myModalCheck.checked = false;
        });

        titles.forEach((title) => {
            if (title.classList.contains("open")) {
                title.classList.remove("open");
            }
        });

        subBoxs.forEach((subBox) => {
            if (subBox.classList.contains("active")) {
                subBox.classList.remove("active");
            }
        });

        subBoxsInputs.forEach((subBoxsInput) => {
            subBoxsInput.value = '';
        });
    });

    document.querySelector(".filter-search-form").onsubmit = function() {
        let countValue = count.textContent;
        localStorage.setItem('countValue', countValue);
    };

    window.onload = function() {
        count.innerHTML = localStorage.getItem('countValue');
    };



}
