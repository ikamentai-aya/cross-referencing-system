import Vue from 'vue';
import vGallery from 'v-gallery';
import 'bootstrap/dist/css/bootstrap.css';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';

Vue.use(vGallery);
Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
