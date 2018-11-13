// vue.config.js is an optional config file that will be automatically loaded by
// @vue/cli-service if it's present in your project root (next to package.json).
module.exports = {
  configureWebpack: {
    watchOptions: {
      ignored: /node_modules/,
      aggregateTimeout: 300,
      poll: 1000,
    },
  }
}
