import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import router from './router'
import './assets/css/style.css'

Vue.config.productionTip = false;
new Vue({
    router,
    render: h => h(App)
}).$mount('#app');

