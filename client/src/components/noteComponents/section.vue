<template>
  <div>
    <h2>Section Note</h2>
    <div style="overflow-y: scroll; height: 500px">
      <div v-for="item in memo_list" :key="item">
        <p class="big">{{item.bigSection}}</p>
        <p v-for="note in item.memo_list" :key ="note">
          {{note.note}}
        </p>
        <div v-for="s in item.section_list" :key="s">
          <p class="middle">{{s.name}}</p>
          <p v-for="n in s.memo_list" :key ="n">
            {{n.note}}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'sectionContent',
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
    // noteに関する情報の取得
    importNoteInfo() {
      let payload = {
        tag: 'report-section',
        id: this.login_name,
      };
      let path = '/note_get';
      this.selectfile = '';
      axios.post(path, payload)
        .then((res) => {
          this.content = res.data.content.filter((key) => this.stamp_list.includes(key.stamp));
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
          this.section_list = res.data.section_list;
          this.section_structure = res.data.section_structure;
          this.memo_list = [];
          // 表示するものの調整を行う
          this.section_structure.forEach((key) => {
            const bigSection = key[0];
            const sList = key[1];
            const sectionList = [];
            if (sList.length > 0) {
              sList.forEach((s) => {
                sectionList.push({
                  name: s,
                  memo_list: this.content.filter((i) => i.content === s),
                });
              });
            }
            this.memo_list.push({
              bigSection,
              memo_list: this.content.filter((i) => i.content === bigSection),
              section_list: sectionList,
            });
          });
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
        .then(() => {
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
      if (this.report === 'section') {
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
</style>
