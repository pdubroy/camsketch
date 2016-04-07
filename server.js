/* eslint-env node */

var assert = require('assert');
var dataurl = require('dataurl');
var fs = require('fs');
var textBody = require('body');
var path = require('path');

// Handlers for requests to `/saveImage`.
function saveImage(req, res) {
  textBody(req, function(err, data) {
    assert(!err);
    var info = dataurl.parse(data);
    assert.equal(info.mimetype, 'image/png');

    var filename = path.join(__dirname, 'image.png');
    fs.writeFile(filename, info.data, {}, function(err) {
      if (!err) {
        console.error(err);
      }
    });
    res.end('ok');
  });
}

// See http://www.browsersync.io/docs/options/ for more information.
require('browser-sync')({
  files: ['*'],
  server: {
    baseDir: 'static',
    middleware: function(req, res, next) {
      if (req.url === '/saveImage') {
        saveImage(req, res);
      } else {
        next();
      }
    }
  },
  startPath: '/index.html'
});
