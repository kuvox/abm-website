(function () {
  var input = document.getElementById("resources-search");
  var grid = document.getElementById("resources-grid");
  if (!input || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".related-card"));
  var groups = Array.prototype.slice.call(grid.querySelectorAll(".resources-category"));

  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function filterCards() {
    var query = normalize(input.value);
    cards.forEach(function (card) {
      var haystack = normalize(card.getAttribute("data-search"));
      var match = !query || haystack.indexOf(query) !== -1;
      card.hidden = !match;
      card.classList.toggle("is-filtered-out", !match);
    });

    groups.forEach(function (group) {
      var groupCards = group.querySelectorAll(".related-card");
      if (!groupCards.length) {
        group.hidden = !!query;
        return;
      }
      var visible = group.querySelectorAll(".related-card:not([hidden])").length > 0;
      group.hidden = !visible;
    });
  }

  input.addEventListener("input", filterCards);
  input.addEventListener("search", function () {
    if (!input.value) filterCards();
  });
})();
