(function () {
  /* Static grid only — interactive mouse/scroll glow is archived in
     docs/grid-trail-interactive.md. Restore from that file if needed. */
  var CELL_SIZE = 48;
  var GRID_LINE_ALPHA = 0.04;

  var sections = document.querySelectorAll(".grid-trail");
  if (!sections.length) return;

  function initGridTrail(section) {
    var canvas = section.querySelector(".grid-trail-canvas");
    if (!canvas) return;

    var ctx = canvas.getContext("2d");
    var cols = 0;
    var rows = 0;
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
    }

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
