<template>
  <div>
    <h2>Notes on the entire paper</h2>
    <br>
    <div style="overflow-y: scroll; height: 500px; margin:10px">
      <v-alert v-for="i in memo_list" :key="i"
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
</template>

<script>
import axios from 'axios';

export default {
  name: 'allContent',
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
      // noteに関する情報の取得
      console.log(this.login_name);
      const payload = {
        tag: 'none',
        id: this.login_name,
      };
      const path = '/note_get';
      this.selectfile = '';
      axios.post(path, payload)
        .then((res) => {
          console.log('all');
          this.memo_list = res.data.content;
          this.memo_list = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
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
    tab() {
      if (this.tab === 'all') {
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
