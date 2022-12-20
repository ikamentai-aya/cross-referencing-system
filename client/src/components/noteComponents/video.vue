<template>
  <div>
    <h2> Video Note</h2>
    <div class="row" id="row">
      <div class="col-6" id="col6">
        <iframe id="presen_video" :src="videoLink" :width = "videoWidth" :height="videoHeight"
          title="movie" frameborder="0" allow="autoplay; fullscreen"
          style="border-style: ridge" allowfullscreen>
        </iframe>
      </div>
      <div class="col-6">
        <v-alert v-for="item in memo_list" :key="item"
        outlined :color="color[item.stamp]" dense
        >
          <div class="block">
            <p><strong>Author:{{item.id}}</strong></p>
          </div>
          <div class="block">
            <a href="#" @click="deleteNote(item)" width="50" style="text-align:right;">
              <v-icon color=#696969>mdi-delete</v-icon>
            </a>
          </div>
          <p>{{item.content}}</p>
          <p>{{item.note}}</p>
        </v-alert>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'videoContent',
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
      videoLink: '',
      videoWidth: '500pt',
      videoHeight: '281pt',
    };
  },
  methods: {
    importNoteInfo() {
      const payload = {
        tag: 'video',
        id: this.login_name,
      };
      const path = '/note_get';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data);
          this.memo_list = res.data.content;
          this.memo_list = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
          this.videoLink = res.data.videoLink;
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
      if (this.report === 'video') {
        console.log('ページ');
        this.importNoteInfo();
      }
    },
  },
  created() {
    this.importNoteInfo();
    // console.log(document.getElementById('row').clientWidth);
    // this.videoWidth = `${document.getElementById('row').clientWidth * 0.4}pt`;
    // this.videoHeight = `${document.getElementById('row').clientWidth * 0.71}pt`;
    // this.videoWidth = '300pt';
  },
};
</script>

<style>
.block{
  display: inline-block;
}
</style>
