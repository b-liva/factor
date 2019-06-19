Vue.component('sales_comparison', {
    data() {
        return {
            msg: '',
            name: 'some name',
            show: true,
            loading: '',
            response: '',
            date_min: '',
            date_max: '',
            val: '',
            details: '',
        }
    },
    template: "<div>" +
        "<input id='date_fa' class='' type='text' :value='date_min' name='date_min'>{{date_min}}" +
        "<input id='exp_date_fa' class='' type='text' name='date_max'>{{date_max}}" +
        "<button @click='getPerms'>بروزرسانی</button>" +
        "<div v-if='details'>details</div>" +
        "<div v-if='response' class='col-md-10 col-md-offset-1'>" +
        "<table class='table table-hover text-center'>" +
        "<thead>" +
        "<tr>" +
        "<td>نام</td>" +
        "<td>تعداد</td>" +
        "<td>کیلووات</td>" +
        "<td>مبلغ</td>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<tr v-for='res in response' @click='expData(res.id)'>" +
        "<td>{{res.name}}</td>" +
        "<td>{{res.count}}</td>" +
        "<td>{{pretty(res.kw)}}</td>" +
        "<td>{{pretty(res.price)}}" +
        "</td>" +
        "</tr>" +
        "</tbody>" +
        "</table>" +
        "</div>" +

        "</div>",

    props: {},
    created() {
        this.debouncedGetData = _.debounce(this.getPerms, 700);
    },
    beforeCreate() {
        console.log('entered');
    },
    beforeMount() {
    },
    mounted() {
    },
    computed: {},
    watch: {
        date_min: function () {
            this.msg = 'در حال ورود اطلاعات';
            this.debouncedGetData();
        }
    },
    methods: {
        pretty: function(value){
            return numeral(value).format('0,0')
        },
        expData: function(value){
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
