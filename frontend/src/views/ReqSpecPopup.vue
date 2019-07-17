<template>
    <div>
        <v-card-title>
            <h2>ثبت ردیف درخواست</h2>
        </v-card-title>
        <v-card-text>
            <v-form ref="form">
                <v-layout row wrap>
                    <v-flex md1><v-text-field :disabled="!specData.editable" label="id" type="number" v-model="specData.id"></v-text-field></v-flex>
                    <v-flex md1><v-text-field :disabled="!specData.editable" label="تعداد" type="number" v-model="specData.qty"></v-text-field></v-flex>
                    <v-flex md1><v-text-field :disabled="!specData.editable" label="کیلووات" type="number" v-model="specData.kw"></v-text-field></v-flex>
                    <v-flex md1><v-text-field :disabled="!specData.editable" label="سرعت" type="number" v-model="specData.rpm"></v-text-field></v-flex>
                    <v-flex md1><v-text-field :disabled="!specData.editable" label="ولتاژ" type="number" v-model="specData.voltage"></v-text-field></v-flex>
                    <v-flex md6><v-textarea :disabled="!specData.editable" label="جزئیات" prepend-icon="edit" v-model="specData.details"></v-textarea></v-flex>
                </v-layout>
                <v-layout row>
                    <v-btn class="success mx-0 mt-3" @click="submit" :loading="specData.submitting">ذخیره</v-btn>
                    <v-btn class="success mx-0 mt-3" @click="specData.editable = !specData.editable" :loading="specData.submitting">toggle</v-btn>
                </v-layout>

            </v-form>
            <div v-for="(spec, index) in specs" :id="spec.id">
                {{spec.qty}} - {{spec.kw}} - {{spec.rpm}} <v-btn fab dark small color="primary"><v-icon dark @click="removeTask(index)">remove</v-icon></v-btn>
            </div>
            <div>{{specs}}</div>

        </v-card-text>
    </div>


</template>

<script>

    export default {
        data() {
            return {
                specData: {
                    id: '',
                    kw: '',
                    rpm: '',
                    voltage: '',
                    qty: '',
                    date: '',
                    title: '',
                    submitting: false,
                    show: false,
                    editable: false,
                },
                specs: [],
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
            }
        },
        methods: {
            submit: function () {
                this.specs.push(this.specData);
            },
            removeTask: function (index) {
                this.specs.splice(index, 1)
            }
        },
        components: {},
    }
</script>