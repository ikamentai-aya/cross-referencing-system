<template>
  <v-dialog
    transition="dialog-bottom-transition"
    max-width="600"
    v-model="dialog"
  >
    <template v-slot:activator="{ on, attrs }">
      <a href="#" class="btn"
        v-bind="attrs"
        v-on="on"
      ><v-icon color=#69696>mdi-note-edit-outline</v-icon></a>
    </template>
    <template v-slot:default="dialog">
      <v-card>
        <v-card-title>Note</v-card-title>
        <v-card-text>
          <v-alert
            dense
            text
            type="error"
          >
            ここで保存したメモは他の人に見られる可能性があります。
            <strong>プライベートな内容の記述はお控えください</strong>
          </v-alert>
          <div>
            <p>Data:</p>
            <v-tabs v-model="tab">
              <!-- どのコンテンツを選ぶのか -->
              <v-tab href="#report">Report
                <v-icon>mdi-file</v-icon>
              </v-tab>
              <v-tab href="#video">Video
                <v-icon>mdi-play-box-outline</v-icon>
              </v-tab>
              <v-tab href="#slide">Slide
                <v-icon>mdi-presentation-play</v-icon>
              </v-tab>
              <v-tab href="#word">Word
                <v-icon>mdi-keyboard-settings-outline</v-icon>
              </v-tab>
              <v-tab href="#none">None
                <v-icon>mdi-border-none-variant</v-icon>
              </v-tab>
              <!-- 論文を選んだ時 -->
              <v-tab-item value='report'>
                <v-tabs background-color='#26D9D9' dark v-model="report">
                  <v-tab href="#page">Page<v-icon></v-icon></v-tab>
                  <v-tab href="#section">Section</v-tab>
                  <v-tab href="#paragraph">Paragraph&sentence</v-tab>
                  <v-tab href="#figure">Figure</v-tab>
                  <!-- 論文のページを選択 -->
                  <v-tab-item value = 'page'>
                    <br>
                    <div class="row">
                      <div class="col-4">
                        <div style="border-style: ridge">
                          <v-img :src = "reportPath" v-if="displayReport"></v-img>
                        </div>
                      </div>
                      <div class="col-8">
                        <p>Please select a page of interest.</p>
                        <p><input v-model="selectReportPage" @change="changeReportPage">
                        /{{report_max_page}}</p>
                      </div>
                    </div>
                  </v-tab-item>
                  <!-- 論文のセクションを選択 -->
                  <v-tab-item value = 'section'>
                    <v-select
                      :items="section_list"
                      v-model="selectSectionIndex"
                      @change="changeSection"
                      width = '10px'
                    ></v-select>
                    <p>{{sectionHead}}</p>
                  </v-tab-item>
                  <!-- 論文の段落を選択 -->
                  <v-tab-item value="paragraph">
                    <br>
                    <p>Please select a <strong>Paragraph</strong> of interest.</p>
                    <p> <input v-model="selectReportParagraph" @change="changeReportParagraph">
                      /0~{{report_max_paragraph}}</p>
                    <p class="paragraph" id = "p_paragraph"
                    @mouseup="selectSentence">{{paragraph}}</p>
                    <v-checkbox
                      v-model="isSentence"
                      v-if="isSentence"
                      label="Select Sentence"
                    ></v-checkbox>
                  </v-tab-item>
                  <!-- 図表を選択した場合 -->
                  <v-tab-item value = 'figure'>
                    <div class="row">
                      <div class="col-6">
                        <br>
                        <p>Please select a <strong>Figure or Table</strong> of interest.</p>
                        <v-img fluid :src="figurePath" contain v-if="displayFigure"></v-img>
                      </div>
                      <div class="col-6">
                        <v-select
                          :items="figure_name_list"
                          v-model="selectFigure"
                          @change="changeFigure"
                          width = '10px'
                        ></v-select>
                      </div>
                    </div>
                  </v-tab-item>
                </v-tabs>
              </v-tab-item>
              <!-- 動画を選んだ時 -->
              <v-tab-item value='video'>
                <div class="row">
                  <div class="col-6">
                    <br>
                    <iframe id="presen_video" :src="videoLink" :width="video_width"
                      :height="video_height"
                      title="movie" frameborder="0" allow="autoplay; fullscreen"
                      style="border-style: ridge" allowfullscreen>
                    </iframe>
                  </div>
                  <div class="col-6">
                    <br>
                    <v-text-field label='Time(mm:dd)' v-model="videoTime">
                    </v-text-field>
                  </div>
                </div>
              </v-tab-item>
              <!-- スライドを選んだ時 -->
              <v-tab-item value='slide'>
                <div class="row">
                  <div class="col-6">
                    <v-img fluid :src="slidePath" v-if="displaySlide"></v-img>
                  </div>
                  <div class="col-6">
                    <p>select page number</p>
                    <div class="row">
                      <div class="col-6">
                        <v-select
                          :items="slideIndexList"
                          v-model="selectIndex"
                          @change="changeSlide"
                          width = '10px'
                        ></v-select>
                      </div>
                      <div class="col-6">
                        <p>/{{slideNum}}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </v-tab-item>
              <!-- wordを選んだ時 -->
              <v-tab-item value='word'>
                <br>
                <v-autocomplete
                  v-model="selectWord"
                  :items="items"
                  dense
                  label="Word"
                ></v-autocomplete>
              </v-tab-item>
            </v-tabs>
            <!-- それに対して何を行うのか -->
            <p>Action:</p>
            <v-textarea
              outlined
              name="input-7-4"
              label="comment"
              v-model="text"
            ></v-textarea>
            <!-- ボタンの類 -->
          <v-chip-group
            v-model="stamp"
            column
          >
            <v-chip v-for="tip in tip_item" :key="tip" filter outlined :color="tip.color">
              {{tip.title}}
            </v-chip>
          </v-chip-group>
          <v-alert
            dense
            outlined
            type="error"
            v-if="isAlert"
          >
            <strong>Paper not selected.</strong> Please select a paper.
          </v-alert>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            depressed
            color='#26D9D9'
            dark
            @click="save"
          >
            Save
          </v-btn>
          <v-btn
            text
            @click="dialog.value = false"
          >Close</v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import axios from 'axios';
