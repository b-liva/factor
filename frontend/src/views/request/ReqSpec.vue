<template>
    <div>
        <v-card-title>
            <h2>ثبت ردیف درخواست</h2>
        </v-card-title>
        <v-card-text>

            <div>
                <v-icon @click="editable = false" v-if="editable">close</v-icon>
                <v-icon @click="editable = true" v-if="!editable">add</v-icon>
                <v-flex md6 v-if="editable">
                    <v-layout row wrap fluid>
                        <v-flex md12>
                            <v-layout row>
                                <v-flex md2>

                                    <v-text-field label="کد" type="number"
                                                  v-model="specData.code"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field label="تعداد" type="number"
                                                  v-model="specData.qty"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field label="کیلووات" type="number"
                                                  v-model="specData.kw"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field label="سرعت" type="number"
                                                  v-model="specData.rpm"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field label="ولتاژ" type="number"
                                                  v-model="specData.voltage"></v-text-field>
                                </v-flex>
                            </v-layout>

                        </v-flex>
                    </v-layout>
                </v-flex>

                <v-btn @click="saveRow">
                    <v-icon>arrow_downward</v-icon>
                </v-btn>
            </div>
            <div>
                <div v-for="(spec, i) in specs">
                    <span>{{spec.qty}}</span> - <span>{{spec.kw}}</span> - <span>{{spec.rpm}}</span> - <span>{{spec.voltage}}</span>
                    <v-icon @click="editRow(i)">edit</v-icon>
                    <v-icon @click="copyRow(i)">file_copy</v-icon>
                    <v-icon @click="removeRow(i)">close</v-icon>
                </div>
            </div>


            <!--<div v-for="row in rows">-->
            <!--{{row.qty}} - {{row.kw}} - {{row.rpm}}-->
            <!--</div>-->

        </v-card-text>
    </div>


</template>

<script>
    import reqSpecRow from './ReqSpecRow'

    export default {
        data() {
            return {
                specData: {
                    id: '',
                    kw: '',
                    rpm: '',
                    voltage: '',
                    qty: '',
                    im: '',
                    ic: '',
                    ie: '',
                    ip: '',
                    date: '',
                    title: '',
                    submitting: false,
                    show: false,
                    editable: true,
                },
                specs: [],
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
                editable: true,
                index: '',
                editing: false,
            }
        },
        methods: {
            removeRow: function (index) {
                this.specs.splice(index, 1)
            },
            saveRow() {
                let sp = {
                    id: this.specData.id,
                    kw: this.specData.kw,
                    rpm: this.specData.rpm,
                    voltage: this.specData.voltage,
                    qty: this.specData.qty,
                    im: this.specData.im,
                    ic: this.specData.ic,
                    ie: this.specData.ie,
                    ip: this.specData.ip,
                    date: this.specData.date,
                    title: this.specData.title,
                    submitting: this.specData.submitting,
                    show: this.specData.show,
                    editable: this.specData.editable,
                };

                if (this.specData.editing) {
                    this.specs[index] = sp;
                }
                if (!this.editing) {
                    this.specs.push(sp);
                }
                this.specData = {
                    id: '',
                    kw: '',
                    rpm: '',
                    voltage: '',
                    qty: '',
                    im: '',
                    ic: '',
                    ie: '',
                    ip: '',
                    date: '',
                    title: '',
                    submitting: false,
                    show: false,
                    editable: true,
                };
                this.editing = false;
                this.$emit('rowsSaved', this.specs);
            },
            saveRows: function () {
                console.log('دیتای قابل ثبت.');
                console.log(this.reqData);
                console.log(this.rows);
            },
            editRow(index) {
                this.specData = this.specs[index];
                this.editing = true;
                this.index = index;
            },
            copyRow(index) {
                this.editing = false;
                this.index = index;
                let sp = Object;
                Object.assign(sp, this.specs[index]);
                this.specData = sp;
            }
        },
        components: {
            reqSpecRow: reqSpecRow,
        },
        computed: {},
        created() {
            this.specDataTemplate = this.specData;
        }
    }
</script>