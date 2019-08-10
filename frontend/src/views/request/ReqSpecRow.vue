<template>
    <div>
        <v-layout row>
            <v-flex md11 v-if="!row.editable">
                <div>
                    <v-layout row wrap>
                        <v-flex md10>
                            {{specs.qty}} - {{specs.kw}} - {{specs.speed}} - {{specs.voltage}} - {{specs.details}}
                        </v-flex>
                        <v-flex md2>
                            <v-layout row wrap>
                                <v-flex md3 v-if="row.editable">
                                    <v-icon v-on:click="save">save</v-icon>
                                </v-flex>
                                <v-flex md3>
                                    <v-icon v-on:click="edit">edit</v-icon>
                                </v-flex>
                                <v-flex md3 v-if="row.editable">
                                    <v-icon v-on:click="remove">close</v-icon>
                                </v-flex>
                            </v-layout>
                        </v-flex>
                    </v-layout>

                </div>
            </v-flex>
            <v-flex md11 v-if="row.editable">
                <v-form ref="form">
                    <v-layout row wrap fluid>
                        <v-flex md6>
                            <v-layout row>
                                <v-flex md2>

                                    <v-text-field :disabled="!row.editable" label="کد" type="number"
                                                  v-model="specs.code"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field :disabled="!row.editable" label="تعداد" type="number"
                                                  v-model="specs.qty"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field :disabled="!row.editable" label="کیلووات" type="number"
                                                  v-model="row.kw"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field :disabled="!row.editable" label="سرعت" type="number"
                                                  v-model="row.speed"></v-text-field>
                                </v-flex>
                                <v-flex md2>
                                    <v-text-field :disabled="!row.editable" label="ولتاژ" type="number"
                                                  v-model="row.voltage"></v-text-field>
                                </v-flex>
                                <!--<v-flex md6>-->
                                <!--<v-textarea :disabled="!row.editable" label="جزئیات" prepend-icon="edit"-->
                                <!--v-model="row.details"></v-textarea>-->
                                <!--</v-flex>-->
                            </v-layout>

                        </v-flex>
                        <v-flex md4>
                            <v-layout row>
                                <v-flex md3>
                                    <v-select
                                            v-model="specs.im"
                                            :items="types.im_types"
                                            item-value="id"
                                            item-text="title"
                                            label="IM"
                                    ></v-select>
                                </v-flex>
                                <v-flex md3>
                                    <v-select
                                            v-model="row.ic"
                                            :items="types.ic_types"
                                            item-value="id"
                                            item-text="title"
                                            label="IC"
                                    ></v-select>
                                </v-flex>
                                <v-flex md3>
                                    <v-select
                                            v-model="row.ip"
                                            :items="types.ip_types"
                                            item-value="id"
                                            item-text="title"
                                            label="IP"
                                    ></v-select>
                                </v-flex>
                                <v-flex md3>
                                    <v-select
                                            v-model="row.ie"
                                            :items="types.ie_types"
                                            item-value="id"
                                            item-text="title"
                                            label="IE"
                                    ></v-select>
                                </v-flex>
                            </v-layout>

                        </v-flex>
                        <v-flex md2>
                            <v-layout row align-center>
                                <v-flex md3>
                                    <v-icon v-on:click="save">save</v-icon>
                                </v-flex>
                                <v-flex md3 v-if="!row.editable">
                                    <v-icon v-on:click="edit">edit</v-icon>
                                </v-flex>

                                <v-flex md3 v-if="row.editable">
                                    <v-layout row justify-center>
                                        <v-dialog v-model="dialog" max-width="600px">
                                            <v-icon flat slot="activator">add</v-icon>
                                            <v-card>
                                                <v-card-title>
                        <span class="headline">
                            {{row.qty}} دستگاه الکتروموتور {{row.kw}} کیلووات {{row.rpm}} دور
                        </span>
                                                </v-card-title>
                                                <v-card-text>
                                                    <v-container grid-list-md>
                                                        <v-textarea
                                                                :disabled="!row.editable"
                                                                label="جزئیات"
                                                                prepend-icon="edit"
                                                                v-model="row.details">
                                                        </v-textarea>
                                                    </v-container>
                                                </v-card-text>
                                            </v-card>
                                        </v-dialog>

                                    </v-layout>
                                </v-flex>
                                <v-flex md3>
                                    <v-icon v-on:click="copy">file_copy</v-icon>
                                </v-flex>
                                <v-flex md3>
                                    <v-icon v-on:click="remove">close</v-icon>
                                </v-flex>
                            </v-layout>

                        </v-flex>
                    </v-layout>
                    <!--<v-layout row>-->
                    <!--<v-btn class="success mx-0 mt-3" @click="submit" :loading="row.submitting">ذخیره</v-btn>-->
                    <!--<v-btn class="success mx-0 mt-3" @click="row.editable = !row.editable"-->
                    <!--:loading="row.submitting">toggle-->
                    <!--</v-btn>-->
                    <!--</v-layout>-->
                </v-form>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
    import axios from 'axios';
    import _ from 'underscore';

    export default {
        data() {

            return {
                msg: '',
                dialog: '',
                popUPNow: '',
                types: [],
                specs: this.row,
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
            }
        },
        created() {
            this.debouncedSpecByCode = _.debounce(this.clearMsg, 700);
            this.getTypes();
        },
        props: {
            row: {
                type: Object,
            }
        },
        methods: {
            submit: function () {
                this.specs.push(this.row);
            },
            copy: function () {
                this.$emit('copy')
            },
            remove: function () {
                this.$emit('remove')
            },
            edit: function () {
                console.log('item opened saved.');
                this.specs.editable = true;
                this.getTypes();
            },
            save: function () {
                console.log('item saved.');
                this.specs.editable = false;
            },
            clearMsg: function () {
                this.msg = '';
            },
            getTypes: function () {
                const url = 'api/request/spec-item-types';
                axios.get(url).then((response) => {
                    this.types = response.data;
                    console.log(this.types);
                }, (error) => {
                    console.log(error);
                });
            },
            addDetails: function () {
                this.popUPNow = true;
            },
        },
        components: {},
        watch: {
            // row: {
            //     immediate: true,
            //     deep: true,
            //     handler(newValue, oldValue) {
            //         console.log('watched is changing');
            //         console.log(oldValue);
            //         console.log(newValue);
            //         this.msg = 'code is being typed..';
            //         this.debouncedSpecByCode();
            //     }
            // },
            'row.code': function (newVal) {
                this.msg = 'typing';
                this.$set(this.specs, 'code', newVal);
                this.debouncedSpecByCode();
            },
            'row.kw': function (newVal) {
                this.msg = 'typing';
                this.$set(this.specs, 'kw', newVal);
                this.debouncedSpecByCode();
            },
        },
    }
</script>