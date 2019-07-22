<template>
    <div>
        <h1>this is rows...</h1>
        <div v-for="(r, index) in specs.specs">{{r}}<v-icon @click="removeSpec(r.id, index)">close</v-icon></div>

    </div>
</template>

<script>
    import axios from 'axios';
    import _ from 'underscore';

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
        created() {},
        props: {
            row: {
                type: Object,
            }
        },
        methods: {
            removeSpec(id, index){
                console.log(index, id);
                this.$emit('specRemoved', this.specs.specs[index].id);
                this.specs.specs.splice(index, 1);
            },
        },
        components: {},
        watch: {},
    }
</script>