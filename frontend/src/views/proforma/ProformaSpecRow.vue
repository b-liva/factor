<template>
    <div>
        <template md4 v-for="(spec, index) in specs.specs">
            <v-layout row>
                <v-flex md1>
                    <v-text-field
                            label="تعداد"
                            v-model="spec.qty"
                            @change="spec.modified = true"
                    >

                    </v-text-field>
                </v-flex>
                <v-flex md4 align-middle>
                    <v-subheader>دستگاه {{spec.kw}} کیلووات {{spec.rpm}} دور {{spec.voltage}} ولت {{spec.modified}}</v-subheader>
                </v-flex>

                <v-flex md2>
                    <v-text-field
                            label="قیمت"
                            v-model="spec.price"
                            @change="spec.modified = true"
                    ></v-text-field>
                </v-flex>
                <v-flex md1>
                    <!--todo: can't be greater than qty-->
                    <v-text-field
                            label="ارسال شده"
                            v-model="spec.sentQty"
                            @change="spec.modified = true"
                    ></v-text-field>
                </v-flex>
                <v-flex md1>
                    <v-subheader><v-icon @click="removeSpec(spec.id, index)">close</v-icon></v-subheader>
                </v-flex>
            </v-layout>
        </template>


        <div>
            <h1>this is rows...!</h1>
            <div v-for="(r, index) in specs.specs">{{r}}
                <v-icon @click="removeSpec(r.id, index)">close</v-icon>
            </div>
        </div>
    </div>


</template>

<script>

    export default {
        data() {
            return {
                msg: '',
                popUPNow: '',
                specs: this.row,
                titleRules: [
                    v => v.length >= 3 || 'حداقل 5 حرف لازم است.'
                ],
            }
        },
        created() {
        },
        props: {
            row: {
                type: Object,
            }
        },
        methods: {
            removeSpec(id, index) {
                console.log(index, id);
                this.$emit('specRemoved', this.specs.specs[index].id);
                this.specs.specs.splice(index, 1);
            },
        },
        components: {},
        watch: {},
    }
</script>