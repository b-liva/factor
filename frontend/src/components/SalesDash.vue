<template>
    <div class="sales">
        <h1 class="subheading grey--text">وضعیت کارشناسان</h1>
        <v-container class="my-5">
            <v-layout
                    text-xs-center
                    wrap
            >
                <v-flex xs3>
                    <date-picker v-model="date_min"></date-picker>
                    <date-picker v-model="date_max"></date-picker>
                    <!--<input class='' type='text' name='days' v-model='days'><br>-->
                </v-flex>

                <v-flex xs3 sm2>
                    <v-text-field
                            v-model="days"
                            label="تعداد روزها"
                            name="days"
                    >
                    </v-text-field>
                </v-flex>
                <v-flex xs2>
                    <v-btn color="success" @click="getPerms">جستجو</v-btn>
                </v-flex>

                <v-flex>

                </v-flex>

                <v-flex v-if="response.length != 0">
                    <h3>کارشناس</h3>

                    <v-data-table
                            :headers="headers"
                            :items="response"
                            class="elevation-1"
                            fluid
                    >
                        <template v-slot:items="props">
                            <tr @click="props.expanded = !props.expanded">
                                <td class="text-xs-right">{{props.item.name}}</td>
                                <td class="text-xs-right">{{props.item.count}}</td>
                                <td class="text-xs-right">{{props.item.ps_count}}</td>
                                <td class="text-xs-right">{{props.item.ps_qty}}</td>
                                <td class="text-xs-right">{{pretty(props.item.kw)}}
                                    ({{pretty(100*props.item.kw/total_fn('kw'), '0,0.00')}}%)
                                </td>
                                <td class="text-xs-right">{{pretty(props.item.price)}}
                                    ({{pretty(100*props.item.price/total_fn('price'), '0,0.00')}}%)
                                </td>
                                <td class="text-xs-right">{{pretty(props.item.perms_total_received)}}
                                    ({{pretty(100*props.item.perms_total_received/props.item.price,
                                    '0,0.00')}}%)
                                </td>
                                <td class="text-xs-right">{{pretty(props.item.price - props.item.perms_total_received)}}
                                    ({{pretty(100*(props.item.price -
                                    props.item.perms_total_received)/props.item.price, '0,0.00')}}%)
                                </td>
                            </tr>
                            <!--<td>{{ props.item.name }}</td>-->
                        </template>
                        <template slot="expand" scope="props">
                            <v-card class="elevation-10">
                                <v-card-text>

                                    <v-data-table :headers="epx_expanded"
                                                  :items="props.item.perms"
                                                  item-key="prof"
                                                  class="elevation-5">
                                        <template slot="items" scope="props">
                                            <td class="text-xs"><a :href="props.item.url" target="_blank">{{
                                                props.item.perm_number }}</a></td>
                                            <td class="text-xs"><a :href="props.item.customer_url" target="_blank">{{
                                                props.item.customer }}</a></td>
                                        </template>
                                    </v-data-table>

                                </v-card-text>
                            </v-card>
                        </template>
                        <template slot="footer">
                            <td><strong>جمع</strong></td>
                            <td class="text-xs-right">{{total_fn('count')}}</td>
                            <td class="text-xs-right">{{total_fn('ps_count')}}</td>
                            <td class="text-xs-right">{{total_fn('ps_qty')}}</td>
                            <td class="text-xs-right">{{pretty(total_fn('kw'))}}</td>
                            <td class="text-xs-right">{{pretty(total_fn('price'))}} ({{pretty(total_fn('price') /
                                total_fn('kw'))}} بر kw)
                            </td>
                            <td class="text-xs-right">{{pretty(total_fn('perms_total_received'))}}" +
                                " ({{pretty(100*total_fn('perms_total_received')/total_fn('price'), '0,0.00')}}%)
                            </td>
                            <td class="text-xs-right">{{pretty(total_fn('price') - total_fn('perms_total_received'))}}"
                                +
                                " ({{pretty(100*(total_fn('price') -
                                total_fn('perms_total_received'))/total_fn('price'),
                                '0,0.00')}}%)
                            </td>
                        </template>
                    </v-data-table>
                </v-flex>


                <v-flex v-if="project_base.length != 0">
                    <h3>وضعیت فروش براساس نوع پروژه</h3>
                    <v-data-table
                            :headers="project_type_headers"
                            :items="project_base"
                            class="elevation-1"
                            fluid
                    >
                        <template v-slot:items="props">
                            <tr @click="props.expanded = !props.expanded">
                                <td class="text-xs-right">{{props.item.type}}</td>
                                <td class="text-xs-right"></td>
                                <td class="text-xs-right">{{pretty(props.item.count)}}</td>
                                <td class="text-xs-right">{{pretty(props.item.kw)}}</td>
                                <td class="text-xs-right">{{pretty(props.item.price)}}</td>
                                <td class="text-xs-right">{{pretty(100*props.item.price / total('price'), '0,0.00')}}%
                                </td>
                                <td class="text-xs-right">{{pretty(props.item.price / props.item.kw)}}</td>
                            </tr>

                        </template>
                        <template slot="expand" scope="props">
                            <!--<template v-slot:expand="props">-->
                            <v-card class="elevation-10">
                                <v-card-text>

                                    <v-data-table :headers="epx_expanded2"
                                                  :items="props.item.pr_perms"
                                                  item-key="customer"
                                                  class="elevation-5">
                                        <template slot="items" scope="props">
                                            <td class="text-xs"><a :href="props.item.url" target="_blank">{{
                                                props.item.number }}</a></td>
                                        </template>
                                    </v-data-table>

                                </v-card-text>
                            </v-card>
                        </template>
                        <template slot="footer">
                            <td><strong>جمع</strong></td>
                            <td class="text-xs-right"></td>
                            <td class="text-xs-right">{{ pretty(total('count')) }}</td>
                            <td class="text-xs-right">{{ pretty(total('kw')) }}</td>
                            <td class="text-xs-right">{{pretty(total('price'))}}</td>
                        </template>

                    </v-data-table>

                </v-flex>

            </v-layout>

        </v-container>
    </div>


