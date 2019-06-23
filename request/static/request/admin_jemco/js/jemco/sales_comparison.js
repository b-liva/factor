Vue.component('sales_comparison', {
    data() {
        return {
            msg: '',
            name: 'some name',
            show: true,
            loading: '',
            response: '',
            project_base: '',
            date_min: '',
            date_max: '',
            val: '',
            details: '',
            total_received: '',
            total_receivable: '',
        }
    },
    template: "<div>" +
        "<div v-if='user_data'>" +
        "<input id='date_fa' class='' type='text' :value='date_min' name='date_min'>{{date_min}}" +
        "<input id='exp_date_fa' class='' type='text' name='date_max'>{{date_max}}" +
        "<button @click='getPerms'>بروزرسانی</button>" +
        "</div>" +
        "<div v-if='details'>details</div>" +
        "<div v-if='response' class='col-md-10 col-md-offset-1'>" +
        "<h3>کارشناس</h3>" +
        "<table class='table table-hover text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>نام</td>" +
        "<td>تعداد</td>" +
        "<td>کیلووات</td>" +
        "<td>مبلغ</td>" +
        "<td>دریافتی</td>" +
        "<td>مانده</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr v-for='res in response' @click='expData(res.id)'>" +
        "<td>{{res.name}}</td>" +
        "<td>{{res.count}}</td>" +
        "<td>{{pretty(res.kw)}}" +
        " ({{pretty(100*res.kw/total_fn('kw'), '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.price)}}" +
        " ({{pretty(100*res.price/total_fn('price'), '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.perms_total_received)}} ({{pretty(100*res.perms_total_received/res.price, '0,0.00')}}%)</td>" +
        "<td>{{pretty(res.price - res.perms_total_received)}} ({{pretty(100*(res.price - res.perms_total_received)/res.price, '0,0.00')}}%)</td>" +
        "</tr>" +
        "<tr>" +
        "<td>جمع</td>" +
        "<td>{{total_fn('count')}}</td>" +
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
    },
    beforeCreate() {},
    beforeMount() {},
    mounted() {},
    computed: {},
    watch: {
        // date_min: function () {
        //     this.msg = 'در حال ورود اطلاعات';
        //     this.debouncedGetData();
        // }
    },
    methods: {
        total_fn: function(element){
            let sum = 0;
          this.response.forEach(function (e) {
             sum += e[element];
          });
          return sum;
        },
        total: function(element){
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
            this.loading = 'loading';
            this.date_min = $("input[name=date_min]").val();
            this.date_max = $("input[name=date_max]").val();
            url = 'request/fetch-sales-data';
            params = {
                'date_min': this.date_min,
                'date_max': this.date_max,
            };
            console.log(params);
            axios.post(url, params)
                .then((result) => {
                    console.log(result);
                    this.response = result.data.response;
                    this.project_base = result.data.project_base;
                    this.loading = '';

                }, (error) => {
                    console.log(error);
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
