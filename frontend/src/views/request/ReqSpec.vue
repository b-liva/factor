<template>
    <div>
        <v-card-title>
            <h2>ثبت ردیف درخواست</h2>
        </v-card-title>
        <v-card-text>

            <div>
                <v-icon @click="editable = false" v-if="editable">close</v-icon>
                <v-icon @click="editable = true" v-if="!editable">add</v-icon>
                <v-layout row fluid>
                    <v-flex md6>
                        <v-layout row>
                            <v-flex md12>
                                <v-layout row>
                                    <v-flex md2>

                                        <v-text-field label="نوع موتور" type="text"
                                                      v-model="specData.projectType"></v-text-field>
                                    </v-flex>
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
                                                      v-model="specData.speed"></v-text-field>
                                    </v-flex>
                                    <v-flex md2>
                                        <v-text-field label="ولتاژ" type="number"
                                                      v-model="specData.voltage"></v-text-field>
                                    </v-flex>
                                </v-layout>

                            </v-flex>
                        </v-layout>
                        <v-layout row>
                            <v-flex md3>
                                <v-select
                                        v-model="specData.im"
                                        :items="types.im"
                                        item-value="id"
                                        item-text="title"
                                        label="IM"
                                ></v-select>
                            </v-flex>
                            <v-flex md3>
                                <v-select
                                        v-model="specData.ic"
                                        :items="types.ic"
                                        item-value="id"
                                        item-text="title"
                                        label="IC"
                                ></v-select>
                            </v-flex>
                            <v-flex md3>
                                <v-select
                                        v-model="specData.ip"
                                        :items="types.ip"
                                        item-value="id"
                                        item-text="title"
                                        label="IP"
                                ></v-select>
                            </v-flex>
                            <v-flex md3>
                                <v-select
                                        v-model="specData.ie"
                                        :items="types.ie"
                                        item-value="id"
                                        item-text="title"
                                        label="IE"
                                ></v-select>
                            </v-flex>
                            <v-flex md2>
                                <v-layout row justify-center>
                                    <v-dialog v-model="dialog" max-width="600px">
                                        <v-icon flat slot="activator">add</v-icon>
                                        <v-card>
                                            <v-card-title>
                        <span class="headline">
                            {{specData.qty}} دستگاه الکتروموتور {{specData.kw}} کیلووات {{specData.rpm}} دور
                        </span>
                                            </v-card-title>
                                            <v-card-text>
                                                <v-container grid-list-md>
                                                    <v-textarea
                                                            :disabled="!specData.editable"
                                                            label="جزئیات"
                                                            prepend-icon="edit"
                                                            v-model="specData.details">
                                                    </v-textarea>
                                                </v-container>
                                            </v-card-text>
                                        </v-card>
                                    </v-dialog>

                                </v-layout>
                            </v-flex>
                        </v-layout>

                    </v-flex>
                    <v-flex md6>
                        <ol>
                            <li v-for="(m, index) in motorList">
                                {{m.code}} - {{m.kw}} - {{m.speed}} - {{m.voltage}} -
                                {{m.im}} - {{m.ic}} - {{m.ip}} - {{m.ie}}
                                <v-icon @click="selectFromCode(index)">add</v-icon>
                            </li>
                        </ol>
                    </v-flex>

                </v-layout>

                <v-btn @click="saveRow">
                    <v-icon>arrow_downward</v-icon>
                </v-btn>
            </div>
            <div>
                <div v-for="(spec, i) in specs">
                    <span>{{spec.code}} - {{spec.qty}}</span> - <span>{{spec.kw}}Kw</span> - <span>{{spec.speed}}Rpm</span> -
                    <span>{{spec.voltage}}V</span> - <span>{{spec.details}}</span>
                    <v-icon @click="editRow(i)">edit</v-icon>
                    <v-icon @click="copyRow(i)">file_copy</v-icon>
                    <v-icon @click="removeRow(i)">close</v-icon>
                </div>
            </div>

        </v-card-text>

        {{specData}}
    </div>


</template>

