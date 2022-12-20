<template>
  <div>
    <br>
    <h2>Slide Note</h2>
    <br>
    <div style="overflow-y: scroll; height: 500px">
      <div v-for="item in memo_list" :key="item">
        <p>{{item.index}}ページ</p>
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
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'slideContent',
  props: ['tab', 'login_name', 'stamp_list'],
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
      let payload = {
        tag: 'slide',
        id: this.login_name,
      };
      let path = '/note_get';
      axios.post(path, payload)
        .then((res) => {
          this.report_max_page = res.data.report_max_page;
          this.content = res.data.content;
          this.content = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
      // そのほかの情報の取得
      payload = {};
      path = '/note_info';
      this.figure_name_list = [];
      axios.post(path, payload)
        .then((res) => {
          this.slide_files = res.data.slide_files;
          this.memo_list = [];
          // 表示するものの調整を行う
          this.slide_files.forEach((key, index) => {
            console.log(key);
            this.memo_list.push({
              path: key,
              memo_list: this.content.filter((i) => i.content === index + 1),
              index,
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
    tab() {
      // タブがpageに変更された時のみ実行する
      if (this.tab === 'page') {
        console.log('ページ');
        this.importNoteInfo();
      }
    },
  },
  created() {
    this.importNoteInfo();
  },
};
</script>

<style>
.block{
  display: inline-block;
}
</style>