</template>

<script>
    import axios from 'axios';
    import _ from 'underscore';
    import $ from 'jquery';
    import VuePersianDatetimePicker from 'vue-persian-datetime-picker'
    import numeral from 'numeral';

    export default {
        data() {
            return {
                headers: [
                    {align: 'right', value: 'name', text: 'نام'},
                    {align: 'right', value: 'perm', text: 'تعداد مجوز'},
                    {align: 'right', value: 'perm2', text: 'تعداد مجوز2'},
                    {align: 'right', value: 'qty', text: 'دستگاه'},
                    {align: 'right', value: 'kw', text: 'کیلووات'},
                    {align: 'right', value: 'amount', text: 'مبلغ'},
                    {align: 'right', value: 'received', text: 'دریافتی'},
                    {align: 'right', value: 'remaining', text: 'مانده'},
                ],
                epx_expanded: [
                    {align: 'right', value: 'prof', text: 'پیش فاکتور'},
                    {align: 'right', value: 'customer', text: 'مشتری'},
                ],
                epx_expanded2: [
                    {align: 'right', value: 'prof', text: 'پیش فاکتور'},
                    {align: 'right', value: 'customer', text: 'مشتری'},
                ],
                project_type_headers: [
                    {align: 'right', value: 'name', text: 'نوع پروژه'},
                    {align: 'right', value: 'perm', text: 'تعداد مجوز'},
                    {align: 'right', value: 'qty', text: 'دستگاه'},
                    {align: 'right', value: 'kw', text: 'کیلووات'},
                    {align: 'right', value: 'price', text: 'قیمت'},
                    {align: 'right', value: 'sales_percent', text: 'درصد از فروش'},
                    {align: 'right', value: 'price_per_kw', text: 'قیمت هر کیلووات'},
                ],
                msg: '',
                name: 'some name should be gone here...',
                show: true,
                loading: false,
                response: [],
                project_base: [],
                perms_count: '',
                date_min: '',
                date_max: '',
                val: '',
                details: '',
                total_received: '',
                total_receivable: '',
                by_date: true,
                days: 30,
            }
        },
        props: {},
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
        components: {
            datePicker: VuePersianDatetimePicker
        },
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

                const url = 'request/fetch-sales-data';
                let params = {
                    'date_min': this.date_min.replace(new RegExp('/', 'gi'), '-'),
                    'date_max': this.date_max.replace(new RegExp('/', 'gi'), '-'),
                    'days': this.days,
                    'by_date': this.by_date,
                    // 'by_date': true,
                };
                console.log(params);
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
                        this.days = result.data.diff_days;
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
            },
        }
    }

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";
</script>

<style>

</style>
