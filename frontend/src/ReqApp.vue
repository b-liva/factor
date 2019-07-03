<template>
  <v-req-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Vuetify</span>
        <span class="font-weight-light">MATERIAL DESIGN</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
        <span class="mr-2">{{testvalue}}</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <HelloWorld/>
    </v-content>
  </v-req-app>
</template>

<script>
import HelloWorld from './components/HelloWorld'

export default {
  name: 'ReqApp',
  components: {
    HelloWorld
  },
  data () {
    return {
        testvalue: 'Some Text from this component',
      //
    }
  }
}
</script>
