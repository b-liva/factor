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
    // $('#pub_datePicker').val(15654);
    // $('.pub_date2').pDatepicker("setDate", new Date());
    // $('.pub_date2').pDatepicker("setDate", new Date);
});


// $(document).ready(function () {
//     $(".pub_date").datetimepicker().on('changeDate', function (e) {
//          // $(this).val(e.date().valueOf())
//         alert(e);
//     });
// });
