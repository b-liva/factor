// var data = [
//         {y: '2014', a: 50, b: 30},
//         {y: '2015', a: 55, b: 35},
//         {y: '2016', a: 65, b: 50},
//         {y: '2017', a: 75, b: 60},
//         {y: '2018', a: 80, b: 65},
//         {y: '2019', a: 90, b: 70},
//         {y: '2020', a: 100, b: 75},
//         {y: '2021', a: 115, b: 75},
//         {y: '2022', a: 120, b: 85},
//         {y: '2023', a: 145, b: 85},
//         {y: '2024', a: 160, b: 95}
//     ];
var data = [];
var config = {
    data: data,
    xkey: 'y',
    ykeys: ['a', 'b', 'c'],
    labels: ['درخواست های دریافتی', 'Money received'],
    fillOpacity: 0.6,
    hideHover: 'auto',
    behaveLikeLine: true,
    resize: true,
    pointFillColors: ['#ffffff'],
    pointStrokeColors: ['black'],
    lineColors: ['gray', 'red'],
    xLabel: ['day'],
    redraw: true,
};

var endPoint = '/kwjs/';

$('#ajaxbtn').click(function (e) {
    e.preventDefault();
    this_ = $('#dayNumers');
    var days = this_.val();
    if (days == null) {
        days = 30;
    }
    // var ajaxUrlRaw = this_.attr('rawUrl') + this_.val() + '/';
    var ajaxUrlRaw = this_.attr('rawUrl') + days + '/';
    // alert('raw: ' + ajaxUrlRaw);
    var data = {
        'days': this_.val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    };

    $.ajax({
        method: 'POST',
        url: endPoint,
        data: data,
        success: function (data_obj) {
            // alert('success_data: ' + data_obj);
            console.log('success_data: ' + data_obj);
            var newData = [];
            var ProformaData = [];

            Object.keys(data_obj).forEach(function (key) {
                console.log(key, data_obj[key]);
                Object.keys(data_obj[key]).forEach(function (k) {
                    if (key == 'reqs') {
                        newData.push({
                            y: k,
                            a: data_obj[key][k],
                        });
                    }
                    else if (key == 'proformas') {
                        newData.push({
                            // y: k,
                            b: data_obj[key][k],
                        });
                    }
                });
            });
            console.log(newData);
            // console.log(ProformaData);
            config.data = newData;
            do_chart(true, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            // do_chart(true, ProformaData, 'b', 'line-chart', 'پیش فاکتورهای صادر شده');
            // chart.setDate(newData);
            chart.redraw();


        },
        error: function (error_data) {
            // alert('failure');
            //
            // alert('errors: ' + error_data);
            console.log('error: ' + error_data);
        },
    });

});

var update_chart = function (method, element) {
    if (element) {
        this_ = $(element);
        // var ajaxUrlRaw = this_.attr('rawUrl') + this_.val() + '/';
        var days = this_.val();
        // alert(typeof (days));
        // console.log('this days ' + days);
        // if (days.length == 0) {
        //     alert('checked');
        //     days = 30;
        //     days= days.toString();
        //
        //     alert(typeof days);
        //     alert(days);
        // }
        // alert('raw: ' + ajaxUrlRaw);
        var data = {
            'days': days,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        };
        redraw = true;
    }
    else {
        var redraw = false;
    }

    $.ajax({
        method: method,
        url: endPoint,
        data: data,

        success: function (data_obj) {
            var newData = [];
            var ProformaData = [];
            var paymentData = [];

            Object.keys(data_obj).forEach(function (key) {
                console.log(key, data_obj[key]);
                Object.keys(data_obj[key]).forEach(function (k) {
                    if (key == 'reqs') {
                        newData.push({
                            y: k,
                            a: data_obj[key][k],
                        });
                    }
                    else if (key == 'proformas') {
                        ProformaData.push({
                            y: k,
                            b: data_obj[key][k],
                        });

                    }
                    else if (key == 'payments') {
                        paymentData.push({
                            y: k,
                            a: data_obj[key][k],
                        });
                        paymentData.b = ProformaData.b;
                    }
                });
            });
            // console.log(newData);
            // console.log(ProformaData);
            // console.log(paymentData);

            do_chart(redraw, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            do_chart(redraw, ProformaData, 'b', 'line-chart', 'پیش فاکتورهای صادر شده');
            do_chart(redraw, paymentData, 'a', 'payment-line-chart', 'پرداخت های انجام شده');
        },
        error: function (error_data) {
            // alert('errors: ' + error_data);
            console.log('error: ' + error_data);
        },
    });
};

var customer_bar = function (method, element) {
    if (element) {
        this_ = $(element);
        // var ajaxUrlRaw = this_.attr('rawUrl') + this_.val() + '/';

        // alert('raw: ' + ajaxUrlRaw);
        var data = {
            'days': this_.val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        };
        redraw = true;
    }
    else {
        var redraw = false;
    }
    var endPoint_customer = '/agentjs/';

    $.ajax({
        method: method,
        url: endPoint_customer,
        data: data,

        success: function (data_obj) {
            var newData = [];
            Object.keys(data_obj).forEach(function (key) {
                console.log('customer data: ' + key, data_obj[key]);
                newData.push({
                    label: data_obj[key].customer_name,
                    value: data_obj[key].kw,
                });
            });

            do_chart_bar(redraw, newData, 'a', 'customer_bar', 'درخواست های دریافتی');
        },
        error: function (error_data) {
            alert('errors: ' + error_data);
            console.log('error: ' + error_data);
        },
    });
};

function do_chart(redraw, params, yk, chartElement, lables) {
//    do chart stuff
    config.data = params;
    config.ykeys = [yk];
    config.xLabel = ['day'];
    config.element = chartElement;
    config.labels = [lables];
    if (redraw === false) {
        if (chartElement === 'area-chart') {
            req_chart_obj = Morris.Line(config);
            console.log('req rendered');
        }
        if (chartElement === 'line-chart') {
            prof_chart_obj = Morris.Line(config);
            console.log('prof rendered');
        }
        if (chartElement === 'payment-line-chart') {
            payment_chart_obj = Morris.Line(config);
            console.log('payment rendered');
        }
        console.log('redraw: ' + redraw);
    }
    else {
        console.log('params: ' + params);
        if (chartElement === 'area-chart') {
            req_chart_obj.setData(params);
            console.log('req rendered again');
        }
        if (chartElement === 'line-chart') {
            prof_chart_obj.setData(params);
            console.log('prof rendered again');
        }
        if (chartElement === 'payment-line-chart') {
            payment_chart_obj.setData(params);
            console.log('payment rendered again');
        }

        console.log('redraw: ' + redraw);

    }
}

function do_chart_bar(redraw, params, yk, chartElement, lables) {
//    do chart stuff
    config.data = params;
    config.element = chartElement;
    config.labels = [lables];
    if (redraw === false) {
        customer_pie = Morris.Donut(config);
    } else {
        customer_pie.setData(params);
    }
}

console.log('config data: ' + config.data);
update_chart('GET', false);
customer_bar('GET', false);
$('#ajaxbtn2').click(function (e) {
    e.preventDefault();
    update_chart('POST', '#dayNumers_noajax');
    customer_bar('POST', '#dayNumers_noajax');
});

// console.log('this is what you want: ' + aData);
// config.element = 'line-chart';
// Morris.Line(config);
// config.element = 'bar-chart';
// Morris.Bar(config);
// config.element = 'stacked';
// config.stacked = true;
// Morris.Bar(config);
// Morris.Donut({
//     element: 'pie-chart',
//     data: [
//         {label: "Friends", value: 30},
//         {label: "Allies", value: 15},
//         {label: "Enemies", value: 45},
//         {label: "Neutral", value: 10}
//     ]
// });

