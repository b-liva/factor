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
    ykeys: ['a', 'b'],
    labels: ['درخواست های دریافتی', 'Money received'],
    fillOpacity: 0.6,
    hideHover: 'auto',
    behaveLikeLine: true,
    resize: true,
    pointFillColors: ['#ffffff'],
    pointStrokeColors: ['black'],
    lineColors: ['gray', 'red'],
    xLabel: ['day'],
};

console.log('this is old data: ' + data);

var endPoint = '/kwjs/';

$('#ajaxbtn').click(function (e) {
    e.preventDefault();
    this_ = $('#dayNumers');
    var ajaxUrlRaw = this_.attr('rawUrl') + this_.val() + '/';

    alert('raw: ' + ajaxUrlRaw);
    var data = {
        'days': this_.val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    };

    // $.ajax({
    //     method: 'POST',
    //     url: endPoint,
    //
    //     data: data,
    //     success: function (data_obj) {
    //         alert('data: ' + data_obj);
    //         console.log('data: ' + data_obj);
    //         var newData = [];
    //         var temp = {};
    //
    //         Object.keys(data_obj).forEach(function (key) {
    //             console.log(key, data_obj[key]);
    //             newData.push({
    //                 y: key,
    //                 a: data_obj[key],
    //             });
    //         });
    //         // for (var x in data_obj) {
    //         //     console.log('x is: ' + x);
    //         //     temp.y = x;
    //         //     temp.a = data_obj[x];
    //         //     newData.push(temp);
    //         // }
    //         console.log(newData)
    //     },
    //     error: function (error_data) {
    //         alert('errors: ' + error_data);
    //         console.log('error: ' + error_data);
    //     },
    // });


    $.ajax({
        method: 'POST',
        url: endPoint,
        data: data,
        success: function (data_obj) {
            alert('success_data: ' + data_obj);
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
                        ProformaData.push({
                            y: k,
                            b: data_obj[key][k],
                        });
                    }
                });
            });
            console.log(newData);
            console.log(ProformaData);
            config.data = newData;
            do_chart(true, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            do_chart(true, ProformaData, 'b', 'line-chart', 'پیش فاکتورهای صادر شده');
            // chart.setDate(newData);
            chart.redraw();


        },
        error: function (error_data) {
            alert('failure');

            alert('errors: ' + error_data);
            console.log('error: ' + error_data);
        },
    });

});

var test = function () {
    $.ajax({
        method: 'GET',
        url: endPoint,
        success: function (data_obj) {
            console.log('data: ' + data_obj);
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
                        ProformaData.push({
                            y: k,
                            b: data_obj[key][k],
                        });
                    }
                });
            });
            console.log(newData);
            console.log(ProformaData);
            config.data = newData;
            do_chart(false, newData, 'a', 'area-chart', 'درخواست های دریافتی');
            do_chart(false, ProformaData, 'b', 'line-chart', 'پیش فاکتورهای صادر شده');
            // chart.setDate(newData);
            // chart.redraw();


        },
        error: function (error_data) {
            alert('errors: ' + error_data);
            console.log('error: ' + error_data);
        },
    });
};

function do_chart(redraw, params, yk, chartType, lables) {
//    do chart stuff
    config.data = params;
    config.ykeys = [yk];
    config.xLabel = ['day'];
    config.element = chartType;
    config.labels = [lables];
    // config.element = 'area-chart';
    // line = Morris.Area(config);
    if (redraw === false) {
        area = Morris.Line(config);
    }
    else {
        area.redraw();
    }
    // setData(params);
    // chart.setData(data);
    // chart.redraw();
}

console.log('config data: ' + config.data);
// var aData = test();
test();
console.log('this is what you want: ' + aData);

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