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
                        <v-form ref="req_form">
                            <v-text-field label="شماره" type="number" v-model="reqData.number"
                                          :rules="titleRules"></v-text-field>
                            <date-picker v-model="reqData.date"></date-picker>

                            <v-autocomplete
                                    v-model="reqData.customer.id"
                                    label="مشتری"
                                    :items="customersListDropDown"
                                    item-value="id"
                                    item-text="name"
                                    :rules="required"
                            ></v-autocomplete>
                            <v-textarea label="جزئیات" prepend-icon="edit" v-model="reqData.details"></v-textarea>
                            <v-btn class="success mx-0 mt-3" @click="submit" :loading="reqData.submitting">ذخیره
                            </v-btn>
                            <v-btn class="success mx-0 mt-3" @click="clearForm" :loading="reqData.submitting">
                                پاکسازی
                                فرم
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-flex>
                <v-flex v-if="reqData.show || true" md8>
                    <reqSpec
                            :spec-prop="specs"
                            ret="reqSpecComponent"
                            @rowsSaved="finilize"
                    ></reqSpec>
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
                error: '',
                reqData: {
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
                required: [v => !!v || 'فیلد اجباری'],
                dialog: false,
            }
        },
        methods: {
            saveRequest() {
                if (this.$refs.req_form.validate() && this.reqData.date != '') {
                    const url = 'api/v2/requests/';
                    let params = {
                        "number": this.reqData.number,
                        "customer": this.reqData.customer.id,
                        "date_fa": this.reqData.date,
                        "is_active": true,
                        "summary": this.reqData.details
                    };
                    axios.post(url, params).then(
                        (response) => {
                            console.log('success');
                            console.log(response);
                            if (response.status == 201) {
                                this.$emit('request_added', {
                                    'msg': 'درخواست با موفقیت ثبت گردید.',
                                    'color': 'success',
                                });
                            }

                        },
                        (error) => {
                            this.error = error;
                            console.log(error.response);
                            let msg = 'خطایی رخ داده است.';
                            this.$emit('request_added', {
                                'msg': msg,
                                'color': 'warning',
                            });
                        }
                    )
                }

            },
            saveSpecs() {
                let params = {
                    'specs': this.specs,
                };
                console.log('saveSpecs should be implemented...');
                console.log(params.specs);
            },
            submit() {
                if (this.$refs.req_form.validate()) {
                    this.reqData.submitting = true;
                    console.log('Data: ');
                    this.saveRequest();
                    this.saveSpecs();

                    this.reqData.submitting = false;

                    this.reqData.show = true;
                }
            },
            clearForm() {
            },
            finilize(e) {
                console.log('finilize');
                console.log(e);
                this.specs = e;
            },
            getCustomer() {
                this.customersListDropDown = [];
                const url = 'api/v2/customers/';
                let params = {
                    'name': this.reqData.customer.name,
                };
                axios.get(url).then((respons) => {
                    console.log(respons);
                    this.customersListDropDown = respons.data;
                }, (error) => {
                    console.log(error);
                });
            },

        },
        components: {
            datePicker: VuePersianDatetimePicker,
            reqSpec: reqSpec,
        },
        beforeCreate() {
            console.log('before create');
        },
        created() {
            this.debouncedGetCustomer = _.debounce(this.getCustomer, 700);
            this.getCustomer();
            console.log('Created.');
        },
        beforeMount() {
            console.log('before mount');
        },
        mounted() {
            console.log('moundte.');
        },
        // watch: {
        //     'reqData.customer.name': function () {
        //         console.log(this.reqData.customer.name);
        //         this.debouncedGetCustomer();
        //     }
        // },
    }
</script>