<template>
    <v-dialog max-width="600px" v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-btn flat slot="activator" class="success">ثبت پیش فاکتور</v-btn>
        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon dark @click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
                <v-card-title><h2>ثبت پیش فاکتور</h2></v-card-title>
            </v-toolbar>
            <v-layout row wrap>
                <v-flex md4>
                    <v-card-text>
                        <v-form ref="form">
                            <v-text-field label="شماره درخواست" type="number" v-model="reqData.number"></v-text-field>
                            <date-picker v-model="profData.date"></date-picker>
                            <v-textarea label="جزئیات" prepend-icon="edit" v-model="profData.details"></v-textarea>
                            <v-checkbox
                                    v-model="profData.perm.status"
                                    label="مجوز"
                                    @change="profData.perm.number = profData.perm.date = profData.perm.due_date = '' "
                            >
                            </v-checkbox>
                            <template v-if="profData.perm.status">
                                <v-text-field
                                        v-model="profData.perm.number"
                                        label="شماره مجوز"
                                ></v-text-field>
                                <date-picker v-model="profData.perm.date"></date-picker>
                                <date-picker v-model="profData.perm.due_date"></date-picker>

                            </template>
                            <v-btn class="success mx-0 mt-3" @click="submit" :loading="profData.submitting">ذخیره
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-flex>
                <v-flex v-if="reqData.show" md8>
                    <div v-for="(rspec, index) in specs" v-if="rspec.show">
                        {{index}}: {{rspec.code}} - {{rspec.qty}} - {{rspec.kw}} - {{rspec.rpm}} - {{rspec.price}} - {{rspec.modified}} - TF:{{rspec.show}}
                        <v-icon @click="addToProforma(rspec)">add</v-icon>
                        <br/>
                    </div>
                    <v-btn @click="addAllToProforma">all
                        <v-icon>add</v-icon>
                    </v-btn>
                    <ProformaSpecRow
                            v-if="profData.show"
                            :row="profData"
                            @specRemoved="showReqSpec"
                    ></ProformaSpecRow>

                    <h2>profData</h2>
                    {{profData}}
                    <h2>reqData</h2>
                    {{reqData}}
                </v-flex>
            </v-layout>
        </v-card>
    </v-dialog>

</template>

<script>
    import axios from 'axios';
    import VuePersianDatetimePicker from 'vue-persian-datetime-picker';
    import ProformaSpecRow from './ProformaSpecRow';
    import _ from 'underscore';

    export default {
        data() {
            return {
                profData: {
                    number: '',
                    date: '',
                    customer: '',
                    details: '',
                    submitting: false,
                    show: false,
                    specs: [],
                    perm: {
                        status: false,
                        number: '',
                        date: '',
                        due_date: '',
                    }
                },
                reqData: {
                    show: false,
                    number: '',
                    specs: [],
                    specsOld: [
                        {
                            'id': 10,
                            'qty': 2,
                            'kw': 132,
                            'rpm': 1500,
                            'voltage': 400,
                            'show': true,
                            'price': 1000000,
                            'sentQty': 0,
                            'modified': false
                        },
                        {
                            'id': 11,
                            'qty': 1,
                            'kw': 160,
                            'rpm': 1000,
                            'voltage': 380,
                            'show': true,
                            'price': 1500000,
                            'sentQty': 0,
                            'modified': false
                        },
                        {
                            'id': 12,
                            'qty': 3,
                            'kw': 315,
                            'rpm': 3000,
                            'voltage': 400,
                            'show': true,
                            'price': 2000000,
                            'sentQty': 0,
                            'modified': false
                        },
                        {
                            'id': 13,
                            'qty': 2,
                            'kw': 75,
                            'rpm': 1500,
                            'voltage': 380,
                            'show': true,
                            'price': 3000000,
                            'sentQty': 0,
                            'modified': false
                        },
                    ],
                },
                specs: [],
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
                        'request': this.reqData,
                        'prof': this.profData,
                    };
                    console.log('Data to serve: ', paramData);
                    this.profData.submitting = false;
                    this.$emit('proforma_added', {
                        'msg': 'پیش فاکتور با موفقیت ثبت گردید.',
                        'color': 'success',
                    });
                    this.profData.show = true;
                }
            },
            getSpecs() {
                const url = 'api/v2/requests/' + this.reqData.number + '/reqspecs';
                console.log(url);
                axios.get(url).then(
                    (response) => {
                        this.specs = [];
                        response.data.forEach((spec) => {
                            spec.show = true;
                            console.log(spec);
                            this.specs.push(spec);
                        });
                        console.log(this.specs);
                    },
                    (error) => {
                        console.log('error')
                    }
                )
            },
            getReqData() {
                const url = 'api/v2/requests/' + this.reqData.number;
                axios.get(url).then(
                    (response) => {
                        console.log(response);
                        this.reqData = response.data;
                        this.reqData.show = true;
                        this.getSpecs();
                    },
                    (error) => {
                        console.log(error);
                    });

            },
            saveProforma: function () {
                console.log('اطلاعات قابل ثبت');
                console.log(this.profData);
            },
            addAllToProforma: function () {
                let list = [];
                this.profData.show = true;
                this.specs.forEach((e) => {
                    list.push(e);
                    e.show = false;
                });
                // this.reqData.specs.forEach(function (e) {
                //     list.push(e);
                //     e.show = false;
                // });
                this.profData.specs = list;
            },
            addToProforma(reqSpec) {
                console.log(reqSpec);
                console.log(this.profData);
                this.profData.specs.push(reqSpec);
                this.profData.show = true;
                reqSpec.show = false;
            },
            showReqSpec(id) {
                let result = this.specs.filter(object => {
                    return object.id === id;
                });
                result[0].show = true;
            }
        },
        components: {
            datePicker: VuePersianDatetimePicker,
            ProformaSpecRow: ProformaSpecRow,
        },
        created() {
            this.debouncedGetReqData = _.debounce(this.getReqData, 700);
        },
        watch: {
            'reqData.number': function () {
                this.debouncedGetReqData();
            }
        },
    }
</script>