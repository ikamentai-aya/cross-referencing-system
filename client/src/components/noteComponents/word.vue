<template>
  <div>
    <h2>word</h2>
    <div class="row">
      <div class="col-6">
        <v-autocomplete
          v-model="select_word"
          :items="wordCandidate"
          dense
          label=""
          @change="selectWord"
        ></v-autocomplete>
      </div>
    </div>
    <p>{{select_word_note}} </p>
    <p v-if="notHaveWord">単語は追加されていません</p>
    <div style="height:400px; overflow-y:scroll;">
      <table border="1" class = "scroll">
        <tr>
          <th>Word</th>
          <th>Translation</th>
        </tr>
        <tr v-for="item in content" :key="item"
        :bgcolor=item.color @click="clickWord(item)">
          <td><small>{{item.content}}</small></td>
          <td><small>{{item.note}}</small></td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WordContent',
  props: ['isWord', 'login_name'],
  data() {
    return {
      content: [],
      wordCandidate: [],
      notHaveWord: false,
      select_word: '',
    };
  },
  methods: {
    selectWord() {
      console.log('select', this.select_word);
      this.select_word_note = this.content.find((el) => el.content === this.select_word).note;
      console.log(this.select_word_note);
    },
    clickWord(item) {
      this.select_word = item;
    },
    importNoteInfo() {
      const payload = {
        tag: 'word',
        id: this.login_name,
      };
      const path = '/note_get';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data.content.length);
          if (res.data.content.length === 0) {
            this.message = '単語は追加されていません';
            this.notHaveWord = true;
            console.log('単語なし');
          } else {
            console.log(res.data);
            this.message = '今までに追加した単語を表示します';
            this.notHaveWord = false;
            this.content = res.data.content;
            this.wordCandidate = this.content.map((key) => key.content);
          }
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
  },
  watch: {
    isWord() {
      this.importNoteInfo();
    },
  },
};
</script>

<style>
table.scroll {
  height: 400pt;
  overflow-y: scroll;
}
</style>
