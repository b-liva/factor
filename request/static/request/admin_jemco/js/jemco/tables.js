$(document).ready(function () {
// var tabledata = [
//  	{id:1, name:"Oli Bob", age:"12", col:"red", dob:""},
//  	{id:2, name:"Mary May", age:"1", col:"blue", dob:"14/05/1982"},
//  	{id:3, name:"Christine Lobowski", age:"42", col:"green", dob:"22/05/1982"},
//  	{id:4, name:"Brendon Philips", age:"125", col:"orange", dob:"01/08/1980"},
//  	{id:5, name:"Margret Marmajuke", age:"16", col:"yellow", dob:"31/01/1999"},
//  ];
//create Tabulator on DOM element with id "example-table"
// var table = new Tabulator("#example-table", {
//  	height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
//  	data:tabledata, //assign data to table
//  	layout:"fitColumns", //fit columns to width of table (optional)
//  	columns:[ //Define Table Columns
// 	 	{title:"Name", field:"name", width:150},
// 	 	{title:"Age", field:"age", align:"left", formatter:"progress"},
// 	 	{title:"Favourite Color", field:"col"},
// 	 	{title:"Date Of Birth", field:"dob", sorter:"date", align:"center"},
//  	],
//  	rowClick:function(e, row){ //trigger an alert message when the row is clicked
//  		alert("Row " + row.getData().id + " Clicked!!!!");
//  	},
// });

    // $('#ReqSearchBtn').click(function (e) {
    //     e.preventDefault();
    //     spec_search('POST');
    // });

    var spec_search = function (method) {
        // define data here
        // var date_start = $('#date_fa').val();
        // var date_end = $('#exp_date_fa').val();
        // var kw_min = $('#id_kw_min').val();
        // var kw_max = $('#id_kw_max').val();
        // var rpm = $('#id_rpm').val();
        // var price = $('#id_price').val();
        // var tech = $('#id_tech').val();
        // var permission = $('#id_permission').val();
        // var sent = $('#id_sent').val();

        var dataObj = {
            'customer_name': $('#id_customer_name').val(),
            'date_min': $('#date_fa').val(),
            'date_max': $('#exp_date_fa').val(),
            'kw_min': $('#id_kw_min').val(),
            'kw_max': $('#id_kw_max').val(),
            'rpm': $('#id_rpm').val(),
            'price': $('#id_price').prop("checked"),
            'tech': $('#id_tech').prop("checked"),
            'permission': $('#id_permission').prop("checked"),
            'sent': $('#id_sent').prop("checked"),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        };
        console.log(dataObj);
        var url = '/request/fsearch2';

        $.ajax({
            method: method,
            url: url,
            data: dataObj,

            success: function (data_obj) {
                console.log(data_obj);
                // Object.keys(data_obj).forEach(function (key) {
                //     console.log(key, data_obj[key]);
                // });
                var table = new Tabulator("#example-table", {
                    height: 205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                    data: data_obj, //assign data to table
                    layout: "fitData",
                    // layout: "fitColumns", //fit columns to width of table (optional)
                    columns: [ //Define Table Columns
                        {title: "Qty", field: "qty", formatter:"cellClassFormatter"},
                        {title: "kw", field: "kw"},
                        {title: "rpm", field: "rpm"},
                        {title: "voltage", field: "voltage"},
                        {title: "Name", field: "customer_name"},
                        {title: "reqno", field: "reqNo"},
                        {title: "price", field: "price"},
                        {title: "tech", field: "tech"},
                        {title: "delay", field: "delay"},
                        // {title:"Age", field:"age", align:"left", formatter:"progress"},
                        // {title:"Favourite Color", field:"col"},
                        // {title:"Date Of Birth", field:"dob", sorter:"date", align:"center"},
                    ],
                    // rowClick: function (e, row) { //trigger an alert message when the row is clicked
                    //     alert("Row " + row.getData().id + " Clicked!!!!");
                    // },
                });
            },
            error: function (error_data) {
                // alert('errors: ' + error_data);
                console.log('error: ' + error_data);
            },
        });
    };

    //create custom formatter
    var cellClassFormatter = function (cell, formatterParams) {
            //cell - the cell component
            //formatterParams - parameters set for the column

            cell.getElement().addClass("custom-class");

            return cell.getValue(); //return the contents of the cell;
        };
    // spec_search('POST');

});