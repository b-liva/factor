var var1 = {
    name: 'Jemco'
};
// console.log(var1)
// alert(var1.name)

$('#newCustomer215').on('submit', function (e) {
    e.preventDefault();
    var this_ = $('#newCustomer');
    console.log(this_);
    // alert(this_);
    var code = $('#customer-code').val();
    var customer = {
        'code': $('input#customer-code').val(),
        'name': $('input#customer-name').val(),
        'type': $('#customer-type option:selected').val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),

    };
    console.log(customer.type);

    $.ajax({
        url: this_.attr('action'),
        method: "POST",
        data: customer,
        success: function (data) {
            console.log('success');
        },
        error: function (error) {
            console.log('error');
        }
    });
    alert($("#pub_datePicker").val());
    alert($('#customer-name').val());
    // alert('hi there');
});

$('.imgClr').on('click', function () {
    var pdata = {
        'id': this.id,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),

    };
    $.ajax({
        url: 'img/del',
        method: "POST",
        data: pdata,
        success: function (data) {
            console.log('success');
        },
        error: function (error) {
            console.log('error');
        }
    });

});


// $(function () {
//         $('.pub_date').datetimepicker({
//             format:'YYYY-MM-DD HH:mm:ss',
//             locale: 'ru'
//         }).on('show', function () {
//         var dp = $(this);
//         if(dp.val() == ''){
//             dp.val('20-05-1980').pDatePicker('update');
//         }
//     });
//     });


// $(document).ready(function () {
//     $(".datetime-input").pDatepicker({
//         autoClose: true,
//         initialValue: false
//     }).on('show', function () {
//         var dp = $(this);
//         if(dp.val() == ''){
//             dp.val('20-05-1980').pDatePicker('update');
//         }
//     });
// });

$(document).ready(function () {
    $("#pub_datePicker").pDatepicker({
        autoClose: true,
        // setDate: new Date(),
        initialValue: true,
        calendarType: 'gregorian',
        format: 'YYYY-MM-DD HH:mm:ss',

    });
    $("#pub_date2").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#date_fa").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#exp_date_fa").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#due_date").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#perm_date").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#date_fa_start").pDatepicker({
        autoClose: true,
        initialValue: false,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#date_fa_end").pDatepicker({
        autoClose: true,
        initialValue: false,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#id_date2").pDatepicker({
        autoClose: true,
        initialValue: true,
        calendarType: 'persian',
        format: 'YYYY-MM-DD',
    });
    $("#test").pDatepicker({
        minDate: 2,
        maxDate: "+10D",
        isRTL: true,
        format: 'YYYY-MM-DD',

    });

    var arr = ['first', 'secon', 'third'];

    $('#autocomplete').autocomplete({
        serviceUrl: '/customer/autocomplete',
        contentType: 'application/json',
        dataType: 'json',
        // lookup: arr,
        // onSearchComplete: function (query, suggestions) {
        //     alert(suggestions);
        // }
        // select: function (suggestion) {
        //     $(this).val(suggestion);
        //     console.log(suggestion);
        // }
        onSelect: function (suggestion) {
            // $(this).val(suggestion.data);
            document.cookie = "customer=" + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            // document.cookie("customer", suggestion.data);
            document.cookie = "customer=" + suggestion.data;
            $('#cu_value').val(suggestion.data);
        }
    });
    $('#cu_chosen').chosen();

    new AutoNumeric.multiple('input[name=price]', {
        digitGroupSeparator: ',',
        decimalPlaces: 0
    });

});


// $(document).ready(function () {
//     $(".pub_date").datetimepicker().on('changeDate', function (e) {
//          // $(this).val(e.date().valueOf())
//         alert(e);
//     });
// });


function checkBeforeDelete() {
    alert('are you sure?');
}

