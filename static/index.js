/* eslint-env browser */
/* global DocumentTouch */

(function() {
  var canvas = document.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var canvasChanged = true;

  // Helpers
  // -------

  function isTouchDevice() {
    return 'ontouchstart' in window ||
           !!(window.DocumentTouch && document instanceof DocumentTouch);
  }

  function handleResize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function handleTouchStart(e) {
    ctx.beginPath();
    ctx.lineCap = 'round';
    ctx.lineWidth = 4;
    ctx.moveTo(e.clientX, e.clientY);
  }

  function handleTouchMove(e) {
    ctx.lineTo(e.clientX, e.clientY);
    ctx.stroke();
    canvasChanged = true;
  }

  function handleTouchEnd(e) {
    ctx.closePath();
    maybeSaveImage();
  }

  function maybeSaveImage() {
    if (canvasChanged) {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        console.log(xhr.status);
      };
      xhr.open('POST', 'saveImage', true);
      xhr.send(canvas.toDataURL());
      canvasChanged = false;
    }
  }

  // Main
  // ----

  window.addEventListener('resize', handleResize);
  handleResize();

  if (isTouchDevice()) {
    canvas.ontouchstart = function(e) {
      if (e.touches.length === 1) {
        handleTouchStart(e.touches[0]);
      }
    };
    canvas.ontouchmove = function(e) {
      if (e.touches.length === 1) {
        handleTouchMove(e.touches[0]);
        e.preventDefault();
      }
    };
    canvas.ontouchend = function(e) {
      handleTouchEnd(e.touches[0]);
    };
  } else {
    var drawing = false;
    canvas.onmousedown = function(e) {
      drawing = true;
      handleTouchStart(e);
    };
    canvas.onmousemove = function(e) {
      if (drawing) {
        handleTouchMove(e);
      }
    };
    canvas.onmouseup = function(e) {
      drawing = false;
      handleTouchEnd(e);
    };
  }

  maybeSaveImage();
  window.setInterval(maybeSaveImage, 1000);
})();
