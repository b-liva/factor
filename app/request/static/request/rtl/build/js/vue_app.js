var data = {
    FundIdModel: '',
    funds: {},
    fund: '',
};

// The object is added to a Vue instance
var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp',
    // data: data
    data: data,
    mounted() {
        // axios
        //     .get('https://api.coindesk.com/v1/bpi/currentprice.json')
        //     .then(response => (this.data = [1, 2]))
        this.getFunds;
        this.getFundDetails;
    },
    methods: {
        getFunds: function () {
            this.loading = true;
            this.$http.get("/api/v1/fund/")
                .then((response) => {
                    vm.funds = response.data;
                    this.loading = false;
                    console.log(this.funds);
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getFundDetails: function () {
            this.loading = true;
            // this.$http.get("/api/v1/fund/" + vm.FundIdModel)
            this.$http.get("/api/v1/fund/" + vm.FundIdModel)
                .then((response) => {
                    this.fund = response.data;
                    this.loading = false;
                    console.log(this.fund);
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
    }
});


$('#fundIdBtn').click(function (e) {
    e.preventDefault();
    var fundId = $('#fundId').val();
    alert(fundId);
    var temp = data.days.push(fundId);
    console.log(temp);
    // ajdata = {
    //     url: '',
    //
    // }
});