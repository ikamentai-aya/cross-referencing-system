<template>
  <div>
    <br>
    <h2>Page Note</h2>
    <br>
    <div style="overflow-y: scroll; height: 500px">
      <div v-for="item in memo_list" :key="item">
        <p>{{item.page}}ページ</p>
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
  name: 'PageContent',
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
      const payload = {
        tag: 'report-page',
        id: this.login_name,
      };
      const path = '/note_get';
      axios.post(path, payload)
        .then((res) => {
          this.report_max_page = res.data.report_max_page;
          this.content = res.data.content;
          // const newContent = [];
          this.content = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
          this.report_basic_path = `/static/static/${res.data.selectfile}/report_content/content/`;
          this.page_list = [...Array(this.report_max_page)].map((_, i) => i);
          this.memo_list = [];
          this.page_list.forEach((i) => {
            this.memo_list.push({
              page: i,
              path: `${this.report_basic_path}${i}.jpg`,
              memo_list: this.content.filter((key) => String(key.content) === String(i)),
            });
          });
          console.log(this.memo_list);
        })
        .catch((error) => {
          // eslint-diable-next-line
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
      // タブがpageに変更された時のみ実行する
      if (this.report === 'page') {
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
