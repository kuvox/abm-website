// Click-to-load YouTube embed. Shows a poster until clicked, so no YouTube
// code loads with the page. Without JS the link opens the video on YouTube.
(function () {
  var warmed = false;
  function warm() {
    if (warmed) return;
    warmed = true;
    ['https://www.youtube-nocookie.com', 'https://i.ytimg.com', 'https://www.google.com'].forEach(function (href) {
      var l = document.createElement('link');
      l.rel = 'preconnect';
      l.href = href;
      document.head.appendChild(l);
    });
  }
  document.addEventListener('pointerover', function (e) {
    if (e.target.closest && e.target.closest('.yt-facade')) warm();
  });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.yt-facade');
    if (!a) return;
    e.preventDefault();
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + a.dataset.ytId + '?autoplay=1&rel=0&playsinline=1';
    f.title = a.dataset.ytTitle || 'YouTube video';
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.allowFullscreen = true;
    f.className = a.className.replace('yt-facade', 'yt-iframe');
    a.replaceWith(f);
  });
})();
