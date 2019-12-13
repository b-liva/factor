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

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
