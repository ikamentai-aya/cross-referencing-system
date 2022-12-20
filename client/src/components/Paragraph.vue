<template>
  <div>
    <v-card-title>
      Paragraph：
      <a href="#" @click="jumpParagraph(paragraphIndex)">
        {{paragraphIndex}}
      </a>
    </v-card-title>
    <v-card-text>
    <div v-if="haveReffer">
      <div v-for="item in paragraphRefs" :key="item.name">
        <div class="row">
          <div class="col-6">
            <v-img fluid :src="item.path">
          </div>
          <div class="col-6">
            <p><a href="#" @click="jumpFigure(item.name)">{{ item.name }}</p>
          </div>
        </div>
      </div>
      <br>
    </div>
    <!-- 引用している論文のリスト表示 -->
    <div v-if="paragraphAdd.cite.isCite">
      <p>cited paper:</p>
      <p>
        <span v-for="item in paragraphAdd.cite.cite_list" :key="item">
          <a href='#' @click="displayCite(item)">[{{item}}],  </a></span>
      </p>
      <div v-if="isDetail">
        <div
        style="padding: 1px; margin-bottom: 1px; border: 1px dashed #333333; border-radius: 5px;">
          <p><small>{{cite_place}}</small></p>
        </div>
        <p><small>[{{select_cite_index}}] {{cite_detail}}</small></p>
      </div>
    </div>
    <!-- 類似している段落の表示 -->
    <table border="1">
      <tr>
        <th>index</th>
        <th>content</th>
      </tr>
      <tr v-for="item in paragraphAdd.paragraph" :key="item" :bgcolor=item.similarity
      @click="jumpParagraph(item.index)">
        <td>{{item.index}}</td>
        <td><small>{{item.content}}</small></td>
      </tr>
    </table>
    <p><small> Slides:
      <label for="option1">
        <input type="radio" id="option1" name="slide_num" value=1 @click="selectSlide(0)"/>
      </label>
      <label for="option2">
        <input type="radio" id="option1" name="slide_num" value=2 @click="selectSlide(1)"/>
      </label>
      <label for="option3">
        <input type="radio" id="option1"  name="slide_num" value =3 @click="selectSlide(2)"/>
      </label>
    </small></p>
    <v-img fluid :src="paragraphAdd.slide[slide_num].path" @click="jumpSlide"></v-img>
    <p>similarity:{{paragraphAdd.slide[slide_num].similarity}}
    , slide number:{{paragraphAdd.slide[slide_num].index}}</p>
    <v-chip-group column v-model="chip_paragraph">
      <v-chip v-for="tip in chip_item" :key="tip" filter outlined :color="tip.color">
        {{tip.title}}
      </v-chip>
    </v-chip-group>
    </v-card-text>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ParagraphComponent',
  props: ['paragraphIndex', 'paragraphRefs', 'haveReffer', 'paragraphAdd', 'isParagraph'],
  data() {
    return {
      headers: [
        {
          text: 'index', value: 'index',
        },
        { text: 'similarity', value: 'similarity' },
        { text: 'content', value: 'content' },
      ],
      cite_detail: '',
      cite_place: '',
      isDetail: false,
      select_cite_index: -1,
      // スライド関連
      slide_num: 0,
      chip_item: [
        { color: '#d92626', title: '論文の要' },
        { color: '#FFB55B', title: '何となく大事' },
        { color: '#26d98e', title: '後で読む' },
        { color: '#7f26d9', title: '分からない' },
        { color: '#268ed9', title: '英語の勉強' },
      ],
      chip_paragraph: '',
    };
  },
  methods: {
    displayCite(item) {
      console.log('スライド情報', this.paragraphAdd.slide);
      console.log(item);
      console.log(this.paragraphAdd.cite.cite_dict[item]);
      if (this.select_cite_index === item && this.isDetail === true) {
        this.isDetail = false;
      } else {
        this.isDetail = true;
        this.cite_detail = this.paragraphAdd.cite.cite_dict[item];
        this.cite_place = this.paragraphAdd.cite.cite_place[item];
        this.select_cite_index = item;
      }
    },
    jumpSlide() {
      this.$emit('toggleMethod', this.paragraphAdd.slide[this.slide_num].path, this.paragraphAdd.slide.index, false);
    },
    selectSlide(num) {
      this.slide_num = num;
    },
    // 選択された段落への移動
    jumpParagraph(index) {
      this.$emit('hilightParagraph', index);
    },
    jumpFigure(name) {
      this.$emit('jumpToFigure', name);
    },
  },
  watch: {
    isParagraph() {
      // このビューが閉じられた時にスタンプが押されていたら保存する
      if (this.isParagraph === false && this.chip_paragraph !== '') {
        const payload = {
          tag: 'report-paragraph',
          note: '',
          id: 0,
          stamp: this.chip_item[this.chip_paragraph].title,
          content: this.paragraphIndex,
        };
        const path = '/note_save';
        axios.post(path, payload)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
  },
};
</script>

<style>
th, td {
  border: solid 1px #696969;
}
</style>
