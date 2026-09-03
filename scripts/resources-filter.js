(function () {
  var input = document.getElementById("resources-search");
  var grid = document.getElementById("resources-grid");
  var bar = document.getElementById("resources-filterbar");
  var empty = document.getElementById("resources-empty");
  if (!grid || !bar) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".resource-card"));
  var buttons = Array.prototype.slice.call(bar.querySelectorAll(".filter-btn"));
  var activeCat = "";

  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function apply() {
    var query = input ? normalize(input.value) : "";
    var shown = 0;
    cards.forEach(function (card) {
      var cats = " " + (card.getAttribute("data-cats") || "") + " ";
      var catMatch = !activeCat || cats.indexOf(" " + activeCat + " ") !== -1;
      var haystack = normalize(card.getAttribute("data-search") + " " + card.textContent);
      var textMatch = !query || haystack.indexOf(query) !== -1;
      var match = catMatch && textMatch;
      card.hidden = !match;
      if (match) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      activeCat = btn.getAttribute("data-cat") || "";
      buttons.forEach(function (b) { b.classList.toggle("is-active", b === btn); });
      apply();
    });
  });

  if (input) {
    input.addEventListener("input", apply);
    input.addEventListener("search", apply);
  }

  // Deep links like /resources#data-feeds pre-select a subject.
  var hash = (location.hash || "").replace("#", "");
  buttons.some(function (btn) {
    if (btn.getAttribute("data-cat") === hash && hash) { btn.click(); return true; }
    return false;
  });
})();
