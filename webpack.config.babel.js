import path from 'path'
import 'webpack'


export default {
    entry: './web_client/app.js',
    output: {
        path: `${__dirname}/eben/static`,
        filename: 'app.js'
    },
    resolve: {
        extensions: ['*', '.js', '.jsx', '.scss'],
        modules: [
            'node_modules'
        ]
    },
    devtool: "#sourcemap",
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    "style-loader", // creates style nodes from JS strings
                    "css-loader", // translates CSS into CommonJS
                    "sass-loader" // compiles Sass to CSS
                ]
            },
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                include: [
                    path.resolve(__dirname, "web_client")
                ],
                query: {
                    plugins: ['transform-runtime'],
                    presets: ['es2015', 'stage-0', 'react']
                }
            }
        ]
    }
}
