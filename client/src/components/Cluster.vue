<template>
  <div>
    <div class="row">
      <h5 :style="this.clusterColor"><font>Summary of clusters:</font>
        <input v-model="message" :placeholder="selectClusterName" @change="changeName">
      </h5>
      <br>
      <div class="col-6" style="position: relative">
        <div class="row">
          <div class="col-6">
            <wordcloud-component
              v-bind:selectCluster="this.selectCluster"
            />
          </div>
          <div class="col-6">
            <!-- クラスターに所属するスライドの表示 -->
            <p v-if="isSlide">Slides similar to the selected cluster</p>
            <div v-for="item in selectClusterSlide" :key="item">
              <v-img fluid :src="item"></v-img>
            </div>
          </div>
        </div>
        <br>
        <!-- <v-gallery max-width="400" :images="clusterImgList"></v-gallery> -->
        <!-- 段落の位置を画像で表示 -->
        <div class="row">
          <div class="col-3" v-for="item in clusterImgList" :key="item">
            <v-img class="slide" :src="item.url" @click="selectImg(item)"></v-img>
            <p><small>{{item.title}}ページ</small></p>
          </div>
        </div>
        <!-- 選択した画像を拡大表示 -->
        <div class="col-12" v-if="doesSelectItem" style="position: absolute; top:0px; left:0px;">
          <div class="card">
            <div class="row">
              <div class="col-11">
                <p>{{selectPage.title}}ページ</p>
              </div>
              <div class="col-1">
                <a href='#' class="btn1" @click="swicthIsShow">×</a>
              </div>
            </div>
            <v-img :src="selectPage.url" @click="clickParagraph" id="selectPage"></v-img>
          </div>
        </div>
      </div>
      <div class="col-6">
        <div v-if="isSelect">
          <div class="row">
            <div class="col-8">
              <p>
                Select Paragraph: {{selectItem.index}}
              </p>
            </div>
            <div class="col-2">
              <a href='#' class="btnclose" @click="swicthIsSelect">
                <v-icon color=#ff6347>mdi-close</v-icon>
              </a>
            </div>
            <div class="col-2">
              <a class="btncheck">
                <v-icon color=#7cfc00>mdi-check</v-icon>
              </a>
            </div>
          </div>
          <div class="selectParagraph">
            <p><small>{{selectItem.all}}</small></p>
          </div>
        </div>
        <!-- クラスターに所属する段落を表で示す -->
        <table border="1">
          <tr>
            <th></th>
            <th>Section</th>
            <th>Start of sentence</th>
            <th>Key Words</th>
          </tr>
          <tr v-for="item in showTableData" :key="item" @click="selectOneParagraph(item)"
          :bgcolor=item.color>
            <td>{{item.index}}</td>
            <td><small>{{item.section}}</small></td>
            <td><small>{{item.start}}</small></td>
            <td><small>{{item.tag}}</small></td>
          </tr>
        </table>
        <br>
        <!-- 表データで映す部分を変更する -->
        <a href='#' v-for="item in tableIndex" class="btn"
          :key="item" @click="switchDisplayrange(item)">{{item}}</a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import WordCloudComponent from './WordCloud.vue';

export default {
  name: 'ClusterComponent',
  components: {
    'wordcloud-component': WordCloudComponent,
  },
  props: ['selectCluster', 'clusterColor', 'clusterWordcloudPath',
    'clusterImgList', 'selectClusterSlide', 'tableData', 'clusterGroup'],
  data() {
    return {
      headers: [
        { text: 'Section', value: 'section' },
        { text: 'start of a sentence', value: 'start' },
      ],
      selectItem: [],
      isSelect: false,
      showTableData: [],
      doesSelectItem: false,
    };
  },
  methods: {
    selectOneParagraph(item) {
      console.log(item);
      this.selectItem = item;
      this.isSelect = true;
    },
    swicthIsSelect() {
      this.isSelect = false;
    },
    switchDisplayrange(item) {
      console.log(item * 5, item * 5 + 5);
      this.showTableData = this.tableData.slice(item * 5, item * 5 + 5);
      console.log(this.tableData.slice(item * 5, item * 5 + 5));
    },
    // 一つの画像を選択したら、その画像を拡大表示するための関数
    selectImg(item) {
      console.log(item);
      this.selectPage = item;
      this.doesSelectItem = true;
    },
    // 画像の拡大表示を終了する
    swicthIsShow() {
      this.doesSelectItem = false;
    },
    // 画像から段落を選択する
    clickParagraph(e) {
      // 画像の情報を取得
      const el = document.getElementById('selectPage');
      const payload = {
        x: e.offsetX,
        y: e.offsetY,
        width: el.clientWidth,
        height: el.clientWidth * 1.295,
        page_num: this.selectPage.title,
      };
      const path = '/find_ref';
      this.isRefer = false;
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data.index);
          const isMatch = (element) => `${element.index}` === `${res.data.index}`;
          const index = this.tableData.findIndex(isMatch);
          if (index > -1) {
            this.selectItem = this.tableData[index];
            this.isSelect = true;
          }
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    changeName() {
      console.log(this.message);
      this.$emit('change', { name: this.message, cluster: this.selectCluster });
    },
  },
  watch: {
    tableData() {
      this.isSelect = false;
      // 表を最大でも5件まで表示するための操作
      const listLength = this.tableData.length;
      if (listLength % 5 === 0) {
        this.tablePage = Math.floor(listLength / 5);
      } else {
        this.tablePage = Math.floor(listLength / 5) + 1;
      }
      this.tableIndex = Array.from(Array(this.tablePage), (v, k) => k);
      this.showTableData = this.tableData.slice(0, 5);
      this.tableNum = 0;
      console.log(this.selectCluster);
      const selectIndex = this.clusterGroup.findIndex((d) => d.index === this.selectCluster);
      this.selectClusterName = this.clusterGroup[selectIndex].name;
    },
    selectClusterSlide() {
      if (this.selectClusterSlide.length > 0) {
        this.isSlide = true;
      } else {
        this.isSelect = false;
      }
    },
    message() {
      console.log(this.message);
    },
  },
};
</script>

<style>
th, td {
  border: solid 1px #A1A3A6;
  padding:5px;
}
tr:active {
  background-color: skyblue;
}

th {
  color: #696969;
}
a.btn {
  border: 2px solid #696969;
  color: #696969;
}
a.btn1 {
  border: 0.5px solid #696969;
  padding: 5px;
}
a.btnclose {
  border: 2px solid #ff6347;
  padding: 5px;
}
a.btncheck {
  border: 2px solid lawngreen;
  padding: 5px;
}
a.btn:active {
  border: 2px solid skyblue;
  color: #696969;
}
.selectParagraph {
  height: 200px;
  overflow: scroll;
}
.card {
  border: solid 1px #A1A3A6;
  padding:5px;
}
.slide {
  border: solid 0.5px #A1A3A6;
}
</style>
