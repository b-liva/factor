<template>
    <v-dialog max-width="600px" v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-btn flat slot="activator" class="success">ثبت دریافتی</v-btn>
        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon dark @click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
                <v-card-title><h2>ثبت مبلغ دریافتی</h2></v-card-title>
            </v-toolbar>
            <v-layout row wrap>
                <v-flex md4>
                    <v-card-text>
                        <v-form ref="form">
                            <v-text-field label="شماره پیش فاکتور" type="number"
                                          v-model="profData.number"></v-text-field>
                            <date-picker v-model="incomeData.date"></date-picker>
                            <v-textarea label="جزئیات" prepend-icon="edit" v-model="incomeData.details"></v-textarea>
                            <v-btn class="success mx-0 mt-3" @click="submit" :loading="incomeData.submitting">ذخیره
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-flex>
                <v-flex v-if="incomeData.show" md8>
                    <v-layout row>
                        <v-flex md6>
                            <div>قیمت کل: {{profData.totalPrice_no_vat}}</div>
                            <div>ارزش افزوده: {{profData.totalPrice_vat}}</div>
                            <div>قابل پرداخت: {{profData.totalPrice}}</div>
                            <div v-for="(spec, index) in profData.specs" v-if="spec.show">
                                {{index}}: {{spec.qty}} - {{spec.kw}} - {{spec.rpm}} - {{spec.price}}
                                <!--<v-icon @click="addToProforma(income)">add</v-icon><br/>-->
                            </div>
                        </v-flex>
                        <v-flex md6>
                            <div v-for="(income, index) in profData.incomes">
                                <span>پرداخت مبلغ {{income.amount}} ریال با شماره پرداخت {{income.number}} در تاریخ {{income.date}} به صورت {{income.type}}
                                </span>
                                <span><v-icon @click="editIncome(index)">edit</v-icon></span>
                                <span><v-icon @click="removeIncome(index)">delete</v-icon></span>
                            </div>
                        </v-flex>
                    </v-layout>


                    <v-layout>
                        <v-flex md2>
                            <v-text-field
                                    label="شماره دریافتی"
                                    v-model="incomeData.number"
                            ></v-text-field>
                        </v-flex>
                        <v-flex md3>
                            <date-picker
                                    label="تاریخ"
                                    v-model="incomeData.date"
                            ></date-picker>
                        </v-flex>
                        <v-flex md2>
                            <v-text-field
                                    label="مبلغ"
                                    v-model="incomeData.amount"
                            ></v-text-field>
                        </v-flex>
                        <v-flex md1>
                            <v-text-field
                                    label="نوع"
                                    v-model="incomeData.type"
                            ></v-text-field>
                        </v-flex>
                    </v-layout>
                    {{incomeData}}
                </v-flex>
            </v-layout>
        </v-card>
    </v-dialog>

</template>

<script>
    import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
    import _ from 'underscore';

    export default {
        data() {
            return {
                profData: {
                    totalPrice_no_vat: 250000,
                    totalPrice_vat: 22000,
                    totalPrice: 290000,
                    number: '',
                    date: '',
                    customer: '',
                    details: '',
                    show: false,
                    specs: [
                        {'id': 10, 'qty': 2, 'kw': 132, 'rpm': 1500, 'price': 2000, 'voltage': 400, 'show': true},
                        {'id': 11, 'qty': 1, 'kw': 160, 'rpm': 1000, 'price': 3000, 'voltage': 380, 'show': true},
                        {'id': 12, 'qty': 3, 'kw': 315, 'rpm': 3000, 'price': 5000, 'voltage': 400, 'show': true},
                        {'id': 13, 'qty': 2, 'kw': 75, 'rpm': 1500, 'price': 6000, 'voltage': 380, 'show': true},
                    ],
                    incomes: [
                        {'id': 5, 'number': 20000, 'amount': 33453, 'date': '1398/02/03', 'type': 'نقد'},
                        {'id': 6, 'number': 200, 'amount': 65451, 'date': '1398/02/03', 'type': 'نقد'}
                    ],
                },
                incomeDataTemplate: {
                    show: false,
                    editing: false,
                    number: '',
                    amount: '',
                    details: '',
                    date: '',
                    type: '',

                },
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
                dialog: false,
            }
        },
        methods: {
            submit() {
                if (this.$refs.form.validate()) {
                    this.profData.submitting = true;
                    let paramData = {
                        'income': this.incomeData,
                        'prof': this.profData,
                    };
                    console.log('Data to serve: ', paramData);
                    this.profData.submitting = false;
                    this.$emit('income_added', {
                        'msg': 'دریافتی با موفقیت ثبت گردید.',
                        'color': 'success',
                    });
                    this.profData.show = true;
                    if ('id' in this.incomeData) {
                        this.incomeData = this.incomeDataTemplate;
                        this.incomeData.show = true;
                    }else {
                        this.profData.incomes.push({...this.incomeData})
                    }
                    this.incomeData = {...this.incomeDataTemplate};
                }
            },
            getProfData() {
                console.log('fn: getProformaData using this number: ' + this.profData.number);
                this.incomeData.show = true;
            },
            saveProforma: function () {
                console.log('اطلاعات قابل ثبت');
                console.log(this.profData);
            },
            addToProforma(reqSpec) {
                console.log(reqSpec);
                console.log(this.profData);
                this.profData.specs.push(reqSpec);
                this.profData.show = true;
                reqSpec.show = false;
            },
            editIncome(index) {
                console.log('editing');
                console.log(this.profData.incomes[index].amount);

                this.incomeData.editing = true;
                this.incomeData = this.profData.incomes[index];
                this.incomeData.show = true;
            },
            removeIncome(index) {
                console.log('remove icon: ', index);
                this.profData.incomes.splice(index, 1);
                //    todo: delete call to the server and before that confirm via a popup.
                console.log('send remove signal to server.');
            }
        },
        components: {
            datePicker: VuePersianDatetimePicker,
        },
        created() {
            this.incomeData = this.incomeDataTemplate;
            this.debouncedGetProfData = _.debounce(this.getProfData, 700);
        },
        watch: {
            'profData.number': function (val) {
                this.debouncedGetProfData();
            }
        },
    }
</script>