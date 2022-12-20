<template>
  <div>
    <h2>Figure Note</h2>
    <br>
    <div style="overflow-y: scroll; height: 500px">
      <div v-for="item in memo_list" :key="item">
        <p>{{item.name}}</p>
        <div class="row">
          <div class="col-2">
            <v-img :src = item.path></v-img>
          </div>
          <div class="col-10">
            <v-alert v-for="i in item.memo_list" :key="i"
            outlined :color="color[i.stamp]" dense
            >
              <div class="block">
                <p><strong>Author:{{i.id}}</strong></p>
              </div>
              <div class="block">
                <a href="#" @click="deleteNote(i)" width="50" style="text-align:right;">
                  <v-icon color=#696969>mdi-delete</v-icon>
                </a>
              </div>
              <p>{{i.note}}</p>
            </v-alert>
          </div>
        </div>
        <br>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'figureContent',
  props: ['report', 'login_name', 'stamp_list'],
  data() {
    return {
      memo_list: [],
      color: {
        何となく大事: '#FFB55B',
        論文の要: '#d92626',
        後で読む: '#26d98e',
        分からない: '#7f26d9',
      },
    };
  },
  methods: {
    importNoteInfo() {
      // noteに関する情報の取得
      let payload = {
        tag: 'report-figure',
        id: this.login_name,
      };
      let path = '/note_get';
      this.selectfile = '';
      axios.post(path, payload)
        .then((res) => {
          this.content = res.data.content;
          this.content = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
          this.selectfile = res.data.selectfile;
          console.log(res.data.content, this.selectfile);
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
      // その他表示に必要な情報を取得する
      payload = {};
      path = '/note_info';
      this.figure_name_list = [];
      axios.post(path, payload)
        .then((res) => {
          this.figure_name_list = res.data.figure_name_list;
          this.memo_list = [];
          // 表示するものの調整を行う
          console.log(this.figure_name_list, this.content);
          this.figure_name_list.forEach((name) => {
            console.log(name);
            this.memo_list.push({
              name,
              path: `static/static/${this.selectfile}/report_content/figure/${name}.jpg`,
              memo_list: this.content.filter((i) => i.content === name),
            });
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteNote(i) {
      const payload = {
        item: i,
      };
      const path = '/note_delete';
      axios.post(path, payload)
        .then((res) => {
          console.log('success', res.data);
          this.importNoteInfo();
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
  },
  watch: {
    report() {
      if (this.report === 'figure') {
        this.importNoteInfo();
        console.log('情報を取得しました');
      }
    },
  },
  created() {
    this.importNoteInfo();
  },
};
</script>