<script>
    import _ from 'underscore'
    import axios from 'axios'
    import reqSpecRow from './ReqSpecRow'

    export default {
        props: ['specProp'],
        data() {
            return {
                template: {
                    id: '',
                    projectType: '',
                    kw: '',
                    speed: '',
                    voltage: '',
                    qty: '',
                    im: '',
                    ic: '',
                    ie: '',
                    ip: '',
                    date: '',
                    title: '',
                    details: '',
                    submitting: false,
                    show: false,
                    editable: true,
                    code: 9999999,
                },
                specData: '',
                specs: this.specProp,
                types: {
                    im: [],
                    ic: [],
                    ip: [],
                    ie: [],
                },
                codes: [
                    {
                        'kw': 132,
                        'rpm': 1500,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 1321500
                    },
                    {
                        'kw': 132,
                        'rpm': 1000,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 1321000
                    },
                    {
                        'kw': 355,
                        'rpm': 1000,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 3551000
                    },
                    {
                        'kw': 355,
                        'rpm': 1500,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 3551500
                    },
                    {
                        'kw': 18.5,
                        'rpm': 3000,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 18.53000
                    },
                    {
                        'kw': 18.5,
                        'rpm': 1500,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 18.51500
                    },
                    {
                        'kw': 160,
                        'rpm': 1500,
                        'voltage': 380,
                        'type': 'روتین',
                        'im': 1,
                        'ic': 1,
                        'ip': 1,
                        'ie': 1,
                        'code': 1601500
                    },
                ],
                fetchedCodes: [],
                motorList: [],
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
                editable: true,
                index: '',
                editing: false,
                dialog: '',
            }
        },
        methods: {
            removeRow: function (index) {
                this.specs.splice(index, 1)
            },
            saveRow() {
                let sp = {
                    ...this.specData,
                };

                if (this.specData.editing) {
                    this.specs[index] = sp;
                }
                if (!this.editing) {
                    this.specs.push(sp);
                }
                this.specData = {
                    ...this.template
                };
                this.editing = false;
                // this.$emit('rowsSaved', this.specs);
            },
            saveRows: function () {
                console.log('دیتای قابل ثبت.');
                console.log(this.reqData);
                console.log(this.rows);
            },
            editRow(index) {
                //todo: editing items from motorCode list not working due to specData.editing property.
                //todo: standard code afeter changing the standard item should be updated.
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
            },
            getIms() {
                const url = 'api/v2/imtypes';
                axios.get(url).then((response) => {
                    this.types.im = response.data;
                }, (error) => {
                    console.log(error);
                });
            },
            getIps() {
                const url = 'api/v2/iptypes';
                axios.get(url).then((response) => {
                    this.types.ip = response.data;
                }, (error) => {
                    console.log(error);
                });
            },
            getIcs() {
                const url = 'api/v2/ictypes';
                axios.get(url).then((response) => {
                    this.types.ic = response.data;
                }, (error) => {
                    console.log(error);
                });
            },
            getIes() {
                const url = 'api/v2/ietypes';
                axios.get(url).then((response) => {
                    this.types.ie = response.data;
                }, (error) => {
                    console.log(error);
                });
            },
            getTypes: function () {
                this.getIms();
                this.getIps();
                this.getIcs();
                this.getIes();
            },
            getMotorCodes() {
                const url = 'api/v2/motorCodes';
                axios.get(url).then(
                    (response) => {
                        console.log(response);
                        this.fetchedCodes = response.data;
                    },
                    (error) => {
                        console.log(error);
                    }
                )
            },
            findMatchedCodes() {
                //todo: get motorCodes and store in an array.
                this.motorList = [];
                console.log('inside getCodes');
                console.log(this.specData);
                this.fetchedCodes.forEach((e) => {
                    if (this.specData.kw == e.kw) {
                        this.motorList.push(e);
                    }
                })
            },
            selectFromCode(index) {
                this.specData = {
                    ...this.motorList[index]
                };
            }
        },
        components: {
            reqSpecRow: reqSpecRow,
        },
        computed: {},
        created() {
            this.specData = {
                ...this.template,
            };
            this.getTypes();
            this.getMotorCodes();
            this.debounceGetCodes = _.debounce(this.findMatchedCodes, 700);
        },
        watch: {
            'specData.kw': function () {
                this.debounceGetCodes();
            },
        }
    }
</script>