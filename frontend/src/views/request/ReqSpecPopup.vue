<template>
    <div>
        <v-card-title>
            <h2>ثبت ردیف درخواست</h2>
        </v-card-title>
        <v-card-text>
            <req-spec-row
                    v-for="(row, index) in rows"
                    :row="row"
                    v-on:remove="removeRow(index)"
            >

            </req-spec-row>
            <div>
                <v-btn @click="addRow">
                    <v-icon>add</v-icon>
                    ردیف جدید
                </v-btn>
                <v-btn @click="saveRows">
                    <v-icon>add</v-icon>
                    ذخیره درخواست
                </v-btn>
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
                rows: [],
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
            }
        },
        methods: {
            submit: function () {
                this.specs.push(this.specData);
            },
            removeRow: function (index) {
                this.rows.splice(index, 1)
            },
            addRow: function () {
                this.rows.push({
                    id: '',
                    code: '',
                    kw: '',
                    rpm: '',
                    voltage: '',
                    qty: '',
                    date: '',
                    title: '',
                    submitting: false,
                    show: false,
                    editable: true,
                });
            },
            saveRows: function () {
                console.log('دیتای قابل ثبت.');
                console.log(this.reqData);
                console.log(this.rows);
            }
        },
        components: {
            reqSpecRow: reqSpecRow,
        },
    }
</script>