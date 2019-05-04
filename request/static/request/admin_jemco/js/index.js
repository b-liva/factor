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

    var ajaxUrlRaw = this_.attr('rawUrl') + days + '/';

    var data = {
        'days': this_.val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    };

    $.ajax({
        method: 'POST',
        url: endPoint,
        data: data,
        success: function (data_obj) {
            var newData = [];
            var ProformaData = [];

            Object.keys(data_obj).forEach(function (key) {
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
            config.data = newData;
            do_chart(true, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            chart.redraw();
        },
        error: function (error_data) {
            console.log('error: ' + error_data);
        },
    });
});

var update_chart = function (method, element) {

    if (element) {
        this_ = $(element);
        var days = this_.val();

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


            do_chart(redraw, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            do_chart(redraw, ProformaData, 'b', 'line-chart', 'پیش فاکتورهای صادر شده');
            do_chart(redraw, paymentData, 'a', 'payment-line-chart', 'پرداخت های انجام شده');
        },
        error: function (error_data) {
            console.log('error: ' + error_data);
        },
    });
};

var customer_bar = function (method, element) {
    if (element) {
        this_ = $(element);

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
                // console.log('customer data: ' + key, data_obj[key]);
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
        // request rendered
        if (chartElement === 'area-chart') {
            req_chart_obj = Morris.Bar(config);
        }
        // prof rendered
        if (chartElement === 'line-chart') {
            prof_chart_obj = Morris.Bar(config);
        }
        // payment rendered
        if (chartElement === 'payment-line-chart') {
            payment_chart_obj = Morris.Bar(config);
        }
    }
    else {
        // console.log('params: ' + params);
        if (chartElement === 'area-chart') {
            req_chart_obj.setData(params);
        }
        if (chartElement === 'line-chart') {
            prof_chart_obj.setData(params);
        }
        if (chartElement === 'payment-line-chart') {
            payment_chart_obj.setData(params);
        }

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

update_chart('GET', false);
customer_bar('GET', false);
$('#ajaxbtn2').click(function (e) {
    e.preventDefault();
    update_chart('POST', '#dayNumers_noajax');
    customer_bar('POST', '#dayNumers_noajax');
});

