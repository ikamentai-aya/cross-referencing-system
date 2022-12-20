<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-7">
          <h3 class="mx-auto"  style="margin : 5px 5px 5px 5px" >{{reportTitle}}</h3>
        </div>
        <div class="col-3">
          <br>
          <v-sheet>
            <v-row align="center" justify="space-around">
              <a href="#" class="btn" @click="backHome" width="50" >
                <v-icon color=#696969>mdi-home</v-icon>
              </a>
              <a href="#" class="btn" @click="changeReport">
                <v-icon color=#d6d6d6 v-if="doDisplayNote">mdi-swap-horizontal</v-icon>
                <v-icon color=#696969 v-if="!doDisplayNote">mdi-swap-horizontal</v-icon>
              </a>
              <note-taking
                v-bind:videoLink="this.video_link"
                v-bind:slide_page_num = "this.slide_page_num"
                v-bind:selectSlide = "this.selectSlide"
                v-bind:slideItems = "this.items"
                v-bind:select_report_path = "select_report_path"
                v-bind:report_max_page="this.report_max_page"
                v-bind:report_page = "this.report_page"
                v-bind:report_basic_path = "this.report_basic_path"
                v-bind:login_name = "this.loginName"
                v-bind:is_login = "this.isLogin"
                @save = "reloadNote"
              ></note-taking>
              <a href="#" class="btn" @click="changeDisplayNote" width="50" >
                <v-icon color=#696969 v-if="!doDisplayNote">mdi-book-open</v-icon>
                <v-icon color=#26d9d9 v-else>mdi-book-open</v-icon>
              </a>
              <a href="#" class="btn" @click="isWord = !isWord" width="50" >
                <v-icon color=#696969 v-if="!isWord&!doDisplayNote&!isRefer&!isParagraph"
                >mdi-cards-outline</v-icon>
                <v-icon color=#d6d6d6 v-if="doDisplayNote|isRefer|isParagraph">
                mdi-cards-outline</v-icon>
                <v-icon color=#26d9d9 v-if="isWord&!doDisplayNote&!isRefer&!isParagraph">
                mdi-cards-outline</v-icon>
              </a>
            </v-row>
          </v-sheet>
        </div>
        <div class="col-1">
          <br>
          <p v-if="isLogin">login Name: {{loginName}}</p>
          <p v-else>Please Login</p>
        </div>
        <div class="col-1">
          <v-text-field
            v-model="loginName"
            label="login name"
            @change="reloadNote"
            clearable
          ></v-text-field>
        </div>
      </div>
      <hr>
      <note-display v-if="doDisplayNote" ref="noteDisplay"
        :fileName="this.fileName"
        :login_name="this.loginName"></note-display>
      <div class="row"  style="margin : 2px 2px 2px 2px"  id="row" v-show = "!doDisplayNote">
        <!-- 右クリックのメニュー -->
        <v-menu
          v-model="showTool"
          :position-x="tool_x"
          :position-y="tool_y"
          absolute
          offset-y
          v-if = "showTool"
        >
        <v-list>
          <v-list-item v-for="item in menu_list" :key="item"
          @click="selectTool(item)" :color="item.color" dense>
            <v-list-item-icon><small><v-icon :color="item.color">{{item.icon}}
              </v-icon></small>
            </v-list-item-icon>
            <v-list-item-title><small>{{item.title}}</small></v-list-item-title>
          </v-list-item>
        </v-list>
        </v-menu>
        <!-- ビデオやスライドに関するビュー -->
        <div class="col-4" v-if="isReport">
          <div id='slide'>
            <div ref='select_slide' style="border-style: ridge; position: relative;"
            v-if="this.select">
              <v-img fluid :src="selectSlide" id="select_slide"
              @click.left = "this.showTool = false"
              @click.right.prevent = "onrightclick"></v-img>
            </div>
            <iframe id="presen_video" :src="video_link" :width="video_width" :height="video_height"
              title="movie" frameborder="0" allow="autoplay; fullscreen"
              style="border-style: ridge" allowfullscreen v-else>
            </iframe>
          </div>
          <br>
          <div class="row">
            <div class="col-10">
              <a href="#" class="btn" @click="changeVideo">
                <v-icon>mdi-swap-horizontal</v-icon>
              </a>
            </div>
            <div class="col-2">
              <p><small>
                {{slide_page_num}}/{{slide_length}}
              </small></p>
            </div>
          </div>
          <br>
          <v-sheet>
            <v-slide-group v-model="model" mandatory show-arrows>
              <v-slide-item
                v-for="(item,i) in items"
                :key="i"
                v-slot="{ active, toggle }"
              >
                <v-card
                  :color="active ? 'primary' : 'grey lighten-1'"
                  class="ma-4"
                  width="180"
                  height="100"
                  @click = "toggle"
                >
                  <v-img fluid :src="item" @click="toggleMethod(item, i, true)"></v-img>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </v-sheet>
          <div class="audioTranscript">
            <p>Speech transcript:</p>
            <p v-for="(item, i) in selectAudio" :key="i"><small>{{item}}</small></p>
          </div>
        </div>
        <div class="col-1" style="position: relative;" v-show="isReport">
          <div id="my_viz1"> </div>
          <div class="col-1">
            <v-alert
              style="position: absolute; top:50px; left:0px;"
              border="top"
              shaped
              color="red lighten-2"
              dark
              :value="is_sim_imfo"
            >
              You may review the paragraphs of the paper similar to the slide you selected.
            </v-alert>
          </div>
        </div>
        <div class="col-5" style="position: relative;" id="col5" v-if="isReport">
          <div style="border-style: ridge">
            <v-img fluid :src="select_report_path"  id="report"
            @click.left = "onleftclick"
            @click.right.prevent = "onrightclick"></v-img>
            <p style="position: absolute; top: 10px; left: 20px"><small>
              {{report_page}}/{{report_max_page}}
            </small></p>
            <div class="col-5">
              <v-alert
                dense
                prominent
                type="error"
                :value="not_paragraph"
                style="position: absolute; top: 10px; left: 10px;"
              >
                Sorry. I can't find the paragraph you chosed.
              </v-alert>
            </div>
          </div>
        </div>
        <div class="col-10" v-else>
          <cluster-component
            v-bind:selectCluster="this.select_cluster"
            v-bind:clusterColor="this.cluster_color"
            v-bind:clusterGroup="this.cluster_group"
            v-bind:clusterWordcloudPath="this.cluster_wordcloud_path"
            v-bind:clusterImgList="this.cluster_img_list"
            v-bind:selectClusterSlide="this.select_cluster_slide"
            v-bind:tableData="this.table_data"
            v-on:change="changeClusterName($event)"
          />
        </div>
        <div class="col-1" v-show="!isParagraph && !isRefer && !isWord" style="position: relative;">
          <div id="my_viz2"></div>
          <v-alert
            style="position: absolute; top:50px; left:0px;"
            border="top"
            shaped
            color="blue lighten-2"
            dark
            :value="is_cluster_imfo"
          >
            Paragraphs with similar content are classified here as a group.
            Click on the group you are interested in to see the details.
          </v-alert>
        </div>
        <div class="col-1" v-show="!isParagraph && !isRefer && !isWord" id="cluster_btn">
          <p><small>Group</small></p>
          <div v-for="g in cluster_group" :key="g">
            <a href="#" class="btn"
              @click="selectCluster(g.index, g.color)" :style="g.color">
            {{g.name}}</a>
          </div>
        </div>
        <div class="col-2" style="position: relative;">
          <!-- 段落を選択したときに段落関連の情報を提示する -->
          <!-- <a href="#" class="btn" @click="hideRefer">
            <v-icon>mdi-close</v-icon>
          </a> -->
          <div v-show="isParagraph">
            <v-row class="justify-end">
              <v-btn
                icon
                color="red"
                @click="hideRefer"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-row>
            <paragraph-component
              v-bind:paragraphIndex="this.paragraphIndex"
              v-bind:paragraphRefs="this.paragraphRefs"
              v-bind:haveReffer="this.haveReffer"
              v-bind:paragraphAdd ="this.paragraphAdd"
              v-bind:isParagraph = "this.isParagraph"
              v-on:toggleMethod="toggleMethod"
              @hilightParagraph="hilightParagraph"
              @jumpToFigure="jumpToFigure"
            />
            <br>
          </div>
          <div v-show="isWord&!isRefer&!isParagraph">
            <word-content
            :isWord = "this.isWord"
            :login_name = "this.loginName"
            ref="wordContent"
          ></word-content>
          </div>
          <!-- 画像を選択したときに参照している段落の一覧を見せる -->
          <div v-show="isRefer">
            <v-row class="justify-end">
              <v-btn
                icon
                color="red"
                @click="hideRefer"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-row>
            <h5>
              paragraphs referring:
              <a href='#' @click="jumpToFigure">{{figureName}}</a>
            </h5>
            <table border="1">
              <tr>
                <th>index</th>
                <th>section</th>
                <th>start of paragraph</th>
              </tr>
              <tr  v-for="item in refer_table_data" :key="item" @click="clickRow(item)">
                <td><small>{{item.index}}</small></td>
                <td><small>{{item.section}}</small></td>
                <td><small>{{item.start}}</small></td>
              </tr>
            </table>
            <br>
            <v-chip-group column v-model="chip_refer">
              <v-chip v-for="tip in chip_item" :key="tip" filter outlined :color="tip.color">
                {{tip.title}}
              </v-chip>
            </v-chip-group>
            <!-- <a href="#" class="btn" @click="hideRefer">
              <v-icon>mdi-close</v-icon>
            </a> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  a:hover {
    text-decoration-line: underline;
    text-decoration-color: cyan;
  }
