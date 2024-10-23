'use strict'
// Template version: 1.1.3
// see http://vuejs-templates.github.io/webpack for documentation.
const path = require('path')

module.exports = {
    build: {
        env: require('./prod.env'),
        index: path.resolve(__dirname, '../dist/index.html'),
        assetsRoot: path.resolve(__dirname, '../dist'),
        assetsSubDirectory: 'static',
        assetsPublicPath: './',
        productionSourceMap: false,
        // Gzip off by default as many popular static hosts such as
        // Surge or Netlify already gzip all static assets for you.
        // Before setting to `true`, make sure to:
        // npm install --save-dev compression-webpack-plugin
        productionGzip: false,
        productionGzipExtensions: ['js', 'css'],
        // Run the build command with an extra argument to
        // View the bundle analyzer report after build finishes:
        // `npm run build --report`
        // Set to `true` or `false` to always turn it on or off
        bundleAnalyzerReport: process.env.npm_config_report
    },
    dev: {
        env: require('./dev.env'),
        port: process.env.PORT || 9000,
        autoOpenBrowser: true,
        assetsSubDirectory: 'static',
        assetsPublicPath: './',
        proxyTable: {
            // 设置代理规则
            '/api': {
              // 目标服务器的主机名和端口号
              target: 'http://localhost:5000/',
              // 指定是否要将请求头中的 host 替换为 target 配置项中的域名
              changeOrigin: true,
              // 指定是否开启连接代理
              secure: false,
              // 设置代理请求的路径
              pathRewrite: {
                '^/api': '' // 重写路径，移除请求中的 '/api' 前缀
              }
            }
        },
        // CSS Sourcemaps off by default because relative paths are "buggy"
        // with this option, according to the CSS-Loader README
        // (https://github.com/webpack/css-loader#sourcemaps)
        // In our experience, they generally work as expected,
        // just be aware of this issue when enabling this option.
        cssSourceMap: false
    }
}