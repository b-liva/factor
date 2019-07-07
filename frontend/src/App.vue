<template>
    <v-app class="grey lighten-4">
        <Navbar/>
        <v-content>
            <router-link to="/home"><btn class="indigo">Go to home</btn></router-link>
            <router-link to="/about">Go to about</router-link>
            <router-link to="/sales">Go to Sales</router-link>
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
