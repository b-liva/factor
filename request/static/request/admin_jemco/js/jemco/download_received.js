Vue.component('download_received', {
    data() {
        return {
            msg: '',
            number: '',
            receivedList: [],
            numbersNotFound: [],
            payments: [],
        }
    },
    template: "<div>" +
        "<h2>رسید اسناد</h2>" +
        "<div class='container'>" +
        "<div class='row'>" +
        "<div class='col-md-3'>" +
        "<label for='number'>شماره دریافتی</label>" +
        "<input v-model='number' placeholder='شماره دریافتی' type='number'>" +
        "<button @click='find_and_add(number)' class='btn btn-success'>add</button>" +
        "<div v-if='receivedList.length'>" +
        "<ul>" +
        "<li v-for='r in receivedList'>" +
        "{{r}} <button @click='removeFromList(r)' class='btn btn-xs'>حذف</button>" +
        "</li></ul>" +
        "<button @click='assign' class='btn btn-xs'>پردازش</button></div>" +
        "</div>" +
        "<div class='col-md-5'>" +
        "<div v-if='numbersNotFound.length'>" +
        "<p>یافت نشد</p><ul>" +
        "<li v-for='nfound in numbersNotFound'>" +
        "{{nfound}}</li></ul>" +
        "</div>" +

        "</div>" +
        "<div class='col-md-4'>" +
        "<div v-if='payments.length'>" +
        "<p>مبالغ دریافتی</p><ul>" +
        "<li v-for='found in payments'>" +
        "{{found.id}} - {{found.amount}} - {{found.customer}} <button class='btn btn-warning' @click='removeFromFound(found)'>حذف</button></li></ul>" +
        "</div>" +
        "<button @click='download'>دانلود</button>" +

        "</div>" +
        "</div>" +
        "</div>" +
        "</div>",

    props: {

    },
    created() {
    },
    beforeCreate() {
    },
    beforeMount() {
    },
    mounted() {
    },
    computed: {},
    watch: {

    },
    methods: {
        find_and_add:function (number) {
            this.receivedList.push(number);
            this.number = '';
        },
        removeFromList:function (number) {
            index = this.receivedList.indexOf(number);
            this.receivedList.splice(index, 1);
        },
        removeFromFound:function (item) {
            index = this.payments.indexOf(item);
            this.payments.splice(index, 1);
        },
        download:function () {
            console.log('download');
            url = 'payment_download';
            params = {
                'payments': this.payments
            };
            axios.post(url, params, {responseType: 'blob'})
            // axios({
            //     url: url,
            //     method: 'post',
            //     data: params,
            //     headers: {
            //         'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            //     },
            //     responseType: 'blob', // important
            //     // responseType: 'arraybuffer', // important
            // })
                .then((result) => {
                    console.log(result.data);
                    const url = window.URL.createObjectURL(new Blob([result.data], {type: 'application/vnd.ms-excel'}));
                    const link = document.createElement('a');
                    let blob = new Blob([result.data], {type: 'application/vnd.ms-excel'}); // for excel
                    // let blob = new Blob([result.data], {type: 'application/zip'});
                    link.style.display = 'none';
                    // link.href = url;
                    link.href = URL.createObjectURL(blob);
                    link.setAttribute('download', 'رسید اسناد.xls');
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }, (error) => {
                    console.log(error);
            })
        },
        assign:function () {
            this.receivedList.forEach(function (item) {
                console.log(item);
            });
            url = 'assign';
            params = {
                'payments': this.receivedList,
            };
            axios.post(url, params)
                .then((result) => {
                    console.log(result);
                    this.numbersNotFound = result.data.not_found;
                    this.payments = result.data.payments;
                }, (error) => {
                    console.log(error);
                })

        }
    }
});

const download_received = new Vue({
    delimiters: ['[[', ']]'],
    el: '#download_received',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

Vue.component('find_pref_price', {
    data() {
        return {
            status: false,
            status_no_price: false,
            msg: '',
            number: '',
            data: '',
            data_no_price: '',
            prices: [],
        }
    },
    template: "<div>" +
        "<p @click='find_pref_price(rspec)' style='cursor: pointer; color: #26b99a;'>قیمت قبل</p>" +
        "<div style='height: 200px; width: 100%; overflow: auto; background: #ededed;' v-if='status'>" +
        "<div v-for='price in data.prices'>" +
        "<span>{{price.customer}} - </span><a class='btn btn-success btn-xs' :href='price.url' target='_blank'> {{pretty(price.price)}}</a>" +
        "<span style='float: left;'>({{price.date}})</span>" +
        "</div>" +
        "</div>" +
        "<p @click='find_pref_no_price(rspec)' style='cursor: pointer; color: #d9534f;'>مشابه بدون قیمت</p>" +
        "<div style='height: 200px; width: 100%; overflow: auto; background: #ededed;' v-if='status_no_price'>" +
        "<div v-for='req in data_no_price.requests'>" +
        "<span></span> {{req.customer}} - <a class='btn btn-danger btn-xs' :href='req.url' target='_blank'> {{req.number}}</a>" +
        "<span style='float: left;'>({{req.date}})</span>" +
        "</div>" +
        "</div>" +
        "</div>",

    props: {
        rspec: '',
    },
    created() {
    },
    beforeCreate() {
    },
    beforeMount() {
    },
    mounted() {
    },
    computed: {},
    watch: {

    },
    methods: {
        find_pref_price:function (pk) {
            if (!this.status){
                url = '/request/pref/find_price_by_id';
                params = {
                    'rspec': pk
                };
                axios.post(url, params)
                    .then((result) => {
                        this.data = result.data;
                        this.prices = result.prices;
                        console.log(result);
                        this.status = true;
                    }, (error) => {
                        console.log('error');
                    })
            }else {
                this.status = false;
            }

        },
        find_pref_no_price:function (pk) {
            if (!this.status_no_price){
                url = '/request/pref/find_no_price_by_id';
                params = {
                    'rspec': pk
                };
                axios.post(url, params)
                    .then((result) => {
                        this.data_no_price = result.data;
                        this.requests = result.requests;
                        console.log(result);
                        this.status_no_price= true;
                    }, (error) => {
                        console.log('error');
                    })
            }else {
                this.status_no_price = false;
            }

        },
        pretty: function (value, format) {
            return numeral(value).format(format)
        },
    }
});

const find_pref_price = new Vue({
    delimiters: ['[[', ']]'],
    el: '#find_pref_price',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
