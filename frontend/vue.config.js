const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    // publicPath: "http://0.0.0.0:8080/",
    // publicPath: "http://localhost:8000/static/",
    publicPath: "http://vbstech.ir/static/",
    // baseUrl: "http://localhost:8000/",
    // publicPath: "http://vbstech.ir/",
    outputDir: './dist/',
    assetsDir: './frontend/',

    chainWebpack: config => {

        config.optimization
            .splitChunks(false);

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../frontend/webpack-stats.json'}]);

        config.resolve.alias
            .set('__STATIC__', 'static');

        config.devServer
            // .public('http://0.0.0.0:8080')
            .public('http://vbstech.ir')
            // .host('0.0.0.0')
            .host('localhost')
            .port(8000)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
            }
        };