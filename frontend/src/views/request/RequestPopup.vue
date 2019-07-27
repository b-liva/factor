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
                            <v-text-field label="مشتری" prepend-icon="people" v-model="reqData.customer"
                                          :rules="titleRules"></v-text-field>
                            <v-textarea label="جزئیات" prepend-icon="edit" v-model="reqData.details"></v-textarea>
                            <v-btn class="success mx-0 mt-3" @click="submit" :loading="reqData.submitting">ذخیره</v-btn>
                        </v-form>
                    </v-card-text>
                </v-flex>
                <v-flex v-if="reqData.show || true" md8>
                    <reqSpec
                            @rowsSaved="finilize"
                    ></reqSpec>
                </v-flex>
                <v-layout row wrap>
                    <h1>درخواست</h1>
                    <div>{{reqData}}</div>
                </v-layout>
                <v-layout row wrap>
                    <h1>ردیف ها</h1>
                    <div v-for="spec in specs">{{spec}}</div>
                </v-layout>

            </v-layout>
        </v-card>
    </v-dialog>

</template>

<script>
    import VuePersianDatetimePicker from 'vue-persian-datetime-picker'
    import reqSpec from './ReqSpec'

    export default {
        data() {
            return {
                reqData: {
                    number: '',
                    date: '',
                    customer: '',
                    details: '',
                    submitting: false,
                    show: false,
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
                    this.reqData.submitting = true;
                    console.log(this.reqData);
                    this.reqData.submitting = false;
                    this.$emit('request_added', {
                        'msg': 'درخواست با موفقیت ثبت گردید.',
                        'color': 'success',
                    });
                    this.reqData.show = true;
                }
            },
            finilize(e) {
                console.log('finilize');
                console.log(e);
                this.specs = e;
            },
        },
        components: {
            datePicker: VuePersianDatetimePicker,
            reqSpec: reqSpec,
        },
    }
</script>