<template>
  <v-container>
    <h2 align='center'>Welcome!</h2>
    <hr>
    <v-alert
      dense
      outlined
      type="error"
      v-if="isAlert"
    >
      <strong>Paper not selected.</strong> Please select a paper.
    </v-alert>
    <v-row align="center">
      <v-col cols="4">
        <v-subheader>
          Select paper.
        </v-subheader>
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="select"
          @change = 'selectFile'
          :hint="`${select}`"
          :items="items"
          item-text="state"
          item-value="abbr"
          label="Select"
          persistent-hint
          return-object
          single-line
        ></v-select>
      </v-col>
      <v-col cols='4' align='right'>
        <v-btn depressed color="primary" @click="decideFile">select</v-btn>
      </v-col>
    </v-row>
    <br>
    <div>
      <object :data="abstractPath" type="text/plain" width="100%" height="100%">
        これはアブストラクトです
      </object>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-4" ref="col">
           <iframe :src="filePath" frameborder="0" allow="autoplay; fullscreen" width="100%"
            :height = "paper_height" allowfullscreen title="this is slide"></iframe>
        </div>
        <div class="col-4">
          <v-img fluid :src="wordcloudPath" v-if="isDisplayWordcloud"></v-img>
        </div>
        <div class="col-4">
          <iframe :src="videoLink" width="100%" :height = "video_height"
            id = 'intro-video' title="movie" allowfullscreen>
          </iframe>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StartComponent',
  data() {
    return {
      select: '',
      items: [],
      filePath: '',
      isDisplayWordcloud: false,
      abstract: '',
      isAlert: false,
    };
  },
  methods: {
    getFileNames() {
      const path = '/start';
      axios.get(path)
        .then((res) => {
          console.log(res);
          this.items = res.data.file_name;
          this.prev_link = res.data.prev_link;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    selectFile() {
      console.log(this.select);
      this.filePath = `/static/static/${this.select}/${this.select}.pdf`;
      this.wordcloudPath = `/static/static/${this.select}/wordcloud.jpg`;
      this.videoLink = this.prev_link[this.select];
      this.abstractPath = `/static/static/${this.select}/abstract.txt`;
      this.isDisplayWordcloud = true;
      console.log(this.filePath);
      const dom = this.$refs.col.getBoundingClientRect();
      this.paper_width = dom.width;
      this.paper_height = dom.width * 1.44;
      this.video_height = dom.width * 0.53;
    },
    sendSelectFile(payload) {
      const path = '/start';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-diable-next-line
          console.error(error);
        });
    },
    decideFile() {
      if (this.select === '') {
        this.isAlert = true;
      } else {
        this.isAlert = false;
        const payload = {
          filename: this.select,
        };
        this.sendSelectFile(payload);
        window.location.href = '/report';
      }
    },
  },
  created() {
    this.getFileNames();
  },
};
</script>