// import jQuery from 'jquery';

export default {
  name: 'NoteTaking',
  props: ['videoLink', 'slide_page_num', 'selectSlide', 'slideItems',
    'select_report_path', 'report_max_page', 'report_basic_path', 'login_name', 'is_login'],
  data() {
    return {
      items: ['いちご', 'みかん', 'りんご'],
      displayReport: true,
      displaySlide: true,
      displayFigure: true,
      figurePath: '',
      paragraph: '',
      sectionHead: '',
      is_saved: false,
      stamp: 0,
      text: '',
      isSentence: false,
      tip_item: [
        { color: '#d92626', title: '論文の要' },
        { color: '#FFB55B', title: '何となく大事' },
        { color: '#26d98e', title: '後で読む' },
        { color: '#7f26d9', title: '分からない' },
        { color: '#268ed9', title: '英語の勉強' },
      ],
    };
  },
  methods: {
    // 表示するスライドを選択する
    changeSlide() {
      this.slidePath = this.slideItems[this.selectIndex];
      this.displaySlide = false;
      this.displaySlide = true;
      console.log('変更', this.selectIndex, this.slidePath);
      console.log(this.tab);
    },
    // 論文のページを変更した時
    changeReportPage() {
      this.reportPath = `${this.report_basic_path}/${this.selectReportPage}.jpg?${this.getTime()}`;
      // 変更を処理するための操作（一回画像を消してから表示する）
      this.displayReport = false;
      this.displayReport = true;
    },
    changeSection() {
      this.sectionHead = this.section_head_list[this.selectSectionIndex];
    },
    // 段落を変更した時
    changeReportParagraph() {
      // 文章選択ができるようにする
      if (this.paragraph === '') {
        const pElement = document.querySelector('p.paragraph');
        console.log('文選択', pElement);
        window.addEventListener('selectionchange', () => {
          console.log(window.getSelection().toString);
        });
      }
      if (this.selectReportParagraph >= 0
        && this.selectReportParagraph <= this.report_max_paragraph) {
        this.paragraph = this.content[this.selectReportParagraph];
      } else if (this.selectReportParagraph < 0) {
        this.selectReportParagraph = 0;
        this.paragraph = this.content[this.selectReportParagraph];
      } else if (this.selectReportParagraph > this.report_max_paragraph) {
        this.selectReportParagraph = this.report_max_paragraph;
        this.paragraph = this.content[this.report_max_paragraph];
      }
    },
    // 図表を選択した場合
    changeFigure() {
      this.figurePath = `/static/static/${this.file}/report_content/figure/${this.selectFigure}.jpg`;
      console.log(this.figurePath, this.selectFigure, this.file);
      this.displayFigure = false;
      this.displayFigure = true;
    },
    // 現在の時刻を取得し、フォーマットする
    getTime() {
      const now = new Date();
      const Hour = now.getHours();
      const Min = now.getMinutes();
      const Sec = now.getSeconds();
      return `${Hour}${Min}${Sec}`;
    },
    // メモを保存するための関数
    save() {
      // メモの種類を記載
      let tag = '';
      if (this.tab === 'report') {
        tag = `report-${this.report}`;
      } else {
        tag = this.tab;
      }
      let content = '';
      if (this.tab === 'report') {
        if (this.report === 'page') {
          content = this.selectReportPage;
        } else if (this.report === 'section') {
          content = this.selectSectionIndex;
        } else if (this.report === 'paragraph') {
          content = `${this.selectReportParagraph}-${this.paragraph}`;
        } else if (this.report === 'figure') {
          content = this.selectFigure;
        }
      } else if (this.tab === 'video') {
        content = this.videoTime;
      } else if (this.tab === 'slide') {
        content = this.selectIndex;
      } else if (this.tab === 'word') {
        content = this.selectWord;
      }
      const payload = {
        tag,
        note: this.text,
        id: this.login_name,
        stamp: this.tip_item[this.stamp].title,
        content,
      };
      const path = '/note_save';
      axios.post(path, payload)
        .then((res) => {
          this.is_saved = true;
          this.text = '';
          this.stamp = 0;
          console.log(res.data);
          this.$emit('save');
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    // 文の選択
    selectSentence() {
      console.log('選択されました');
      if (this.isSentence) {
        const paragraph = document.getElementById('p_paragraph');
        paragraph.removeChild(paragraph.lastChild);
        paragraph.removeChild(paragraph.lastChild);
      }
      let selection;
      if (window.getSelection) {
        selection = window.getSelection();
        console.log(selection, selection.toString());
      } else if (document.selection) {
        selection = document.selection.createRange();
        console.log(selection);
      }
      const afterEl = document.createElement('span');
      const after = this.paragraph.substr(selection.getRangeAt(0).endOffset);
      afterEl.textContent = after;
      // this.paragraph = selection;
      const before = this.paragraph.substr(0, selection.getRangeAt(0).startOffset);
      this.paragraph = before;
      console.log(this.paragraph);
      // ハイライト箇所の作成
      const el = document.createElement('span');
      el.className = 'highlight';
      el.textContent = selection;

      const paragraph = document.getElementById('p_paragraph');
      paragraph.appendChild(el);
      console.log(afterEl);
      paragraph.appendChild(afterEl);
      this.isSentence = true;
    },
    // 文の選択を解除
    resetSelectSectence() {
      const paragraph = document.getElementById('p_paragraph');
      paragraph.removeChild(paragraph.lastChild);
      paragraph.removeChild(paragraph.lastChild);
      this.paragraph = this.content[this.selectReportParagraph];
      this.isSentence = false;
    },
  },
  watch: {
    isSentence() {
      if (!this.isSentence) this.resetSelectSectence();
    },
    selectSlide() {
      this.slidePath = this.selectSlide;
      this.slideNum = this.slideItems.length;
      this.slideIndexList = this.slideItems.map((d, i) => i + 1);
      this.selectReportPage = this.report_page;
      this.reportPath = this.select_report_path;
      console.log(this.reportPath);
      // セクションについて取得する
      const payload = {};
      const path = '/note_info';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data);
          this.file = res.data.file;
          this.content = res.data.content;
          this.report_max_content = this.content.length - 1;
          this.section_list = res.data.section_list;
          this.section_head_list = res.data.section_head;
          this.report_max_paragraph = this.content.length;
          this.figure_name_list = res.data.figure_name_list;
          this.items = res.data.word_list;
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
  },
  created() {
    console.log('note taking vue created');
  },
};
</script>

<style>
v-button.objective {
  border: solid 1px #A1A3A6;
}
.highlight {
  background: linear-gradient(transparent 40%, aqua 40% 90%, transparent 90%);
}
</style>
