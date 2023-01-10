<template>
  <v-container>
    <v-row>
      <v-col cols="3"></v-col>
      <v-col cols="4">
        <h2 align='center'>Add New File!</h2>
      </v-col>
      <v-col cols="2">
        <v-btn
          class="ma-2"
          outlined
          color="indigo"
          @click="cancel"
        >
          {{backDisplay}}
        </v-btn>
      </v-col>
      <v-col cols="3"></v-col>
    </v-row>
    <hr>
    <v-row>
      <v-alert
        dense
        outlined
        type="error"
        v-if="isAlert"
      >
        フォームが正しく入力されているか確認してください
      </v-alert>
      <v-alert
        dense
        outlined
        type="info"
        v-if="isProcess"
      >
        前処理を実行中です。このままでお待ちください。
      </v-alert>
      <v-alert
        dense
        outlined
        type="success"
        v-if="isComplete"
      >
        前処理が完了しました
      </v-alert>
      <v-col cols = "8">
        <p>論文の表示名を入力してください<p>
        <br>
        <v-text-field
          label="Outlined"
          outlined
          dense
          v-model="name"
        ></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-btn
          class="ma-2"
          outlined
          color="indigo"
          @click="selectFile"
        >
          PreProcess Start
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="3">
        <v-file-input
          accept=".pdf"
          label="report input"
          v-model="pdf"
        ></v-file-input>
      </v-col>
      <v-col cols="3">
        <v-file-input
          accept="video/*"
          label="video input"
          v-model="video"
        ></v-file-input>
      </v-col>
      <v-col cols="3">
        <v-file-input
          accept=".json"
          label="Audio Transcript Input"
          v-model="json"
        ></v-file-input>
      </v-col>
      <v-col cols="3">
        <v-file-input
          accept="video/*"
          label="preview video"
          v-model="preview"
        ></v-file-input>
      </v-col>
    </v-row>
    <p>please paste bibtex.</p>
    <v-textarea
      outlined
      name="input-7-4"
      label="Outlined textarea"
      v-model="bib"
    ></v-textarea>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'importFile',
  data() {
    return {
      name: '',
      pdf: '',
      video: '',
      json: '',
      preview: '',
      isAlert: false,
      isProcess: false,
      isComplete: false,
      backDisplay: 'cancel',
    };
  },
  methods: {
    cancel() {
      window.location.href = '/';
    },
    selectFile() {
      console.log(this.video);
      if (this.video === '' || this.pdf === '' || this.json === '' || this.name === ''
        || this.bib === '' || this.preview === '') {
        console.log('error');
        this.isAlert = true;
      } else {
        const payload = {
          name: this.name,
          pdf: this.pdf,
          video: this.video,
          json: this.jsn,
        };
        this.isProcess = true;
        this.isAlert = false;
        this.isComplete = false;

        console.log(this.video[0], payload);
        const params = new FormData();
        params.append('userpdf', this.pdf);
        params.append('uservideo', this.video);
        params.append('userjson', this.json);
        params.append('userpreview', this.preview);
        params.append('name', this.name);
        params.append('bibtex', this.bib);
        const path = '/uploadFile';

        // 情報の削除
        this.pdf = '';
        this.video = '';
        this.json = '';
        this.name = '';
        this.bib = '';
        this.preview = '';
        axios.post(path, params)
          .then((res) => {
            console.log(res.data);
            this.isProcess = false;
            this.isComplete = true;
            this.backDisplay = 'home';
          })
          .catch((error) => {
            // eslint-diable-next-line
            this.isAlert = true;
            console.error(error);
          });
      }
    },
  },
};
</script>
