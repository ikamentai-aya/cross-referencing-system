<template>
  <div>
    <!-- <h1>Zoomの埋め込みのお試し</h1>
    <iframe src="https://us04web.zoom.us/j/72250476249?pwd=mrPEIaUvTVWUN2rwMLFbw5cidlkWtm.1" sandbox="allow-forms allow-scripts" title="zoom"></iframe> -->
    <div id="d3view"></div>
    <p>{{selectWord}}</p>
    <!-- <a href='#' class="btn" @click="wideDisplay">{{btn_icon}}</a> -->
  </div>
</template>

<script>
import axios from 'axios';
import * as d3 from 'd3';

export default {
  name: 'WordCloudComponent',
  props: ['selectCluster'],
  data() {
    return {
      selectWord: 'Click on a word to select it',
      btn_icon: '↗️',
      isWideDisplay: false,
    };
  },
  methods: {
    createD3() {
      console.log('D3の練習');
      const path = '/wordcloud';
      const payload = {
        select_cluster: this.selectCluster,
      };
      axios.post(path, payload)
        .then((res) => {
          this.wordcloud_item = res.data.item;
          console.log(this.wordcloud_item);
          this.layout();
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    layout() {
      console.log('ok');
      this.cluster_svg = d3.select('#d3view').append('svg')
        .attr('class', 'wordcloud')
        .attr('width', 600)
        .attr('height', 400)
        .attr('viewBox', '0 0 600 400')
        .attr('preserveAspectRatio', 'xMidYMid');
      this.cluster_svg.selectAll('text')
        .data(this.wordcloud_item)
        .enter()
        .append('text')
        .text((d) => d.title)
        .attr('x', (d) => d.x)
        .attr('y', (d) => d.y)
        .attr('font-size', (d) => d.size)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'central');
      // 単語をクリックしたらその単語を表示する
      this.cluster_svg.selectAll('text').on('click', (data, i) => {
        this.selectWord = `select word is: ${i.title}`;
      });
      // ビューの大きさに合わせてサイズの変更を行う
      this.cluster_svg.attr('width', window.innerWidth * 0.2)
        .attr('height', window.innerWidth * 0.13);
    },
    wideDisplay() {
      if (this.isWideDisplay) {
        this.isWideDisplay = false;
        this.btn_icon = '↗️';
      } else {
        this.isWideDisplay = true;
        this.btn_icon = '↙️';
      }
    },
  },
  created() {
    this.createD3();
  },
  watch: {
    selectCluster() {
      d3.selectAll('svg.wordcloud').remove();
      this.createD3();
    },
  },
};
</script>

<style>
.d3view {
  border: solid 1px #A1A3A6;
}
a.btn {
  border: 2px solid #696969;
  color: #696969;
}
</style>
