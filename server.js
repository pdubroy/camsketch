/* eslint-env node */

var assert = require('assert');
var browserSync = require('browser-sync');
var dataurl = require('dataurl');
var fs = require('fs');
var join = require('path').join;
var textBody = require('body');

var IMAGE_DIR = join(
    process.env.HOME, 'Library/Application Support/org.cdglabs.camsketch');

function dirExists(path) {
  try {
    return fs.statSync(path).isDirectory();
  } catch (e) {
    return false;
  }
}

// Handlers for requests to `/saveImage`.
function saveImage(req, res) {
  textBody(req, function(err, data) {
    assert(!err);
    var info = dataurl.parse(data);
    assert.equal(info.mimetype, 'image/png');

    var filePath = join(IMAGE_DIR, 'image.png');
    fs.writeFile(filePath, info.data, {}, function(err) {
      if (err) {
        console.error(err);
      }
    });
    res.end('ok');
  });
}

// Ensure that the directory exists.
if (!dirExists(IMAGE_DIR)) {
  fs.mkdirSync(IMAGE_DIR);
}

// See http://www.browsersync.io/docs/options/ for more information.
browserSync({
  files: ['*'],
  open: false,
  server: {
    baseDir: 'static',
    middleware: function(req, res, next) {
      if (req.url === '/saveImage') {
        saveImage(req, res);
      } else {
        next();
      }
    }
  }
});
