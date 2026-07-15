(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('navlinks');
  if (!toggle || !nav) return;

  var OPEN_ICON = '\u2715'; // ✕
  var CLOSED_ICON = '\u2630'; // ☰
  var mobileQuery = window.matchMedia('(max-width: 900px)');
  var megaItems = nav.querySelectorAll('.has-megamenu');

  function closeMegaMenus() {
    megaItems.forEach(function (li) {
      li.classList.remove('megamenu-open');
    });
  }

  function setOpen(isOpen) {
    nav.classList.toggle('open', isOpen);
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.textContent = isOpen ? OPEN_ICON : CLOSED_ICON;
    document.body.classList.toggle('nav-open', isOpen);
    if (!isOpen) closeMegaMenus();
  }

  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    setOpen(!nav.classList.contains('open'));
  });

  // On mobile, tapping a megamenu label (Services/Learn/About) toggles its
  // panel open instead of navigating — the panel's own links still navigate
  // normally, and each covers the same destination as the parent label.
  megaItems.forEach(function (li) {
    var link = li.querySelector(':scope > a');
    if (!link) return;
    link.addEventListener('click', function (e) {
      if (!mobileQuery.matches) return;
      e.preventDefault();
      var isOpen = li.classList.contains('megamenu-open');
      closeMegaMenus();
      li.classList.toggle('megamenu-open', !isOpen);
    });
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (e.defaultPrevented) return;
      setOpen(false);
    });
  });

  document.addEventListener('click', function (e) {
    if (!nav.classList.contains('open')) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      setOpen(false);
      toggle.focus();
    }
  });
})();
