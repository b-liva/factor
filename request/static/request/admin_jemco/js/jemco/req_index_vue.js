Vue.component('cmform', {
    template: "<div>" +
        "<div class='row'><div class='col-md-12'><div :class='toggleBtnClass' v-html='' @click='toggleVisible' class=' pull-left'>" +
        "<i :class='arrowClass' aria-hidden='true'></i></div></div>" +
        "" +
        "<div class='col-md-11'  v-show='is_visible'>" +
        "<div v-for='c in chats' class='row'>" +
        "<div :class='direction(c.dir)'>" +
        "<div  v-if='ltrdir'><div class='pull-right  salesPerson'>{{c.chat_owner}}</div><br><div class='text-right'>{{c.chat_txt}}</div></div>" +
        "<div v-else ><div class='pull-left customerPerson'>{{c.chat_owner}}</div> <br><div class='text-right'>{{c.chat_txt}}</div></div>" +
        "</div>" +
        "</div>" +
        "<form  @submit.prevent='submitChat'>" +
        "<textarea class='col-md-10' v-model='chat' style='height: 60px;'>" +
        "</textarea>" +
        "<div class='col-md-2' ><button class='btn btn-success col-md-12' style='height: 60px;'>ثبت</button></div>" +
        "</form></div></div>" +
        "</div>",
    data() {
        return {
            is_visible: false,
            is_visible_text: "<i class='fa fa-arrow-down' aria-hidden='true'></i> جزئیات",
            loaded: false,
            chat: '',
            chats: [],
            toggleBtnClass: 'btn btn-success btn-xs',
            arrowClass: 'fa fa-arrow-down pull-left',
            dir: '',
            ltrdir: '',
        }
    },
    props: {
        spec_id: '',
    },
    computed:{

    },
    methods: {
        submitChat: function () {
            // alert('data submitted.' + this.chat + " - specId: " + this.spec_id);
            axios.post('/speccm/add-vue', params = {
                'spec': this.spec_id,
                'text': this.chat,
            })
                .then(res => {
                    this.chats = res.data.chats;
                });
        },
        toggleVisible: function () {
            this.is_visible = !this.is_visible;
            if (!this.loaded) {

                axios.post('/speccm/get_chat', params = {
                    'spec': this.spec_id
                })
                    .then(res => {
                        this.chats = res.data.chats;
                        this.loaded = true
                    })
            }
            if (this.is_visible) {
                this.is_visible_text = "<i class='fa fa-arrow-up' aria-hidden='true'></i>";
                this.toggleBtnClass = 'btn btn-danger btn-xs';
                this.arrowClass = 'fa fa-arrow-up pull-left';
            }
            else {
                this.is_visible_text = "جزئیات <i class='fa fa-arrow-down' aria-hidden='true'></i>";
                this.toggleBtnClass = 'btn btn-success btn-xs';
                this.arrowClass = 'fa fa-arrow-down pull-left';
            }
        },
        direction: function (value) {
            if (value === 'right'){
                this.ltrdir = true;
                return 'col-md-6 pull-right rtlClass';
            }
            else {
                this.ltrdir = false;
                return 'col-md-6 pull-left ltrClass';
            }
        },
    }
});
const vueapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#request_index_app',
    data: {},
    watch: {},
    created: function () {
    },
    methods: {},
    computed: {}
});