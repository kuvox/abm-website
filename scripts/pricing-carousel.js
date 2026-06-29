(function () {
  var carousel = document.getElementById('pricing-carousel');
  if (!carousel) return;

  var cards = carousel.querySelectorAll('.pricing-card');
  var dots = document.querySelectorAll('.pricing-carousel-dot');
  if (!cards.length || !dots.length) return;

  function setActiveDot(index) {
    dots.forEach(function (dot, i) {
      var active = i === index;
      dot.classList.toggle('is-active', active);
      dot.setAttribute('aria-selected', active ? 'true' : 'false');
    });
  }

  function scrollToCard(index) {
    var card = cards[index];
    if (!card) return;
    carousel.scrollTo({ left: card.offsetLeft - carousel.offsetLeft, behavior: 'smooth' });
    setActiveDot(index);
  }

  function indexFromScroll() {
    var scrollLeft = carousel.scrollLeft;
    var closest = 0;
    var closestDist = Infinity;
    cards.forEach(function (card, i) {
      var dist = Math.abs(card.offsetLeft - carousel.offsetLeft - scrollLeft);
      if (dist < closestDist) {
        closestDist = dist;
        closest = i;
      }
    });
    return closest;
  }

  dots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      scrollToCard(Number(dot.getAttribute('data-index')));
    });
  });

  carousel.addEventListener('scroll', function () {
    window.clearTimeout(carousel._pricingScrollTimer);
    carousel._pricingScrollTimer = window.setTimeout(function () {
      setActiveDot(indexFromScroll());
    }, 80);
  }, { passive: true });
})();
