const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

const path = require('path');

module.exports = {
	publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',

	assetsDir: '../app/static',

	transpileDependencies: true,

	configureWebpack: {
		// Webpack configuration option
	},

	productionSourceMap: false,

	outputDir: path.resolve(__dirname, '../app/static/dist'),
};
