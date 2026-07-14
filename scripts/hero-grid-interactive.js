(function () {
  var CELL_SIZE = 48;
  var HIGHLIGHT_OPACITY = 0.26;
  var CORE_OPACITY = 0.12;
  var DECAY_RATE = 0.92;
  var GRID_LINE_ALPHA = 0.04;
  var NEIGHBOR_BOOST = 0.55;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (window.matchMedia("(pointer: coarse)").matches) return;

  var sections = document.querySelectorAll(".grid-trail");
  if (!sections.length) return;

  function initGridTrail(section) {
    var canvas = section.querySelector(".grid-trail-canvas");
    if (!canvas) return;

    var ctx = canvas.getContext("2d");
    var cols = 0;
    var rows = 0;
    var opacities = [];
    var animating = false;
    var dpr = window.devicePixelRatio || 1;

    function buildGrid() {
      var rect = section.getBoundingClientRect();
      dpr = window.devicePixelRatio || 1;
      canvas.width = Math.floor(rect.width * dpr);
      canvas.height = Math.floor(rect.height * dpr);
      canvas.style.width = rect.width + "px";
      canvas.style.height = rect.height + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      cols = Math.ceil(rect.width / CELL_SIZE);
      rows = Math.ceil(rect.height / CELL_SIZE);
      opacities = new Float32Array(cols * rows);
    }

    function cellIndex(col, row) {
      if (col < 0 || row < 0 || col >= cols || row >= rows) return -1;
      return row * cols + col;
    }

    function lightCell(col, row, amount) {
      var idx = cellIndex(col, row);
      if (idx === -1) return;
      opacities[idx] = Math.min(1, opacities[idx] + amount);
    }

    function lightAt(x, y) {
      var col = Math.floor(x / CELL_SIZE);
      var row = Math.floor(y / CELL_SIZE);

      lightCell(col, row, HIGHLIGHT_OPACITY + CORE_OPACITY);
      lightCell(col - 1, row, HIGHLIGHT_OPACITY * NEIGHBOR_BOOST);
      lightCell(col + 1, row, HIGHLIGHT_OPACITY * NEIGHBOR_BOOST);
      lightCell(col, row - 1, HIGHLIGHT_OPACITY * NEIGHBOR_BOOST);
      lightCell(col, row + 1, HIGHLIGHT_OPACITY * NEIGHBOR_BOOST);
    }

    function draw() {
      var w = canvas.width / dpr;
      var h = canvas.height / dpr;
      ctx.clearRect(0, 0, w, h);

      ctx.strokeStyle = "rgba(255, 255, 255, " + GRID_LINE_ALPHA + ")";
      ctx.lineWidth = 1;
      for (var c = 0; c <= cols; c++) {
        var x = c * CELL_SIZE + 0.5;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }
      for (var r = 0; r <= rows; r++) {
        var y = r * CELL_SIZE + 0.5;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      for (var i = 0; i < opacities.length; i++) {
        if (opacities[i] <= 0.01) continue;
        var col = i % cols;
        var row = Math.floor(i / cols);
        var alpha = opacities[i];
        ctx.fillStyle = "rgba(231, 77, 59, " + (alpha * 0.85) + ")";
        ctx.fillRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        if (alpha > 0.5) {
          ctx.fillStyle = "rgba(255, 255, 255, " + ((alpha - 0.5) * CORE_OPACITY) + ")";
          ctx.fillRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
      }
    }

    function tick() {
      var anyLeft = false;
      for (var i = 0; i < opacities.length; i++) {
        if (opacities[i] > 0.01) {
          opacities[i] *= DECAY_RATE;
          anyLeft = true;
        } else {
          opacities[i] = 0;
        }
      }

      draw();

      if (anyLeft) {
        requestAnimationFrame(tick);
      } else {
        animating = false;
      }
    }

    function startAnimation() {
      if (animating) return;
      animating = true;
      requestAnimationFrame(tick);
    }

    section.addEventListener("mousemove", function (e) {
      var rect = section.getBoundingClientRect();
      lightAt(e.clientX - rect.left, e.clientY - rect.top);
      startAnimation();
    });

    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        buildGrid();
        draw();
      }, 150);
    });

    buildGrid();
    draw();
  }

  sections.forEach(initGridTrail);
})();
