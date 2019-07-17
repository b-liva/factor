<template>
    <nav>
        <v-toolbar flat app>
            <v-toolbar-side-icon class="grey--text" @click="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-title>
                <span class="font-weight-lighten">معاونت بازرگانی <span class="text-uppercase green--text">جمکو</span></span>
            </v-toolbar-title>
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/home">داشبورد</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/sales" tag="li" active-class="active">کارشناسان</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/about" tag="li" active-class="active">درباره</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/requests" tag="li" active-class="active">سفارشات خرید</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/proformas" tag="li" active-class="active">پیش فاکتور</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/received" tag="li" active-class="active">دریافت</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<router-link to="/sandbox" tag="li" active-class="active">sandbox</router-link>-->
            <!--</v-btn>-->
            <!--<v-btn flat color="grey">-->
                <!--<v-icon>exit_to_app</v-icon>-->
                <!--<span>خروج</span>-->
            <!--</v-btn>-->
        </v-toolbar>
        <v-btn flat color="">sign out</v-btn>
        <v-navigation-drawer app v-model="drawer" class="indigo" right>
            <v-list>
                <v-list-tile v-for="link in links" route :to="link.route">
                    <v-list-tile-action>
                        <v-icon class="white--text">{{ link.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title class="white--text">{{ link.text }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>

            </v-list>
        </v-navigation-drawer>

    </nav>

</template>

<script>
    export default {
        data() {
            return {
                drawer: true,
                links: [
                    {icon: 'dashboard', text: 'داشبورد', route: '/'},
                    {icon: 'supervisor_account', text: 'کارشناسان', route: '/sales'},
                    {icon: 'perm_contact_calendar', text: 'مشتریان', route: '/customers'},
                    {icon: 'phone_callback', text: 'سفارشات فروش', route: '/requests'},
                    {icon: 'more', text: 'پیش فاکتور', route: '/proformas'},
                    {icon: 'money', text: 'دریافتی', route: '/received'},
                    {icon: 'code', text: 'sandbox', route: '/sandbox'},
                    {icon: 'exit_to_app', text: 'خروج', route: '/exit'},
                ]
            }
        }
    }
</script>
