const { defineConfig } = require('@vue/cli-service');

module.exports = {
  transpileDependencies: [
    'vuetify',
  ],
  assetsDir: 'static',
  devServer: {
    port: 8081,
    host: '127.0.0.1'
  }
};
