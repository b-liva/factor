Vue.component('customer_index', {
    data() {
        return {
            delay: 500,
            msg: '',
            customerName: '',
            call: '',
            err: false,
            loading: false,
            customers: [],
            cus: {
                status: false,
                details: '',
                search_name: '',
            },
        }
    },

    props: {
        customer_id: '',
    },
    template: "<div>" +
        "<p>{{cus}}</p>" +
        "<div v-if='cus.status' class='row'><div  id=\"customerDetails\" class=\"col-md-3 col-sm-3 col-xs-12 col-xs-offset-0\">" +
        "<div class='row'><h3 class='pull-right'><a class=\"btn btn-warning\" href='#'>{{cus.details.name}}</a></h3>" +
        "<i class='pull-left fa fa-close' @click='cus.status=!cus.status'></i></div>" +
        "<p><i class=\"fa fa-calendar\" aria-hidden=\"true\"></i> جمع دریافت شده: {{cus.details.total_received}}</p>" +
        "<p><i class=\"fa fa-calendar\" aria-hidden=\"true\"></i> تعداد: {{cus.details.perm_qty_delivered.count}}</p>" +
        "<p><i class=\"fa fa-calendar\" aria-hidden=\"true\"></i> معادل ریالی ارسال شده: {{cus.details.perm_qty_delivered.sent_value}}</p>" +
        "<p><i class=\"fa fa-globe\" aria-hidden=\"true\"></i>" +
        "<a style=\"color: yellow;\" href=\"{{ customer.website }}\"> جمع قابل دریافت: {{cus.details.total_receivable}}</a>" +
        "</p>" +
        "</div></div>" +
        "<p v-if='loading'>Loading</p>" +
        "<p v-else>{{err}}</p>" +
        "<p v-if='err' @click='err=!err'>بروز خطا</p>" +
        "<div class='col-md-4'><input type='text' v-model='customerName' class='form-control'></div>" +
        "<div class='col-md-3'><span v-if='msg'>{{msg}}</span><span v-if='loading'>{{loading}}</span></div>" +
        "<table class=\"table table-hover text-center\">" +
        "<thead class=\"text-center\">" +
        "<tr class=\"text-center\">" +
        "<th class=\"text-center\">ردیف</th>" +
        "<th class=\"text-center\">کد مشتری</th>" +
        "<th class=\"text-center\">کد تدوین</th>" +
        "<th class=\"text-center\">نام</th>" +
        "<th class=\"text-center\">تلفن</th>" +
        "<th class=\"text-center\">owner</th>" +
        "<th class=\"text-center\">تاریخ عضویت</th>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr @click='c_details(customer)' v-for='customer in customers'>" +
        "<td>{{ customer.id }}</td>" +
        "<td>{{ customer.name }}</td>" +
        "<td><div>{{ customer.total_receivable }}</div>" +
        "</td>" +
        "</tr>" +
        "</tbody>" +
        "</table>" +
        "<button @click='refresh'>refresh</button>" +
        "<button @click='getCustomersApi'>getCustomers</button>" +
        "</div>",
    created() {
        this.debouncedGetCustomer = _.debounce(this.getCustomers, 500);
    },
    beforeCreate() {
    },
    beforeMount() {
    },
    mounted() {
    },
    computed: {},
    watch: {
        customerName: function () {
            this.msg = 'در حال ورود اطلاعات';
            this.debouncedGetCustomer();
        }
    },
    methods: {
        c_details: function (customer) {
            this.customer = customer;
            this.loading = 'در حال جستجو';
            console.log('refresh clicked...');
            axios.post('/customer/customer-details-vue', params = {
                'id': this.customer.id,
            }).then((result) => {
                if (!result.data.response.err) {
                    this.cus.details = result.data.response;
                    console.log(this.cus);
                    this.cus.status = true;
                }
                else {
                    this.err = result.data.response.err;
                }
                this.loading = null;
            }, (error) => {
                this.err = true;
                this.loading = null;
                console.log(error)
            })

        },
        refresh: function () {
            this.loading = true;
            console.log('refresh clicked...');
            axios.post('/customer/index-vue-refresh', params = {}).then((result) => {
                this.customers = result.data.response;
                console.log(this.customers);
                this.loading = false;
                this.cus.search_name = '';
                this.customerName = '';
            }, (error) => {
                console.log(error)
            })
        },
        getCustomers: function (e) {
            this.msg = null;
            this.loading = 'در حال جستجو';

            if (this.call) {
                console.log(this.call);
                this.call.cancel();
            }
            this.call = axios.CancelToken.source();
            var url = '/customer/customer-search-vue';
            var params = {
                'name': this.customerName,
                // 'name': this.cus.search_name,
            };

            axios.post(url, params, {cancelToken: this.call.token}).then((result) => {
                this.loading = 'در حال بارگذاری';
                console.log(this.loading);

                if (!result.data.response.err) {
                    this.customers = result.data.response;
                    this.err = false;
                }
                else {
                    this.err = result.data.response.err;
                }
                this.loading = false;
            }, (error) => {
                this.err = true;
                this.loading = false;
                console.log(error)
            })
        },
        getCustomersApi: function () {
            this.loading = true;
            axios.get('api/customer/').then((response) => {
                this.customers = response.data;
                this.loading = false;
            }).catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
    }
});

const cindex = new Vue({
    delimiters: ['[[', ']]'],
    el: '#customerindex',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
