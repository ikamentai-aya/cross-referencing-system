<template>
  <div id="my_viz2"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'ClusterHeatmap',
  props: [
    'cluster_width', 'height', 'cluster_group', 'y_label',
  ],
  data() {
    return {
      select_cluster: '',
    };
  },
  methods: {
    // クラスターのヒートマップを描画する
    newD3Cluster() {
      const margin = {
        top: 10, right: 10, bottom: 30, left: 10,
      };
      const width = this.cluster_width - margin.right - margin.left;
      const height = this.height - margin.top - margin.bottom - 50;
      this.cluster_svg = d3.select('#my_viz2').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      const myGroupes = this.cluster_group;
      const myVars = this.y_label;

      const x = d3.scaleBand().range([0, width]).domain(myGroupes).padding(0.1);
      this.cluster_svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x).tickSize(0));
      const y = d3.scaleBand().range([30, height]).domain(myVars).padding(0.01);

      // インフォメーション関連
      this.cluster_svg.append('text').attr('class', 'info').attr('x', width - 14).attr('y', 15)
        .text('?')
        .attr('fill', 'royalblue');

      this.cluster_svg.append('circle').attr('cx', width - 10).attr('cy', 10).attr('r', 10)
        .attr('fill', 'rgb(0,0,0,0)')
        .attr('stroke', 'royalblue');

      this.cluster_svg.select('circle').on('click', () => {
        if (this.is_cluster_imfo) {
          this.cluster_svg.select('text.info').text('?');
          this.is_cluster_imfo = false;
        } else {
          this.cluster_svg.select('text.info').text('×');
          this.is_cluster_imfo = true;
        }
      });

      // タイトルを入れる
      this.cluster_svg.append('text').attr('x', 0).attr('y', 10).style('font-size', `${width / 20}px`)
        .text('similar paragraph group');

      this.cluster_svg.selectAll('rect.heatmap')
        .data(this.cluster_data)
        .enter()
        .append('rect')
        .attr('class', 'heatmap')
        .attr('x', (d) => x(d.x))
        .attr('y', (d) => y(d.y))
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .style('fill', (d) => {
          let color = 'whitesmoke';
          if (d.isin > -1) {
            color = d3.schemePaired[d.isin];
          }
          return color;
        })
        .on('click', (data, i) => {
          console.log(data);
          this.select_cluster = i.x;
          console.log(i.x);
          this.selectCluster();
        });
    },
  },
};
</script>
