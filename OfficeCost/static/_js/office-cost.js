"use strict";
$(document).ready(function () {
    $('#navbar-collapse-1 a').each(function () {
        if ($(this).attr('href') == window.location.pathname) {
            $(this).parent().addClass('active');
        }
    });
    $('#amount').on({'keypress': amountKeyFilter, 'blur': amountBlur});
    $('#select').on('change', selectChange);
    $('#add-form').submit(addFormSubmit);
    $('#dateRedirect').click(dateRedirect);
});

function dateRedirect(event) {
    var startDate = $('#startDate').val();
    var finishDate = $('#finishDate').val();
    var departmentSelect = $('#departmentSelect').val();
    var params = {
        startDate: startDate,
        finishDate: finishDate,
        departmentSelect: departmentSelect
    };
    var paramsStr = $.param(params);
    location.href += '?' + paramsStr;

}

function selectChange(event) {
    if (this.selectedIndex !== 0) {
        $(this).parents('.form-group').removeClass('has-error');
    }

}

function addFormSubmit(event) {
    var select = $('#select');
    if (select.val() === null) {
        event.preventDefault();
        select.parents('.form-group').addClass('has-error');
        //alert
    }
    var date = $('#date');
    if (date.val() === '') {
        event.preventDefault();
        date.parents('.form-group').addClass('has-error');
    }
    var amount = $('#amount');
    if (amount.val() === '') {
        event.preventDefault();
        amount.parents('.form-group').addClass('has-error');
    }
}

function amountKeyFilter(event) {
    if ($.isNumeric(event.key) || (event.key === '.' && !checkContainDot($(this).val()))) {
        $(this).parents('.form-group').removeClass('has-error');
    }
    else {
        event.preventDefault();
        $(this).parents('.form-group').addClass('has-error');
    }
}

function checkContainDot(value) {
    var currentInput = value || '';
    return (currentInput.includes('.'))
}

function amountBlur(event) {
    var element = $('#amount');
    if (!checkContainDot(element.val()) && element.val() != '') {
        element.val(element.val() + '.00');
    }
    else {
        if (element.val().match(/\.\d$/)) {
            element.val(element.val() + '0');
        }
        else if (element.val().match(/\.$/)) {
            element.val(element.val() + '00');
        }
    }
    element.parents('.form-group').removeClass('has-error');
}