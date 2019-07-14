<template>
    <v-app class="grey lighten-4">
        <Navbar/>
        <v-content>
            <router-link to="/home"><btn class="indigo">Dashboard</btn></router-link>
            <router-link to="/sales">sales page</router-link>
            <router-link to="/about">about</router-link>
            <router-link to="/requests">requests</router-link>
            <router-link to="/proformas">proformas</router-link>
            <router-link to="/payments">payments</router-link>
            <router-view></router-view>
            <!--<SalesDash/>-->
        </v-content>
    </v-app>
</template>

<script>
    import Navbar from './components/Navbar'
    import HelloWorld from './components/HelloWorld'
    import SalesDash from './components/SalesDash'

    export default {
        name: 'App',
        components: {
            Navbar,
            SalesDash,
            HelloWorld,
        },
        data() {
            return {
                //
            }
        },
        mounted() {
            this.$vuetify.rtl = true;
        },
    }
</script>
