<template>
  <div>
    <div class="row">
      <div class="col-4">
      </div>
      <div class="col-8">
        <v-chip-group
          v-model="stamp"
          column
          multiple
        >
          <v-chip v-for="tip in tip_item" :key="tip" filter outlined :color="tip.color">
            {{tip.title}}
          </v-chip>
        </v-chip-group>
      </div>
    </div>
    <v-tabs v-model="tab" vertical>
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
      <v-tab href="#all">All
        <v-icon>mdi-border-none-variant</v-icon>
      </v-tab>
      <!-- 論文を選んだ時 -->
      <v-tab-item value='report' vertical>
        <div class="row">
          <div class="col-9">
            <v-tabs v-model="report" vertical>
              <v-tab href="#all">All</v-tab>
              <v-tab href="#page">Page<v-icon></v-icon></v-tab>
              <v-tab href="#section">Section</v-tab>
              <v-tab href="#paragraph">Paragraph&sentence</v-tab>
              <v-tab href="#figure">Figure</v-tab>
              <!-- 論文のページを選択 -->
              <v-tab-item value = 'page'>
                <page-content
                  :report="this.report"
                  :login_name="this.login_name"
                  :report_max_page="this.report_max_page"
                  :report_basic_path = "this.report_basic_path"
                  :stamp_list="this.stamp_list"
                  ref="pageContent"
                ></page-content>
              </v-tab-item>
              <!-- 論文のセクションを選択 -->
              <v-tab-item value = 'section'>
                <section-content
                  :report = "this.report"
                  :login_name="this.login_name"
                  :stamp_list="this.stamp_list"
                  ref="sectionContent"
                ></section-content>
              </v-tab-item>
              <!-- 論文の段落を選択 -->
              <v-tab-item value="paragraph">
                <paragraph-content
                  :report="report"
                  :login_name="this.login_name"
                  :stamp_list="this.stamp_list"
                  ref="paragraphContent"
                ></paragraph-content>
              </v-tab-item>
              <!-- 図表を選択した場合 -->
              <v-tab-item value = 'figure'>
                <figure-content
                  :report="this.report"
                  :login_name="this.login_name"
                  :stamp_list="this.stamp_list"
                  ref="figureContent"
                ></figure-content>
              </v-tab-item>
              <!-- 論文全体に対するメモ -->
              <v-tab-item value = 'all'>
                <report-all-content
                  :report="this.report"
                  :login_name="this.login_name"
                  :fileName="this.fileName"
                  :stamp_list="this.stamp_list"
                  ref="reportAllContent"
                ></report-all-content>
              </v-tab-item>
            </v-tabs>
          </div>
          <div class="col-3">
            <iframe :src="`/static/static/${this.fileName}/${this.fileName}.pdf`"
            frameborder="0" allow="autoplay; fullscreen" width="100%"
            :height = "height" allowfullscreen title="this is slide"></iframe>
          </div>
        </div>
      </v-tab-item>
      <!-- 動画を選んだ時 -->
      <v-tab-item value='video'>
        <video-content
          :tab = "this.tab"
          :login_name="this.login_name"
          :stamp_list="this.stamp_list"
          ref="videoContent"
        ></video-content>
      </v-tab-item>
      <!-- スライドを選んだ時 -->
      <v-tab-item value='slide'>
        <slide-content
          :tab = "this.tab"
          :login_name="this.login_name"
          :stamp_list="this.stamp_list"
          ref="slideContent"
        ></slide-content>
      </v-tab-item>
      <!-- wordを選んだ時 -->
      <v-tab-item value='all'>
        <all-content
          :tab="this.tab"
          :login_name="this.login_name"
          :stamp_list="this.stamp_list"
          ref="allContent"
        ></all-content>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
import pageContent from './noteComponents/page.vue';
import figureContent from './noteComponents/figure.vue';
import sectionContent from './noteComponents/section.vue';
import paragraphContent from './noteComponents/paragraph.vue';
import videoContent from './noteComponents/video.vue';
import slideContent from './noteComponents/slide.vue';
import allContent from './noteComponents/all.vue';
import reportAllContent from './noteComponents/reportAll.vue';

export default {
  name: 'NoteDisplay',
  props: ['videoLink', 'slide_page_num', 'selectSlide', 'slideItems', 'fileName',
    'select_report_path', 'report_max_page', 'report_basic_path', 'login_name'],
  components: {
    pageContent,
    figureContent,
    sectionContent,
    paragraphContent,
    videoContent,
    slideContent,
    allContent,
    reportAllContent,
  },
  data() {
    return {
      stamp: [0, 1, 2, 3],
      tip_item: [
        { color: '#d92626', title: '論文の要' },
        { color: '#FFB55B', title: '何となく大事' },
        { color: '#26d98e', title: '後で読む' },
        { color: '#7f26d9', title: '分からない' },
      ],
      report: 'all',
      tab: 'report',
      filePath: '',
      height: '600px',
      stamp_list: ['何となく大事', '論文の要', '後で読む', '分からない'],
    };
  },
  methods: {
    reload() {
      console.log('変化を子コンポーネント側でも検知');
      console.log(this.stamp);
      if (this.tab === 'video') this.$refs.videoContent.importNoteInfo();
      if (this.tab === 'slide') this.$refs.slideContent.importNoteInfo();
      if (this.tab === 'all') this.$refs.allContent.importNoteInfo();
      if (this.tab === 'report') {
        if (this.report === 'page') this.$refs.pageContent.importNoteInfo();
        if (this.report === 'section') this.$refs.sectionContent.importNoteInfo();
        if (this.report === 'figure') this.$refs.figureContent.importNoteInfo();
        if (this.report === 'paragraph') this.$refs.paragraphContent.importNoteInfo();
        if (this.report === 'all') this.$refs.reportAllContent.importNoteInfo();
      }
      // this.height = `${document.getElementById('width').clientWidth * 2.0}pt`;
    },
  },
  watch: {
    reportTitle() {
      this.filePath = `/static/static/${this.reportTitle}/${this.reportTitle}.pdf`;
      console.log(this.reportTitle);
    },
    stamp() {
      this.stamp_list = this.stamp.map((key) => this.tip_item[key].title);
      this.reload();
    },
  },
  created() {
    this.height = `${document.getElementById('width').clientWidth * 2.0}px`;
  },
};
</script>

<style>
v-button.objective {
  border: solid 1px #A1A3A6;
}
</style>
