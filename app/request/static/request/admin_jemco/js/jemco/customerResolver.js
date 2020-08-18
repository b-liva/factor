Vue.component('customer_resolver', {
    template: "<div><tr>" +
        "<td>{{ customer.c1 }}</td>" +
        "<td>{{ customer.c2 }}</td>" +
        "<td>{{ customer.similarity }}</td>" +
        "<td>" +
        "<input type='checkbox' v-model='customer.resolved' :key='customer.id' @click='update'>{{ customer.resolved }}" +
        "<i v-if='loading' class=\"fa fa-refresh\" aria-hidden=\"true\"></i>" +
        "</td>" +
        "<td>{{ customer.cleared }}</td>" +
        "</tr></div>",
    data() {
        return {
            status: false,
            res: '',
            loading: false,
            customer: {
                key: this.customer_id,
                c1: this.customer_c1,
                c2: this.customer_c2,
                similarity: this.customer_sim,
                resolved: this.customerResolved,
                cleared: this.customerCleared,
                // resolved: false,
            }
        }
    },
    props: {
        customer_id: '',
        customer_c1: '',
        customer_c2: '',
        customer_sim: '',
        customerResolved: Boolean,
        customerCleared: '',
    },
    created() {
    },
    beforeCreate() {
    },
    beforeMount() {
    },
    mounted() {
        // this.customer.resolved = this.customerResolved;
        // console.log(this.customer_c1);
        // console.log(this.customerResolved);
        console.log(this.customer.resolved);
        if (this.customer.resolved == false){
            console.log(this.customer.key + "is: False.....")
        }
        if (this.customer.resolved == true){
            console.log(this.customer.key + "is: True")
        }
    },
    computed: {},

    methods: {
        update: function () {
            this.loading = true;
            console.log('update...');
            axios.post('/ereq/customer-status-update', params = {
                'id': this.customer.key,
                'status': !this.customer.resolved,
            }).then((result) => {
                this.customer.resolved = result.data.resolved;
                this.loading = false;
                console.log(result.data.resolved);
            }, (error) => {
                console.log(error)
            })
        }
    }
});

Vue.component('customer_entered', {
    template: "<div>" +
        "<ul>" +
        "<li v-for='customer in customers'>{{customer}}</li>" +
        "</ul>" +
        "<div @click='refresh' class='btn btn-success'>refresh</div></div>",
    data() {
        return {
            customers: [],
        }
    },
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

    methods: {
        refresh: function () {
            axios.post('/ereq/customer-entered', params = {
            }).then((result) => {
                this.customers = result.data.customers;
            }, (error) => {
                console.log(error)
            })
        }
    }
});
const appl = new Vue({
    delimiters: ['[[', ']]'],
    el: '#customerResolver',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
