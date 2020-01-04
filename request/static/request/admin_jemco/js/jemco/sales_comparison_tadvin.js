Vue.component('sales_comparison_tadvin', {
    data() {
        return {
            msg: '',
            computing: false,
            name: 'some name',
            show: true,
            response: '',
            project_base: '',
            perms_count: '',
            date_min: '',
            date_max: '',
            total_sales_by_owner: '',
            total_qty: '',
            total_perms_count: '',
            val: '',
            details: '',
            total_received: '',
            total_receivable: '',
            by_date: true,
            days: 30,
            perms: {},
            date_picker: $('#date_fa').persianDatepicker(),
        }
    },

    template: "<div>" +
        "<div v-if=''>" +

        "<input id='date_fa' class='' type='text' name='date_min' :disabled=\"computing == true\">{{date_min}}" +
        "<input id='exp_date_fa' class='' type='text' name='date_max' :disabled=\"computing == true\">{{date_max}}" +
        "<button @click='getPerms' v-if='!computing'>بروزرسانی</button>" +
        "<input id='dayes' class='' type='text' name='days' v-model='days' :disabled=\"computing == true\">" +
        "<div class=\"load-wrapp\" v-if='computing'>\n" +
        "            <div class=\"load-1\">\n" +
        "                <div class=\"line\"></div>\n" +
        "                <div class=\"line\"></div>\n" +
        "                <div class=\"line\"></div>\n" +
        "            </div>\n" +
        "        </div>" +
        "</div>" +
        "<div v-if='details'>details</div>" +
        "<div v-if='response' class='col-md-10 col-md-offset-1'>" +
        "<h3>کارشناس</h3>" +
        "<table class='table table-hover text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>نام</td>" +
        "<td>تعداد</td>" +
        "<td>دستگاه</td>" +
        "<td>کیلووات</td>" +
        "<td>مبلغ</td>" +
        "<td>دریافتی</td>" +
        "<td>درصد</td>" +
        "<td>مانده</td>" +
        "<td>درصد</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<template  v-for='res in response'>" +

        "<tr @click='res.show_details = !res.show_details; getDetails(res.owner.id, res.show_details)'>" +
        "<td>{{res.owner.name}}</td>" +
        "<td>{{res.count}}</td>" +
        "<td>{{res.ps_qty}}</td>" +
        "<td></td>" +

        "<td>{{pretty(res.price)}}</td>" +
        "<td>{{pretty(res.perms_total_received)}} </td>" +
        "<td>{{pretty(100*res.perms_total_received/res.price, '0,0.00')}}</td>" +
        "<td>{{pretty(res.price - res.perms_total_received)}}</td>" +
        "<td>{{pretty(100*(res.price - res.perms_total_received)/res.price, '0,0.00')}}</td>" +
        "</tr>" +

        "<tr v-if='res.show_details'>" +
        "<td colspan='8'><table class='table tableFull text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>شماره</td>" +
        "<td colspan='5'>مشتری</td>" +
        "<td>جمع پیش فاکتور</td>" +
        "<td>دریافت شده</td>" +
        "<td>درصد</td>" +
        "<td>مانده</td>" +
        "<td>درصد</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr v-for='perm in perms[res.owner.id]'>" +
        "<td><a :href='perm.url' class='badge badge-light'>{{perm.perm_number}}</a></td>" +
        "<td colspan='5'>{{perm.customer}}</td>" +
        "<td>{{pretty(perm.proforma_total)}}</td>" +
        "<td>{{pretty(perm.total_received)}}</td>" +
        "<td>{{pretty(100 * perm.total_received / perm.proforma_total, '0,0.00')}}</td>" +
        "<td>{{pretty(perm.total_remainder)}}</td>" +
        "<td>{{pretty(100 * perm.total_remainder / perm.proforma_total, '0,0.00')}}</td>" +
        "</tr>" +
        "</tbody>" +
        "</table></td>" +
        "</tr>" +
        "</template>" +
        "<tr>" +
        "<td>جمع</td>" +
        "<td>{{pretty(total_perms_count)}}</td>" +
        "<td>{{pretty(total_qty)}}</td>" +
        "<td></td>" +
        "<td>{{pretty(total_sales_by_owner)}}</td>" +
        "<td>{{pretty(total_received)}}</td>" +
        "<td></td>" +
        "<td>{{pretty(total_remainder)}}</td>" +
        "</tr>" +

        "</tbody>" +
        "</table>" +
        "<h3>وضعیت فروش براساس نوع پروژه</h3>" +
        "<table class='table table-hover text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>نوع پروژه</td>" +
        "<td>تعداد دستگاه</td>" +
        "<td>کیلووات</td>" +
        "<td>قیمت</td>" +
        "<td>درصد از فروش</td>" +
        "<td>قیمت هر کیلووات</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr v-for='type in project_base'>" +
        "<td>{{type.type}}</td>" +
        "<td>{{pretty(type.count)}}</td>" +
        "<td>{{pretty(type.kw)}}</td>" +
        "<td>{{pretty(type.price)}}</td>" +

        "<td>{{pretty(type.price / type.kw)}}</td>" +
        "</tr>" +
        "<td>جمع</td>" +

        "</tbody>" +
        "</table>" +
        "</div>" +

        "</div>",

    props: {
        user_data: '',
    },
    created() {
        this.debouncedGetData = _.debounce(this.getPerms, 700);
        // this.getPerms();
    },
    beforeCreate() {
    },
    beforeMount() {
    },
    mounted() {
    },
    computed: {},
    watch: {
        // date_min: function () {
        //     this.msg = 'در حال ورود اطلاعات';
        //     this.debouncedGetData();
        // }
        days: function () {
            this.msg = 'در حال ورود اطلاعات';
            this.by_date = false;
            this.debouncedGetData();
        }
    },
    methods: {
        total_fn: function (element) {
            let sum = 0;
            this.response.forEach(function (e) {
                sum += e[element];
            });
            return sum;
        },
        total: function (element) {
            let sum = 0;
            this.project_base.forEach(function (e) {
                sum += e[element];
            });
            return sum;
        },
        pretty: function (value, format) {
            return numeral(value).format(format)
        },
        expData: function (value) {
            this.details = true;
            console.log(value);
        },
        getPerms: function () {
            this.computing = true;
            if (this.by_date) {
                this.date_min = $("input[name=date_min]").val();
                this.date_max = $("input[name=date_max]").val();
            }

            url = 'request/fetch-sales-data-tadvin';
            params = {
                'date_min': this.date_min,
                'date_max': this.date_max,
                'days': this.days,
                'by_date': this.by_date,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            };
            console.log(params);
            axios.post(url, params)
                .then((result) => {
                    console.log(result);
                    this.response = result.data.response;
                    console.log(this.response);
                    this.project_base = result.data.project_base;
                    this.perms_count = result.data.perms_count;
                    this.date_min = result.data.date_min;
                    this.date_max = result.data.date_max;
                    this.total_sales_by_owner = result.data.total_sales_by_owner;
                    this.total_qty = result.data.total_qty;
                    this.total_perms_count = result.data.total_perms_count;
                    this.total_received = result.data.total_received;
                    this.total_remainder = result.data.total_remainder;
                    $("input[name=date_min]").val(this.date_min);
                    $("input[name=date_max]").val(this.date_max);
                    // this.days = result.data.diff_days;
                    this.computing = false;
                    this.days.stop = result.data.diff_days;
                    this.by_date = true;

                }, (error) => {
                    console.log(error);
                    this.by_date = true;
                    this.computing = false;
                })
        },
        printData: function () {
            console.log('date selected');
            console.log(this.date_min);
        },
        getDetails: function (id, show_details) {
            if (!show_details){
                return 0;
            }
            this.computing = true;
            this.msg = '';
            if (this.by_date) {
                this.date_min = $("input[name=date_min]").val();
                this.date_max = $("input[name=date_max]").val();
            }

            url = 'request/fetch-sales-data-tadvin-per-owner';
            params = {
                'date_min': this.date_min,
                'date_max': this.date_max,
                'days': this.days,
                'by_date': this.by_date,
                'id': id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            };
            console.log(params);
            axios.post(url, params)
                .then((result) => {
                    console.log(result);
                    this.perms[id] = result.data.details;
                    // this.days = result.data.diff_days;
                    this.computing = false;

                }, (error) => {
                    console.log(error);
                    this.by_date = true;
                    this.computing = false;
                })
        }
    }
});

const sales_tadvin = new Vue({
    delimiters: ['[[', ']]'],
    el: '#sales_comparison_tadvin',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";