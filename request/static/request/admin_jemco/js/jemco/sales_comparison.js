Vue.component('sales_comparison', {
    data() {
        return {
            msg: '',
            name: 'some name',
            show: true,
            loading: false,
            response: '',
            project_base: '',
            perms_count: '',
            date_min: '',
            date_max: '',
            val: '',
            details: '',
            total_received: '',
            total_receivable: '',
            by_date: true,
            days: 30,
            date_picker: $('#date_fa').persianDatepicker(),
        }
    },
    template: "<div>" +
        "<div v-if=''>" +
        // "<input id='date_fa' class='' type='text' :value='date_min' name='date_min'>{{date_min}}" +
        "<input id='date_fa' class='' type='text' name='date_min'>{{date_min}}" +
        "<input id='exp_date_fa' class='' type='text' name='date_max'>{{date_max}}" +
        "<button @click='getPerms'>بروزرسانی</button>" +
        "<input id='dayes' class='' type='text' name='days' v-model='days'>{{days}}({{by_date}})<br>{{msg}}" +
        "</div>" +
        "<div v-if='details'>details</div>" +
        "<div v-if='response' class='col-md-10 col-md-offset-1'>" +
        "<h3>کارشناس</h3>" +
        "<table class='table table-hover text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>نام</td>" +
        "<td>تعداد</td>" +
        "<td>تعداد2</td>" +
        "<td>دستگاه</td>" +
        "<td>کیلووات</td>" +
        "<td>مبلغ</td>" +
        "<td>دریافتی</td>" +
        "<td>مانده</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<template  v-for='res in response'>" +

        "<tr @click='res.show_details = !res.show_details'>" +
        "<td>{{res.name}}</td>" +
        "<td>{{res.count}}</td>" +
        "<td>{{res.ps_count}}</td>" +
        "<td>{{res.ps_qty}}</td>" +
        "<td>{{pretty(res.kw)}}" +
        " ({{pretty(100*res.kw/total_fn('kw'), '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.price)}}" +
        " ({{pretty(100*res.price/total_fn('price'), '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.perms_total_received)}} ({{pretty(100*res.perms_total_received/res.price, '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.price - res.perms_total_received)}} ({{pretty(100*(res.price - res.perms_total_received)/res.price, '0,0.00')}}%)</td>" +
        "</tr>" +

        "<tr v-if='res.show_details'>" +
        "<td colspan='8'><table class='table tableFull text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>شماره</td>" +
        "<td colspan='5'>مشتری</td>" +
        "<td>جمع پیش فاکتور</td>" +
        "<td>دریافت شده</td>" +
        "<td>مانده</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr v-for='perm in res.perms'>" +
        "<td><a :href='perm.url' class='badge badge-light'>{{perm.perm_number}}</a></td>" +
        "<td colspan='5'>{{perm.customer}}</td>" +
        "<td>{{pretty(perm.proforma_total)}}</td>" +
        "<td>{{pretty(perm.total_received)}}({{pretty(perm.total_received_percentage)}}%)</td>" +
        "<td>{{pretty(perm.perm_receivable)}}({{pretty(perm.perm_receivable_percentage)}}%)</td>" +
        "</tr>" +
        "</tbody>" +
        "</table></td>" +
        "</tr>" +
        "</template>" +
        "<tr>" +
        "<td>جمع</td>" +
        "<td>{{total_fn('count')}}</td>" +
        "<td>{{total_fn('ps_count')}}</td>" +
        "<td>{{total_fn('ps_qty')}}</td>" +
        "<td>{{pretty(total_fn('kw'))}}</td>" +
        "<td>{{pretty(total_fn('price'))}} ({{pretty(total_fn('price') / total_fn('kw'))}} بر kw)</td>" +
        "<td>{{pretty(total_fn('perms_total_received'))}}" +
        " ({{pretty(100*total_fn('perms_total_received')/total_fn('price'), '0,0.00')}}%)</td>" +
        "<td>{{pretty(total_fn('price') - total_fn('perms_total_received'))}}" +
        " ({{pretty(100*(total_fn('price') - total_fn('perms_total_received'))/total_fn('price'), '0,0.00')}}%)</td>" +
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
        "<td>{{pretty(100*type.price / total('price'), '0,0.00')}}%</td>" +
        "<td>{{pretty(type.price / type.kw)}}</td>" +
        "</tr>" +
        "<td>جمع</td>" +
        "<td>{{pretty(total('count'))}}</td>" +
        "<td>{{pretty(total('kw'))}}</td>" +
        "<td>{{pretty(total('price'))}}</td>" +
        "</tbody>" +
        "</table>" +
        "</div>" +

        "</div>",

    props: {
        user_data: '',
    },
    created() {
        this.debouncedGetData = _.debounce(this.getPerms, 700);
        this.getPerms();
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
            this.loading = true;
            this.msg = '';
            if (this.by_date) {
                this.date_min = $("input[name=date_min]").val();
                this.date_max = $("input[name=date_max]").val();
            }

            url = 'request/fetch-sales-data';
            params = {
                'date_min': this.date_min,
                'date_max': this.date_max,
                'days': this.days,
                'by_date': this.by_date,
            };
            axios.post(url, params)
                .then((result) => {
                    console.log(result);
                    this.response = result.data.response;
                    this.project_base = result.data.project_base;
                    this.perms_count = result.data.perms_count;
                    this.date_min = result.data.date_min;
                    this.date_max = result.data.date_max;
                    $("input[name=date_min]").val(this.date_min);
                    $("input[name=date_max]").val(this.date_max);
                    // this.days = result.data.diff_days;
                    this.loading = false;
                    this.days.stop = result.data.diff_days;
                    this.by_date = true;

                }, (error) => {
                    console.log(error);
                    this.by_date = true;
                })
        },
        printData: function () {
            console.log('date selected');
            console.log(this.date_min);
        },
        getDate: function () {
            alert('clicked...')
        }
    }
});

const sales = new Vue({
    delimiters: ['[[', ']]'],
    el: '#sales_comparison',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
