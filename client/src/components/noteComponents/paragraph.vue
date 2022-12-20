<template>
  <div>
    <h2>Paragraph & Sentence Note</h2>
    <div style="overflow-y: scroll; height: 500px">
      <div v-for="item in memo_list" :key="item">
        <p class="big">{{item.bigSection}}</p>
        <div v-for="note in item.memo_list" :key ="note">
          <p :style="style[note.stamp]">{{note.sentence}}</p>
          <p class="memo">{{note.note}}</p>
        </div>
        <div v-for="s in item.section_list" :key="s">
          <p class="middle">{{s.name}}</p>
          <!-- <p v-for="n in s.memo_list" :key ="n">
            {{n.note}}
          </p> -->
          <div v-for="n in s.memo_list" :key ="n">
            <p class="content">{{n.sentence}}</p>
            <p class="memo">{{n.note}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'paragraphContent',
  props: ['report', 'login_name', 'stamp_list'],
  data() {
    return {
      memo_list: [],
      content: [],
      color: {
        何となく大事: '#FFB55B',
        論文の要: '#d92626',
        後で読む: '#26d98e',
        分からない: '#7f26d9',
      },
      style: {
        何となく大事: 'border-left: 10px solid #FFB55B; padding 1em;',
        論文の要: 'border-left: 10px solid #d92626; padding 1em;',
        後で読む: 'border-left: 10px solid #26d98e; padding 1em;',
        分からない: 'border-left: 10px solid #7f26d9; padding 1em;',
      },
    };
  },
  methods: {
    // noteに関する情報の取得
    importNoteInfo() {
      let payload = {
        tag: 'report-paragraph',
        id: this.login_name,
      };
      let path = '/note_get';
      this.selectfile = '';
      axios.post(path, payload)
        .then((res) => {
          this.content = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
          console.log(this.content);
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
      // その他表示に必要な情報を取得する
      payload = {};
      path = '/note_info';
      this.figure_name_list = [];
      console.log(this.content);
      axios.post(path, payload)
        .then((res) => {
          this.section_list = res.data.section_list;
          this.memo_list = [];
          this.section_structure = res.data.section_structure;
          this.section_structure.unshift(['', []]);
          // 表示するものの調整を行う
          this.section_structure.forEach((key) => {
            const bigSection = key[0];
            const sList = key[1];
            const sectionList = [];
            if (sList.length > 0) {
              sList.forEach((s) => {
                sectionList.push({
                  name: s,
                  memo_list: this.content.filter((c) => c.section === s),
                });
              });
            }
            this.memo_list.push({
              bigSection,
              memo_list: this.content.filter((c) => c.section === bigSection),
              section_list: sectionList,
            });
          });
          console.log(this.memo_list);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // 選択したメモを消去する関数
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
      if (this.report === 'paragraph') {
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

<style>
p.big {
  background-color: #e3f6f5;
  border-left: 10px solid #26D9D9;
  font-size: 24pt;
}
p.middle {
  background-color: #e3f6f5;
  border-left: 10px solid #26D9D9;
  font-weight: bold;
  font-size: 16pt;
}
p.memo {
  padding: 1em;
  background-color: #f5f5f5;
}
</style>