</style>

<script>
import axios from 'axios';
import * as d3 from 'd3';
import ParagraphComponent from './Paragraph.vue';
import ClusterComponent from './Cluster.vue';
import NoteTaking from './NoteTaking.vue';
import NoteDisplay from './NoteDisplay.vue';
import WordContent from './noteComponents/word.vue';

export default {
  name: 'ReportComponent',
  components: {
    'paragraph-component': ParagraphComponent,
    'cluster-component': ClusterComponent,
    NoteTaking,
    NoteDisplay,
    WordContent,
  },
  data() {
    return {
      fileName: 'note-1020',
      id: 0,
      reportTitle: '',
      items: [],
      model: null,
      selectSlide: '',
      slide_page_num: 0,
      audioContent: '',
      selectAudio: [],
      select: true,
      report_page: 0,
      select_report_path: '',
      report_basic_path: '',
      video_link: '',
      video_link_base: '',
      heatmap_data: {},
      heatmap: {},
      cluster_heatmap: {},
      cluster_data: {},
      cluster_group: {},
      y_label: {},
      svg: {},
      cluster_svg: {},
      select_cluster: '',
      cluster_wordcloud_path: '',
      cluster_img_list: [],
      cluster_rect: {},
      cluster_color: '',
      isReport: true,
      section_title: [],
      video_width: 600,
      video_height: 600,
      table_data: [],
      is_sim_imfo: false,
      is_cluster_imfo: false,
      not_paragraph: false,
      isRefer: false,
      isParagraph: false,
      paragraphRefs: [],
      showTool: false,
      menu_position: {
        left: 0,
        top: 0,
      },
      menu_list: [
        { title: '何となく大事', icon: 'mdi-check', color: '#FFB55B' },
        { title: '研究の要', icon: 'mdi-check-decagram', color: '#d92626' },
        { title: '後で読む', icon: 'mdi-repeat-variant', color: '#26d98e' },
        { title: '分からない', icon: 'mdi-help', color: '#7f26d9' }],
      tag: '',
      chip_item: [
        { color: '#FFB55B', title: '何となく大事' },
        { color: '#d92626', title: '研究の要' },
        { color: '#26d98e', title: '後で読む' },
        { color: '#7f26d9', title: '分からない' },
        { color: '#268ed9', title: '英語の勉強' },
      ],
      doDisplayNote: false,
      isWord: false,
      // loginに関すること
      isLogin: false,
      loginName: '',
    };
  },
  methods: {
    getData() {
      const path = '/report_back';
      axios.get(path)
        .then((res) => {
          // eslint-disable-next-line prefer-destructuring
          this.reportTitle = res.data.report_title;
          this.fileName = res.data.filename;
          this.items = res.data.slide_files;
          this.report_max_page = res.data.report_page - 1;
          const [first1] = this.items;
          this.selectSlide = first1;
          this.slide_length = res.data.audio_content.length;
          this.audioContent = res.data.audio_content;
          const [first2] = this.audioContent;
          this.selectAudio = first2;
          this.report_basic_path = res.data.select_report;
          this.video_link = res.data.video_link;
          this.video_link_base = this.video_link;
          this.select_report_path = `${this.report_basic_path}/0.jpg`;
          this.heatmap_data = res.data.heatmap_data;
          this.cluster_data = res.data.cluster_data;
          this.cluster_group = res.data.cluster_group;
          this.cluster_slide = res.data.cluster_slide_path;
          this.y_label = res.data.heat_map_label;
          this.section_title = res.data.section_title;
          this.cluster_width = document.getElementById('my_viz2').clientWidth;
          this.height = document.getElementById('col5').clientWidth * 1.41;
          this.newD3Method(true);
          this.newD3Cluster();
          // 動画のサイズを調整
          // const e = document.getElementById('left');
          // const video = document.getElementById('slide');
          const dom = this.$refs.select_slide;
          const rect = dom.getBoundingClientRect();
          this.video_width = rect.width;
          this.video_height = rect.width * 0.64;
          this.cluster_wordcloud_path = `/static/static/${this.fileName}/wordcloud/0.png`;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    newD3Method() {
      // グラフのサイズ
      const margin = {
        top: 10, right: 10, bottom: 30, left: 10,
      };
      const width = document.getElementById('my_viz1').clientWidth * 0.9;
      const height = this.height - margin.top - margin.bottom - 50;

      this.svg = d3.select('#my_viz1').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      const myGroupes = [0, 1];
      const myVars = this.y_label;

      this.svg_x = d3.scaleBand().range([0, width]).domain(myGroupes);
      this.svg_y = d3.scaleBand().range([30, height]).domain(myVars).padding(0.01);

      this.svg.append('text').attr('x', 0).attr('y', 10).style('font-size', `${width / 10}px`)
        .text('similar paragraph');

      // インフォメーション
      this.svg.append('text').attr('class', 'info').attr('x', width - 14).attr('y', 15)
        .text('?')
        .attr('fill', 'pink');

      this.svg.append('circle').attr('cx', width - 10).attr('cy', 10).attr('r', 10)
        .attr('fill', 'rgb(0,0,0,0)')
        .attr('stroke', 'pink');

      this.svg.select('circle')
        .on('click', () => {
          if (this.is_sim_imfo) {
            this.svg.select('text.info').text('?');
            this.is_sim_imfo = false;
          } else {
            this.svg.select('text.info').text('×');
            this.is_sim_imfo = true;
          }
        });

      const myColor = d3.scaleLinear()
        .domain([0, 0.5])
        .range(['mistyrose', 'red']);

      this.svg.selectAll()
        .data(this.heatmap_data)
        .enter()
        .append('rect')
        .attr('class', 'heatmap')
        .attr('x', this.svg_x(1))
        .attr('y', (d) => this.svg_y(d.y))
        .attr('width', this.svg_x.bandwidth())
        .attr('height', this.svg_y.bandwidth())
        .style('fill', (d) => myColor(d.color));

      this.svg.selectAll('rect.title')
        .data(this.section_title)
        .enter()
        .append('rect')
        .attr('class', 'title')
        .attr('x', this.svg_x(0))
        .attr('y', (d) => this.svg_y(d.start))
        .attr('width', this.svg_x.bandwidth())
        .attr('height', (d) => this.svg_y.bandwidth() * d.height)
        .attr('fill', 'white')
        .attr('stroke', '#969696')
        .attr('stroke-width', 2);

      this.svg.selectAll('text.section')
        .data(this.section_title)
        .enter()
        .append('text')
        .attr('class', 'section')
        .attr('x', this.svg_x(0) + 3)
        .attr('y', (d) => this.svg_y(Math.floor((d.end + d.start + 1) / 2)))
        .attr('fill', '#969696')
        .attr('font-size', this.svg_y.bandwidth())
        .text((d) => d.title.slice(0, 5));

      this.svg.selectAll('rect.heatmap').on('click', (data, i) => {
        this.hilightParagraph(i.y);
      });
    },
    // 類似度の可視化を更新する
    updateD3Method() {
      const myColor = d3.scaleLinear()
        .domain([0, 0.5])
        .range(['mistyrose', 'red']);
      // const myColor = d3.scaleLinear()
      //   .domain([0, 0.5])
      //   .range(['aliceblue', 'blue');

      this.svg.selectAll('rect.heatmap')
        .data(this.heatmap_data)
        .attr('x', this.svg_x(1))
        .attr('y', (d) => this.svg_y(d.y))
        .attr('width', this.svg_x.bandwidth())
        .attr('height', this.svg_y.bandwidth())
        .style('fill', (d) => myColor(d.color));
    },
    // クラスターのヒートマップを描画する
    newD3Cluster() {
      const margin = {
        top: 10, right: 10, bottom: 30, left: 10,
      };
      const width = this.cluster_width * 0.9;
      // const height = document.documentElement.clientHeight - margin.top - margin.bottom - 50;
      const height = this.height - margin.top - margin.bottom - 50;

      this.cluster_svg = d3.select('#my_viz2').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      // const myGroupes = this.cluster_group;
      const myGroupes = [0, 1];
      const myVars = this.y_label;

      const x = d3.scaleBand().range([0, width]).domain(myGroupes).padding(0.01);
      // this.cluster_svg.append('g')
      //   .attr('transform', `translate(0,${height})`)
      //   .call(d3.axisBottom(x).tickSize(0));
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

      // セクションタイトルを挿入する
      this.cluster_svg.selectAll('rect.title')
        .data(this.section_title)
        .enter()
        .append('rect')
        .attr('class', 'title')
        .attr('x', x(0))
        .attr('y', (d) => y(d.start))
        .attr('width', x.bandwidth())
        .attr('height', (d) => y.bandwidth() * d.height)
        .attr('fill', 'white')
        .attr('stroke', '#969696')
        .attr('stroke-width', 2);

      this.cluster_svg.selectAll('text.section')
        .data(this.section_title)
        .enter()
        .append('text')
        .attr('class', 'section')
        .attr('x', this.svg_x(0) + 3)
        .attr('y', (d) => this.svg_y(Math.floor((d.end + d.start + 1) / 2)))
        .attr('fill', '#969696')
        .attr('font-size', this.svg_y.bandwidth())
        .text((d) => d.title.slice(0, 5));

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
            let hue = 360 * d.isin;
            hue /= this.cluster_group.length;
            color = `hsl( ${hue}, 70%, 50%)`;
          }
          return color;
        })
        .on('click', (data, i) => {
          this.hilightParagraph(i.y);
        });
      // ボタンの色変更
      this.cluster_group.forEach((_, i) => {
        let hue = 360 * i;
        hue /= this.cluster_group.length;
        const hsv = `hsl( ${hue}, 70%, 50%)`;
        this.cluster_group[i].color = `background-color: ${hsv}; color: white; border: solid 2px white`;
      });
    },
    changeClusterName(event) {
      const selectIndex = this.cluster_group.findIndex((d) => d.index === this.select_cluster);
      this.cluster_group[selectIndex].name = event.name;
    },
    // スライドを変更した時
    toggleMethod(item, i, isChange) {
      this.slide_page_num = i;
      this.selectSlide = item;
      this.selectAudio = this.audioContent[i];

      if (i === 0) {
        this.video_link = this.video_link_base;
      } else {
        const time = (Number(this.items[i - 1].split('_').slice(-1)[0].split('.')[0]) + 1) * 10;
        this.video_link = `${this.video_link_base}?autoplay=1#t=${time}s"`;
        // document.getElementById('presen_video').contentWindow.location.reload();
      }
      // ここではヒートマップの処理を行う
      const path = '/report_back';
      const payload = {
        select_slide: this.selectSlide,
      };
      axios.post(path, payload)
        .then((res) => {
          this.heatmap_data = res.data.heatmap_data;
          // this.heatmap.data.values = this.heatmap_data;
          // embed('#heatmap', this.heatmap);
          this.updateD3Method();
          if (isChange) {
            this.hilightParagraph(res.data.max_index);
          }
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    backHome() {
      window.location.href = '/';
    },
    // 論文上をクリックしたとき
    clickReport(e) {
      const el = document.getElementById('report');
      const payload = {
        x: e.offsetX,
        y: e.offsetY,
        width: el.clientWidth,
        height: el.clientWidth * 1.295,
        page_num: this.report_page,
      };
      const path = '/find_ref';
      this.isRefer = false;
      this.isWord = false;
      axios.post(path, payload)
        .then((res) => {
          const now = new Date();
          const Min = now.getMinutes();
          const Sec = now.getSeconds();
          if (res.data.file !== '' && res.data.file !== this.figureName && res.data.tag === 'figure') {
            // 図表を選択したとき
            this.isRefer = true;
            this.refer_table_data = res.data.table;
            this.figureName = res.data.file;
            this.figurePage = this.report_page;
            this.isParagraph = false;
            this.select_report_path = `/static/static/${this.fileName}/select.jpg?${Min}${Sec}`;
          } else if (res.data.tag === 'figure' && res.data.file === this.figureName) {
            // 同じ図表を選択した時
            this.figureName = '';
            this.isRefer = false;
            this.isParagraph = false;
            this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
          } else if (res.data.tag === 'paragraph') {
            // 段落を選択した時
            // もうすでに選択した段落を選択した場合
            if (this.paragraphIndex === res.data.index) {
              this.isParagraph = false;
              this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
              this.paragraphIndex = -1;
              this.svg.selectAll('rect.select').remove();
            } else {
              this.isParagraph = false;
              this.isParagraph = true;
              this.paragraphRefs = res.data.paragraph_ref;
              this.paragraphIndex = res.data.index;
              this.paragraphAdd = res.data.paragraph_add;
              this.haveReffer = (this.paragraphRefs.length > 0);
              // this.select_report_path =
              //  `/static/static/${this.fileName}/select.jpg?${Min}${Sec}`;
              this.hilightParagraph(this.paragraphIndex);
            }
          } else if (e.offsetX < el.clientWidth * 0.2) {
            // 左端をクリックした時→前のページへ飛ぶ
            this.movePrevPage();
          } else if (e.offsetX > el.clientWidth * 0.8) {
            // 右端をクリックした時->後のページへ飛ぶ
            this.moveNextPage();
          }
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    clickRow(item) {
      const index = item;
      this.hilightParagraph(index.index);
    },
    jumpToFigure() {
      this.report_page = this.figurePage;
      this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
    },
    // ビデオとスライドの切り替え
    changeVideo() {
      if (this.select === true) {
        this.select = true;
        this.select = false;
      } else {
        this.select = true;
      }
    },
    // クラスターを一つ選んだ時
    selectCluster(g, color) {
      this.cluster_color = color;
      if (this.isReport === false && this.select_cluster === g) {
        this.isReport = true;
        // クラスターのヒートマップをもとに戻す
        this.cluster_svg.selectAll('rect.heatmap')
          .data(this.cluster_data)
          .attr('fill-opacity', 1)
          .attr('stroke', 'white');
      } else {
        this.select_cluster_slide = this.cluster_slide[this.select_cluster];
        this.select_cluster = g;
        const path = '/cluster';
        const payload = {
          // selectCluster: this.select_cluster,
          selectCluster: g,
          fileName: this.fileName,
        };
        this.isReport = false;
        this.cluster_color = d3.schemePaired[this.select_cluster];
        axios.post(path, payload)
          .then((res) => {
            this.cluster_img_list = res.data.img_list;
            this.table_data = res.data.table_data;
          })
          .catch((error) => {
            // eslint-diable-next-line
            console.error(error);
          });
        this.cluster_wordcloud_path = `static/static/${this.fileName}/wordcloud/${this.select_cluster}.png`;
        // ヒートマップの変更(関係ないとこは少し透明になる)
        this.cluster_svg.selectAll('rect.heatmap')
          .data(this.cluster_data)
          .attr('fill-opacity', (d) => {
            let opacity = 0.2;
            if (d.isin === g) {
              opacity = 1.0;
            }
            return opacity;
          })
          .attr('stroke', (d) => {
            let stroke = 'white';
            if (d.isin === g) {
              stroke = '#969696';
            }
            return stroke;
          });
      }
    },
    // 論文を写すかクラスタービューを写すかの切り替え
    changeReport() {
      let cluster = this.select_cluster;
      if (this.select_cluster === '') cluster = 0;
      if (this.isReport) {
        this.selectCluster(cluster);
        this.isReport = false;
      } else {
        this.isReport = true;
        // クラスターのヒートマップをもとに戻す
        this.cluster_svg.selectAll('rect.heatmap')
          .data(this.cluster_data)
          .attr('fill-opacity', 1)
          .attr('stroke', 'white');
      }
    },
    // 選ばれたパラグラフをハイライトする
    hilightParagraph(index) {
      console.log(index);
      this.svg.selectAll('rect.select').remove();
      this.isReport = true;
      const payload = {
        select_paragraph: index,
      };
      const path = '/select';
      axios.post(path, payload)
        .then((res) => {
          if (res.data > -1) {
            this.report_page = res.data - 0;
            this.select_report_path = `/static/static/${this.fileName}/select.jpg?${index}`;
            this.not_paragraph = false;
          } else {
            this.not_paragraph = true;
          }
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
      // 選んだ部分をd3上でハイライトする
      this.svg.append('rect').attr('class', 'select')
        .attr('x', this.svg_x(1))
        .attr('y', this.svg_y(index))
        .attr('width', this.svg_x.bandwidth())
        .attr('height', this.svg_y.bandwidth())
        .style('fill', 'rgb(0,0,0,0)')
        .style('stroke', 'red')
        .style('stroke-width', 2);
    },
    moveNextPage() {
      if (this.report_page < this.report_max_page) this.report_page += 1;
      this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
      this.not_paragraph = false;
      this.isReport = true;
    },
    movePrevPage() {
      if (this.report_page > 0) this.report_page -= 1;
      this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
      this.not_paragraph = false;
      this.isReport = true;
    },
    // パラグラフの移動
    // moveParagraph() {
    //   this.isParagraph = false;
    //   this.isParagraph = true;
    //   this.paragraphRefs = res.data.paragraph_ref;
    //   this.paragraphIndex = res.data.index;
    //   this.paragraphAdd = res.data.paragraph_add;
    //   this.haveReffer = (this.paragraphRefs.length > 0);
    //   this.select_report_path = `/static/static/${this.fileName}/select.jpg?${Min}${Sec}`;
    // },
    hideRefer() {
      if (this.isRefer && this.chip_refer) {
      // メモの送信
        const payload = {
          tag: 'report-figure',
          note: '',
          id: 0,
          stamp: this.chip_item[this.chip_refer].title,
          content: this.figureName,
        };
        const path = '/note_save';
        axios.post(path, payload)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      }
      this.isRefer = false;
      this.isParagraph = false;
      // 論文のページ表示の変更
      this.select_report_path = `${this.report_basic_path}/${this.report_page}.jpg`;
      // 今後の動作のための処理
      this.paragraphIndex = -1;
      this.figureName = '';
      this.svg.selectAll('rect.select').remove();
    },
    // 右クリックした時
    onleftclick(e) {
      if (this.showTool === true) {
        this.showTool = false;
      } else {
        this.clickReport(e);
      }
    },
    onrightclick(e) {
      this.menu_position = {
        top: `${e.pageY}px`,
        left: `${e.pageX}px`,
      };
      this.tool_x = e.pageX;
      this.tool_y = e.pageY;
      this.showTool = true;
      // この右クリックがどちらのものか判定
      const slideWidth = document.documentElement.offsetWidth * 0.34;
      if (e.pageX < slideWidth) {
        this.tag = 'slide';
      } else {
        this.tag = 'report-page';
      }
    },
    // スライドと論文のどちらを選択したか保存すtる
    // 右ツールバーでメモした時
    selectTool(stamp) {
      let content = '';
      if (this.tag === 'slide') content = this.slide_page_num;
      else content = this.report_page;
      const payload = {
        tag: this.tag,
        note: '',
        id: 0,
        stamp: stamp.title,
        content,
      };
      const path = '/note_save';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    changeDisplayNote() {
      if (this.doDisplayNote) this.doDisplayNote = false;
      else this.doDisplayNote = true;
      console.log('実験');
    },
    // ノートがsaveされた時に色々なものを変更する関数
    reloadNote() {
      console.log('saveされました');
      if (this.doDisplayNote) this.$refs.noteDisplay.reload();
      else this.$refs.wordContent.importNoteInfo();
    },
  },
  created() {
    this.getData();
  },
  watch: {
    loginName() {
      if (this.loginName !== '') this.isLogin = true;
      else this.isLogin = false;
    },
  },
};
</script>

<style>
a.btn {
  border: 2px solid #696969;
  color: #696969;
  width: 50px;
}
a.btn1 {
  border: 2px solid #696969;
  color: #696969;
  width: 50px;
}
.audioTranscript {
  height: 200px;
  overflow-y: scroll;
}
</style>
