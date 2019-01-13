axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
const app = new Vue({
        delimiters: ['[[', ']]'],
        el: '.searchApp',
        data: {
            answerClass: '',
            question: '',
            specs: [],
            answer: '',
            extra_info: {
                total_kw: '',
                total_qty: '',
            },
            // specs: '',
            filter: {
                price: false,
                tech: false,
                sent: false,
                permission: false,
                kw_min: '',
                kw_max: '',
                customer: '',
                rpm: '',
            },
            pprice: false,
            ttech: false,
            currentSort: 'name',
            currentSortDir: 'asc',
            pageSize: 30,
            currentPage: 1
        },
        watch: {
            filter: {
                handler: function () {
                    this.answerClass = 'alert alert-warning';
                    this.answer = 'در حال ورود اطلاعات';
                    this.debounceDoSearch();
                },
                deep: true,
            }
        },
        created: function () {
            // fetch('https://api.myjson.com/bins/s9lux')
            // fetch("http://localhost:8000/request/fsearch2")

            console.log('vue instance created');
            // specs = this.doSearch2();
            // this.debaounceDoSearch = _.debounce(this.doSearch(), 500)
            this.debounceDoSearch = _.debounce(function () {
                this.doSearch();
            }, 1000);
            // this.doSearch();
        },
        methods: {
            sort: function (s) {
                //if s == current sort, reverse
                if (s === this.currentSort) {
                    this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
                }
                this.currentSort = s;
            },
            nextPage: function () {
                if ((this.currentPage * this.pageSize) < this.specs.length) this.currentPage++;
            },
            prevPage: function () {
                if (this.currentPage > 1) this.currentPage--;
            },
            checkbox: function (value) {
                console.log(value);
            },
            // debounceDoSearch: function(){
            //     _.debounce(function () {
            //         this.doSearch();
            //     }, 500)
            // },
            doSearch: function () {
                this.answerClass = 'alert alert-info';
                this.answer = 'در حال جستجو.';

                var newData = {
                    'price': this.filter.price,
                    'tech': this.filter.tech,
                    // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                };
                console.log('search started WITH THIS DATA: ' + newData);
                //
                console.log(newData);

                axios.post('/request/fsearch2', params = {
                    'price': this.filter.price,
                    'tech': this.filter.tech,
                    'sent': this.filter.sent,
                    'permission': this.filter.permission,
                    'customer_name': this.filter.customer,
                    'kw_min': this.filter.kw_min,
                    'kw_max': this.filter.kw_max,
                    'rpm': this.filter.rpm,
                    // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                })
                // .then(res => res.json())
                    .then(res => {
                        this.specs = res.data.response;
                        this.extra_info.total_kw = res.data.total_kw;
                        this.extra_info.total_qty = res.data.total_qty;
                        this.extra_info.rpm = res.data.rpm;
                        // this.filter.rpm = res.data.rpm;
                        console.log(res);
                        this.answerClass = 'alert alert-success';
                        this.answer = 'اطلاعات بروز رسانی گردید.';

                    });
                // this.$http.get("/request/fsearch2", newData)
                //     .then(res => res.json())
                //     .then(res => {
                //         this.specs = res;
                //         console.log("res: " + res)
                //     })

            }
            ,
            doSearch2: function () {
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
                var newData = {
                    'price': this.filter.price,
                    'tech': this.filter.tech,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                };
                $.ajax({
                    method: 'POST',
                    url: '/request/fsearch2',
                    data: dataObj,
                    success: function (data_obj) {
                        console.log(data_obj);
                        return data_obj;
                    },
                });
            }
            ,
        },
        computed: {
            sortedSpecs: function () {
                return this.specs.sort((a, b) => {
                    let modifier = 1;
                    if (this.currentSortDir === 'desc') modifier = -1;
                    if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
                    if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
                    return 0;
                }).filter((row, index) => {
                    let start = (this.currentPage - 1) * this.pageSize;
                    let end = this.currentPage * this.pageSize;
                    if (index >= start && index < end) return true;
                });
            }
        }
    })
;