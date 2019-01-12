const app = new Vue({
    delimiters: ['[[', ']]'],
    el: '.searchApp',
    data: {
        specs: [],
        filter: {
            'price': false,
            'tech': false,
        },
        pprice: false,
        ttech: false,
        currentSort: 'name',
        currentSortDir: 'asc',
        pageSize: 20,
        currentPage: 1
    },
    created: function () {
        // fetch('https://api.myjson.com/bins/s9lux')
        // fetch("http://localhost:8000/request/fsearch2")


        // specs = this.doSearch2();
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
        doSearch: function () {
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
            // var dataObj = {
            //     'price': price,
            //     'tech': tech,
            //     'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            // };

            console.log(dataObj);
            var newData = {
                'price': this.filter.price,
                'tech': this.filter.tech,
                // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            };
            this.$http.push("/request/fsearch2", newData)
                .then(res => res.json())
                .then(res => {
                    this.specs = res;
                    console.log("res: " + res)
                })
        },
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
            // var dataObj = {
            //     'price': price,
            //     'tech': tech,
            //     'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            // };

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
        },
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
});