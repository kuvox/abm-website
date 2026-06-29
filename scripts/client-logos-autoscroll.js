/**
 * Slow auto-scroll for client logo collages (.client-collage-card--home).
 * Used on index.html and about.html.
 *
 * REVERT: remove script tags from those pages and delete this file.
 */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var cards = document.querySelectorAll('.client-collage-card--home');
  if (!cards.length) return;

  /** ~13px/s — about half the prior ~27px/s rate */
  var SPEED_PX_PER_SEC = 13;

  function whenImagesReady(card, cb) {
    var imgs = card.querySelectorAll('img');
    if (!imgs.length) {
      cb();
      return;
    }
    var pending = imgs.length;
    var finished = false;
    function finish() {
      if (finished) return;
      finished = true;
      cb();
    }
    function done() {
      pending -= 1;
      if (pending <= 0) finish();
    }
    imgs.forEach(function (img) {
      if (img.complete) done();
      else {
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
      }
    });
    setTimeout(finish, 2500);
  }

  function initCard(card) {
    function scrollable() {
      return card.scrollHeight - card.clientHeight > 1;
    }

    function start() {
      if (!scrollable()) return false;

      card.classList.add('client-collage-card--autoscroll');

      var paused = false;
      var lastTime = performance.now();
      var rafId = 0;

      function tick(now) {
        if (!paused && scrollable()) {
          var dt = Math.min((now - lastTime) / 1000, 0.05);
          lastTime = now;
          var max = card.scrollHeight - card.clientHeight;
          card.scrollTop = Math.min(card.scrollTop + SPEED_PX_PER_SEC * dt, max);
          if (card.scrollTop >= max - 1) {
            card.scrollTop = 0;
          }
        } else {
          lastTime = now;
        }
        rafId = requestAnimationFrame(tick);
      }

      function pause() {
        paused = true;
      }

      function resume() {
        paused = false;
        lastTime = performance.now();
      }

      card.addEventListener('mouseenter', pause);
      card.addEventListener('mouseleave', resume);
      card.addEventListener('focusin', pause);
      card.addEventListener('focusout', function (e) {
        if (!card.contains(e.relatedTarget)) resume();
      });
      card.addEventListener('touchstart', pause, { passive: true });
      card.addEventListener('touchend', resume, { passive: true });

      rafId = requestAnimationFrame(tick);
      return true;
    }

    function tryStart(attempt) {
      if (start()) return;
      if (attempt < 8) {
        setTimeout(function () {
          tryStart(attempt + 1);
        }, 250);
      }
    }

    whenImagesReady(card, function () {
      tryStart(0);
    });
  }

  function boot() {
    cards.forEach(initCard);
  }

  if (document.readyState === 'complete') boot();
  else window.addEventListener('load', boot);
})();
