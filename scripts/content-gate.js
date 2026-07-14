(function () {
  'use strict';

  var STORAGE_KEY = 'abm_content_unlocked';
  var HUBSPOT_PORTAL_ID = '14501596';
  var HUBSPOT_FORM_ID = '59ed14ff-4a47-42d9-b782-e7f93f564945';

  var DISPOSABLE_DOMAINS = [
    'mailinator.com', 'guerrillamail.com', 'tempmail.com', 'throwaway.email',
    'yopmail.com', 'sharklasers.com', 'trashmail.com', '10minutemail.com',
    'fakeinbox.com', 'getnada.com', 'maildrop.cc', 'dispostable.com'
  ];

  var unlocked = false;

  function isUnlocked() {
    try {
      return localStorage.getItem(STORAGE_KEY) === '1';
    } catch (e) {
      return false;
    }
  }

  function moveSuccessToBottom() {
    var gate = document.getElementById('content-gate');
    var slot = document.getElementById('content-gate-success');
    if (!gate || !slot) return;

    var wrap = gate.querySelector('.content-gate-form-wrap');
    if (!wrap) return;

    slot.appendChild(wrap);
    slot.hidden = false;
    slot.removeAttribute('hidden');
  }

  function unlock(options) {
    if (unlocked && !(options && options.force)) return;
    unlocked = true;

    try {
      localStorage.setItem(STORAGE_KEY, '1');
    } catch (e) { /* ignore */ }

    document.body.classList.add('content-unlocked');

    var gated = document.getElementById('gated-content');
    var gate = document.getElementById('content-gate');
    var preview = document.querySelector('.content-gate-preview');

    if (options && options.moveSuccess) {
      moveSuccessToBottom();
    }

    if (gated) gated.removeAttribute('hidden');
    if (gate) {
      gate.setAttribute('hidden', '');
      gate.style.display = 'none';
    }
    if (preview) preview.classList.remove('content-gate-preview--faded');

    if (options && options.scroll !== false && gated) {
      gated.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function isValidEmail(email) {
    if (!email || typeof email !== 'string') return false;
    var trimmed = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed)) return false;
    var domain = trimmed.split('@')[1];
    return DISPOSABLE_DOMAINS.indexOf(domain) === -1;
  }

  function looksLikeSuccess(root) {
    if (!root) return false;
    if (root.querySelector('.submitted-message, .hs-form-success, [data-hs-form-success]')) {
      return true;
    }
    var text = (root.textContent || '').replace(/\s+/g, ' ').trim();
    return /^success[!]?/i.test(text) || /\bSuccess!\b/.test(text);
  }

  function mountFallbackForm(container) {
    container.innerHTML =
      '<form class="content-gate-fallback" id="content-gate-fallback" novalidate>' +
      '  <label for="content-gate-email">Work email</label>' +
      '  <input type="email" id="content-gate-email" name="email" autocomplete="email" required placeholder="you@company.com">' +
      '  <p class="content-gate-error" id="content-gate-error" hidden>Enter a valid work email address.</p>' +
      '  <button type="submit" class="btn btn-primary">Unlock the guide</button>' +
      '</form>';

    var form = document.getElementById('content-gate-fallback');
    var error = document.getElementById('content-gate-error');
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var email = document.getElementById('content-gate-email').value;
      if (!isValidEmail(email)) {
        error.hidden = false;
        return;
      }
      error.hidden = true;
      unlock({ scroll: true });
    });
  }

  function mountHubSpotForm(container) {
    if (!HUBSPOT_PORTAL_ID || !HUBSPOT_FORM_ID) {
      mountFallbackForm(container);
      return;
    }

    var script = document.createElement('script');
    script.src = 'https://js.hsforms.net/forms/embed/' + HUBSPOT_PORTAL_ID + '.js';
    script.defer = true;
    script.onload = function () {
      container.innerHTML =
        '<div class="hs-form-frame" data-region="na1" data-form-id="' +
        HUBSPOT_FORM_ID +
        '" data-portal-id="' +
        HUBSPOT_PORTAL_ID +
        '"></div>';
      watchGateForSuccess();
    };
    script.onerror = function () {
      mountFallbackForm(container);
    };
    document.head.appendChild(script);
  }

  function watchGateForSuccess() {
    var gate = document.getElementById('content-gate');
    if (!gate || typeof MutationObserver === 'undefined') return;

    var observer = new MutationObserver(function () {
      if (looksLikeSuccess(gate)) {
        observer.disconnect();
        unlock({ moveSuccess: true, scroll: true });
      }
    });
    observer.observe(gate, {
      childList: true,
      subtree: true,
      characterData: true,
    });
  }

  function listenForHubSpotSubmit() {
    window.addEventListener('message', function (event) {
      var d = event && event.data;
      if (!d) return;

      // Object-shaped HubSpot callbacks
      if (typeof d === 'object') {
        if (d.type === 'hsFormCallback' && d.eventName === 'onFormSubmitted') {
          unlock({ moveSuccess: true, scroll: true });
          return;
        }
        if (d.type === 'hsFormCallback' && d.id === 'onFormSubmitted') {
          unlock({ moveSuccess: true, scroll: true });
          return;
        }
        if (d.eventName === 'onFormSubmitted' || d.eventName === 'onFormSubmit') {
          unlock({ moveSuccess: true, scroll: true });
          return;
        }
      }

      // Occasional string payloads from embeds
      if (typeof d === 'string' && /onFormSubmitted|formSubmitted/i.test(d)) {
        unlock({ moveSuccess: true, scroll: true });
      }
    });

    // Global HubSpot event bus (classic + some new embeds)
    window.addEventListener('hs-form-event', function () {
      unlock({ moveSuccess: true, scroll: true });
    });
  }

  function init() {
    var gate = document.getElementById('content-gate');
    if (!gate) return;

    listenForHubSpotSubmit();

    if (isUnlocked()) {
      unlock({ scroll: false, force: true });
      return;
    }

    var slot = document.getElementById('content-gate-form');
    if (slot) mountHubSpotForm(slot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
