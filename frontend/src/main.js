import Vue from 'vue'
import App from './App.vue'
import router from './router';
import NavBar from '@/components/NavBar.vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import { Steps, Step } from 'element-ui';
import moment from "moment"

Vue.use(BootstrapVue);
Vue.use(Steps);
Vue.use(Step);
Vue.use(moment)

Vue.config.productionTip = false

const DEFAULT_TITLE = 'Gapsule';
// eslint-disable-next-line
router.afterEach((to, from) => {
  if (typeof to.meta == 'function') {
    document.title = to.meta.call(to) || DEFAULT_TITLE;
  } else {
    document.title = to.meta.title || DEFAULT_TITLE;
  }
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

new Vue({
  router,
  render: h => h(NavBar),
}).$mount('#navbar')

