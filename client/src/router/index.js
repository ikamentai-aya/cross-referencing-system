import Vue from 'vue';
import Router from 'vue-router';
import StartComponent from '../components/Start.vue';
import ReportComponent from '../components/Report.vue';
// import WordCloudComponent from '../components/WordCloud.vue';
import ClusterHeatmap from '../components/ClusterHeatmap.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'StartComponent',
      component: StartComponent,
    },
    {
      path: '/report',
      name: 'ReportComponent',
      component: ReportComponent,
    },
    {
      path: '/zoom',
      name: 'Clustercomponent',
      component: ClusterHeatmap,
    },
  ],
});
