<template>
    <div class="proformas">
        <v-snackbar v-model="snackbar" :timeout="4000" top :color="msgColor">
            <span>{{ msg }}</span>
            <v-btn flat color="white">بستن</v-btn>
        </v-snackbar>
        <h1 class="subheading grey--text">مبالغ دریافتی</h1>

        <IncomePopup @income_added="incomeAdd"></IncomePopup>
        <v-container fluid class="my-5">
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
                    <v-btn color="success" @click="getIncomes">جستجو</v-btn>
                </v-flex>
                <v-flex>
                    <template>
                        <v-progress-linear
                                :indeterminate="flags.incomesLoading || flags.incomesLoading"></v-progress-linear>
                    </template>
                </v-flex>
                <v-flex v-if="response.length != 0">
                    <v-data-table
                            :headers="headers"
                            :items="response"
                            class="elevation-1"
                            item-key="number"
                            fluid
                    >
                        <template v-slot:items="props">
                            <tr @click="expandIncomes(props)">
                                <td class="text-xs-right">{{props.item.number}}</td>
                                <td class="text-xs-right">{{props.item.customer}}</td>
                                <td class="text-xs-right">{{props.item.total_kw}}</td>
                                <td class="text-xs-right">{{props.item.details}}</td>
                                <td class="text-xs-right">{{props.item.owner}}</td>
                            </tr>
                            <!--<td>{{ props.item.name }}</td>-->
                        </template>
                        <template slot="expand" scope="props">
                            <v-data-table
                                    :headers="expanded_headers"
                                    :items="specs"
                                    item-key="qty"
                                    class="elevation-1"
                                    fluid
                            >
                                <template v-slot:items="newprops">
                                    <tr v-if="flags.specsLoading">
                                        <td colspan="6" class="text-xs-center"><h3>در حال بروزرسانی</h3></td>
                                    </tr>
                                    <tr v-else>
                                        <td class="text-xs-right">{{newprops.item.qty}}</td>
                                        <td class="text-xs-right">{{newprops.item.kw}}</td>
                                        <td class="text-xs-right">{{newprops.item.rpm}}</td>
                                        <td class="text-xs-right">{{newprops.item.voltage}}</td>
                                        <td class="text-xs-right">{{newprops.item.ic}}</td>
                                        <td class="text-xs-right">{{newprops.item.im}}</td>
                                    </tr>
                                    <!--<td>{{ props.item.name }}</td>-->
                                </template>
                            </v-data-table>
                        </template>
                        <template slot="footer">
                            <td><strong>جمع</strong></td>
                            <td><strong>{{count}}</strong></td>
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
    import IncomePopup from './IncomePopup'

    export default {
        data() {
            return {
                headers: [
                    {align: 'right', value: 'number', text: 'شماره'},
                    {align: 'right', value: 'customer', text: 'مشتری'},
                    {align: 'right', value: 'amount', text: 'مبلغ'},
                ],
                expanded_headers: [
                    {align: 'right', value: 'qty', text: 'تعداد'},
                    {align: 'right', value: 'kw', text: 'کیلووات'},
                    {align: 'right', value: 'rpm', text: 'سرعت'},
                    {align: 'right', value: 'voltage', text: 'ولتاژ'},
                    {align: 'right', value: 'ic', text: 'ic'},
                    {align: 'right', value: 'im', text: 'im'},
                ],
                msg: '',
                name: 'some name should be gone here...',
                show: true,
                flags: {
                    loading: false,
                    incomeLoading: false,
                },
                response: [],
                specs: [],
                perms_count: '',
                date_min: '',
                date_max: '',
                val: '',
                details: '',
                total_received: '',
                total_receivable: '',
                by_date: true,
                days: 30,
                count: 0,
                request_number: 0,
                snackbar: false,
                msgColor: '',
            }
        },
        props: {},
        created() {
            this.debouncedGetData = _.debounce(this.getIncome, 700);
        },
        beforeCreate() {
        },
        beforeMount() {
        },
        mounted() {
        },
        computed: {},
        components: {
            datePicker: VuePersianDatetimePicker,
            IncomePopup: IncomePopup,
        },
        watch: {
            days: function () {
                this.msg = 'در حال ورود اطلاعات';
                this.by_date = false;
                this.debouncedGetData();
            }
        },
        methods: {
            incomeAdd: function (v) {
                this.snackbar = true;
                this.msg = v.msg;
                this.msgColor = v.color;
            },
            total_fn: function (element) {
                let sum = 0;
                this.response.forEach(function (e) {
                    sum += e[element];
                });
                return sum;
            },
            pretty: function (value, format) {
                return numeral(value).format(format)
            },
            getIncomes: function () {
                this.flags.incomesLoading = true;
                this.msg = '';

                const url = 'api/payments/index';
                let params = {
                    // 'date_min': this.date_min.replace(new RegExp('/', 'gi'), '-'),
                    // 'date_max': this.date_max.replace(new RegExp('/', 'gi'), '-'),
                    'days': this.days,
                    'by_date': this.by_date,
                    // 'by_date': true,
                };
                axios.post(url, params)
                    .then((result) => {
                        console.log(result);
                        this.response = result.data.incomes;
                        this.count = result.data.count;
                        // this.perms_count = result.data.perms_count;
                        this.date_min = result.data.date_min;
                        this.date_max = result.data.date_max;
                        $("input[name=date_min]").val(this.date_min);
                        $("input[name=date_max]").val(this.date_max);
                        // this.days = result.data.diff_days;
                        this.days = result.data.diff_days;
                        this.flags.incomesLoading = false;

                    }, (error) => {
                        this.by_date = true;
                        this.flags.incomesLoading = false;
                    })
            },
        }
    }

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";
</script>

