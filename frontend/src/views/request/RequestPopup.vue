<template>
    <v-dialog max-width="600px" v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">

        <v-btn flat slot="activator" class="success">ثبت سفارش فروش جدید</v-btn>

        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon dark @click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
                <v-card-title><h2>ثبت سفارش فروش جدید</h2></v-card-title>
            </v-toolbar>
            <v-layout row wrap>
                <v-flex md4>

                    <v-card-text>
                        <v-form ref="form">
                            <v-text-field label="شماره" type="number" v-model="reqData.number"></v-text-field>
                            <date-picker v-model="reqData.date"></date-picker>
                            <v-text-field :id="reqData.customer.id" label="مشتری" prepend-icon="people" v-model="reqData.customer.name"
                                          :rules="titleRules"></v-text-field>
                            <v-textarea label="جزئیات" prepend-icon="edit" v-model="reqData.details"></v-textarea>
                            <v-btn class="success mx-0 mt-3" @click="submit" :loading="reqData.submitting">ذخیره</v-btn>
                            <v-btn class="success mx-0 mt-3" @click="clearForm" :loading="reqData.submitting">پاکسازی فرم</v-btn>
                        </v-form>
                    </v-card-text>
                </v-flex>
                <v-flex v-if="reqData.show || true" md8>
                    <reqSpec
                            :spec-prop="specs"
                            ret="reqSpecComponent"
                            @rowsSaved="finilize"
                    ></reqSpec>

                    <div>
                        <ol>
                            <li v-for="customer in customersListDropDown">{{customer}}</li>
                        </ol>
                    </div>
                </v-flex>
            </v-layout>
            <v-layout row wrap>
                <h1>درخواست</h1>
                <div>{{reqData}}</div>
            </v-layout>
            <v-layout row wrap>
                <h1>ردیف ها</h1>
                <div v-for="spec in specs">{{spec}}</div>
            </v-layout>
        </v-card>
    </v-dialog>

</template>

<script>
    import axios from 'axios'
    import _ from 'underscore'
    import VuePersianDatetimePicker from 'vue-persian-datetime-picker'
    import reqSpec from './ReqSpec'

    export default {
        data() {
            return {
                reqTemplate: {
                    number: '',
                    date: '',
                    customer: {
                        id: '',
                        name: '',
                    },
                    details: '',
                    submitting: false,
                    show: false,
                },
                reqData: '',
                specs: [],
                customersListSimulate: [
                    {id: 1, name: 'هوایار'},
                    {id: 1, name: 'سازش'},
                    {id: 1, name: 'پارس کمپرسور'},
                    {id: 1, name: 'فولاد خوزستان'},
                    {id: 1, name: 'فولاد مبارکه'},
                    {id: 1, name: 'پتروشیمی مارون'},
                    {id: 1, name: 'ام الدبس'},
                ],
                customersListDropDown: [],
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
                dialog: false,
            }
        },
        methods: {
            submit() {
                if (this.$refs.form.validate()) {
                    this.reqData.submitting = true;
                    console.log('Data: ');
                    let dataParam = {
                        'request': this.reqData,
                        'specs': this.specs,
                    };
                    console.log(dataParam);
                    this.reqData.submitting = false;
                    this.$emit('request_added', {
                        'msg': 'درخواست با موفقیت ثبت گردید.',
                        'color': 'success',
                    });
                    this.reqData.show = true;
                }
            },
            clearForm(){
                console.log(this.$parent.$refs.reqSpecComponentt);
                this.customersListDropDown = [];
                this.reqData = {...this.reqTemplate};
                this.specs = [];
            },
            finilize(e) {
                console.log('finilize');
                console.log(e);
                this.specs = e;
            },
            getCustomer(){
                this.customersListDropDown = [];
                console.log('Customer: ', this.reqData.customer);
                this.customersListSimulate.forEach((e) => {
                    if (this.reqData.customer.name.indexOf(e.name) >= 0){
                        this.customersListDropDown.push(e);
                    }
                })
            },

        },
        components: {
            datePicker: VuePersianDatetimePicker,
            reqSpec: reqSpec,
        },
        beforeCreate(){
            console.log('before create');
        },
        created(){
            this.reqData = {...this.reqTemplate};
            console.log(this.reqData);
            this.debouncedGetCustomer = _.debounce(this.getCustomer, 700);
            console.log('Created.');
        },
        beforeMount(){
            console.log('before mount');
        },
        mounted(){
            console.log('moundte.');
        },
        watch:{
            'reqData.customer.name': function (e) {
                console.log(e);
                this.debouncedGetCustomer();
            }
        },
    }
</script>