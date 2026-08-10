(function () {
  'use strict';

  var gate = document.getElementById('preview-password-gate');
  if (!gate) return;

  var slug = gate.getAttribute('data-preview-slug') || 'preview';
  var expected = (gate.getAttribute('data-preview-password') || '').trim();
  var storageKey = 'abm_preview_unlock_' + slug;
  var form = document.getElementById('preview-password-form');
  var input = document.getElementById('preview-password-input');
  var error = document.getElementById('preview-password-error');
  var gated = document.getElementById('preview-gated-content');

  function isUnlocked() {
    try {
      return sessionStorage.getItem(storageKey) === '1';
    } catch (e) {
      return false;
    }
  }

  function unlock() {
    try {
      sessionStorage.setItem(storageKey, '1');
    } catch (e) { /* ignore */ }

    document.body.classList.add('preview-unlocked');
    if (gated) {
      gated.removeAttribute('hidden');
    }
    gate.setAttribute('hidden', '');
    gate.style.display = 'none';
  }

  if (isUnlocked()) {
    unlock();
    return;
  }

  if (!form || !input) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var value = (input.value || '').trim();
    if (value.toLowerCase() === expected.toLowerCase()) {
      if (error) error.hidden = true;
      unlock();
      if (gated) {
        gated.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      return;
    }
    if (error) {
      error.hidden = false;
    }
    input.focus();
    input.select();
  });
})();
