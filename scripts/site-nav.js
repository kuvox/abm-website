(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('navlinks');
  if (!toggle || !nav) return;

  var OPEN_ICON = '\u2715'; // ✕
  var CLOSED_ICON = '\u2630'; // ☰

  function setOpen(isOpen) {
    nav.classList.toggle('open', isOpen);
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.textContent = isOpen ? OPEN_ICON : CLOSED_ICON;
    document.body.classList.toggle('nav-open', isOpen);
  }

  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    setOpen(!nav.classList.contains('open'));
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
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
