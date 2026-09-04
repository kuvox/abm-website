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

  var COOKIE_DAYS = 365;

  function hasCookie() {
    return new RegExp('(?:^|;\\s*)' + STORAGE_KEY + '=1(?:;|$)').test(document.cookie);
  }

  function setCookie() {
    try {
      var expires = new Date(Date.now() + COOKIE_DAYS * 864e5).toUTCString();
      document.cookie = STORAGE_KEY + '=1; expires=' + expires + '; path=/; SameSite=Lax' +
        (location.protocol === 'https:' ? '; Secure' : '');
    } catch (e) { /* ignore */ }
  }

  function isUnlocked() {
    // localStorage is the primary flag; a first-party cookie is the backup so
    // the unlock survives storage being cleared independently of cookies
    // (and vice versa). Either one is enough.
    var stored = false;
    try { stored = localStorage.getItem(STORAGE_KEY) === '1'; } catch (e) { /* ignore */ }
    return stored || hasCookie();
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

  function resourceSlug() {
    var parts = window.location.pathname.split('/').filter(Boolean);
    var last = parts[parts.length - 1] || '';
    return last.replace(/\.html$/, '');
  }

  function trackUnlock() {
    // Conversion signal for GTM/GA4 — only fired on a real form submission,
    // not on revisit (localStorage) or ?access=unlocked email links.
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'lead_form_submit',
      form_id: HUBSPOT_FORM_ID,
      form_name: 'gated_content',
      resource_slug: resourceSlug(),
      page_path: window.location.pathname,
    });
  }

  function unlock(options) {
    if (unlocked && !(options && options.force)) return;
    unlocked = true;
    if (options && options.fromSubmit) trackUnlock();

    try {
      localStorage.setItem(STORAGE_KEY, '1');
    } catch (e) { /* ignore */ }
    setCookie();

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
    // Only used when HubSpot's embed script cannot load. Mirrors the fields the
    // HubSpot form requires (first name, email, company website) so the
    // submission is accepted by the Forms API.
    container.innerHTML =
      '<form class="content-gate-fallback" id="content-gate-fallback" novalidate>' +
      '  <div class="form-row"><label for="content-gate-first">First name</label>' +
      '  <input type="text" id="content-gate-first" name="firstname" autocomplete="given-name" required></div>' +
      '  <div class="form-row"><label for="content-gate-email">Work email</label>' +
      '  <input type="email" id="content-gate-email" name="email" autocomplete="email" required placeholder="you@company.com"></div>' +
      '  <div class="form-row"><label for="content-gate-website">Company website</label>' +
      '  <input type="text" id="content-gate-website" name="website" inputmode="url" autocomplete="url" required placeholder="www.company.com"></div>' +
      '  <p class="content-gate-error" id="content-gate-error" hidden>Enter a valid work email address.</p>' +
      '  <button type="submit" class="btn btn-primary">Unlock the guide</button>' +
      '</form>';

    var form = document.getElementById('content-gate-fallback');
    var error = document.getElementById('content-gate-error');
    var button = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var first = (document.getElementById('content-gate-first').value || '').trim();
      var email = (document.getElementById('content-gate-email').value || '').trim();
      var site = (document.getElementById('content-gate-website').value || '').trim();
      if (!isValidEmail(email) || !first || !site) {
        error.textContent = !isValidEmail(email) ? 'Enter a valid work email address.' : 'Please fill in every field.';
        error.hidden = false;
        return;
      }
      error.hidden = true;
      button.disabled = true;
      if (!/^https?:\/\//i.test(site)) site = 'https://' + site;
      var payload = {
        fields: [
          { name: 'firstname', value: first },
          { name: 'email', value: email },
          { name: 'website', value: site },
        ],
        context: { pageUri: window.location.href, pageName: document.title },
      };
      var hutk = (document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/) || [])[1];
      if (hutk) payload.context.hutk = decodeURIComponent(hutk);
      fetch('https://api.hsforms.com/submissions/v3/integration/submit/' + HUBSPOT_PORTAL_ID + '/' + HUBSPOT_FORM_ID, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          if (!res.ok) throw new Error('submit failed');
          unlock({ scroll: true, fromSubmit: true });
        })
        .catch(function () {
          // Best effort: never leave the reader stuck if HubSpot rejects the
          // fallback (e.g. consent-field requirements). Unlock without tracking.
          unlock({ scroll: true });
        });
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
        unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
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
          unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
          return;
        }
        if (d.type === 'hsFormCallback' && d.id === 'onFormSubmitted') {
          unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
          return;
        }
        if (d.eventName === 'onFormSubmitted' || d.eventName === 'onFormSubmit') {
          unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
          return;
        }
      }

      // Occasional string payloads from embeds
      if (typeof d === 'string' && /onFormSubmitted|formSubmitted/i.test(d)) {
        unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
      }
    });

    // Global HubSpot event bus (classic + some new embeds)
    window.addEventListener('hs-form-event', function () {
      unlock({ moveSuccess: true, scroll: true, fromSubmit: true });
    });
  }

  var ACCESS_PARAM = 'access';
  var ACCESS_VALUE = 'unlocked';

  function hasAccessParam() {
    try {
      var params = new URLSearchParams(window.location.search);
      return params.get(ACCESS_PARAM) === ACCESS_VALUE;
    } catch (e) {
      return new RegExp('[?&]' + ACCESS_PARAM + '=' + ACCESS_VALUE + '(&|$)').test(window.location.search);
    }
  }

  function cleanAccessParam() {
    try {
      var url = new URL(window.location.href);
      url.searchParams.delete(ACCESS_PARAM);
      window.history.replaceState({}, document.title, url.pathname + url.search + url.hash);
    } catch (e) { /* ignore */ }
  }

  function init() {
    var gate = document.getElementById('content-gate');
    if (!gate) return;

    listenForHubSpotSubmit();

    // Auto-unlock via email link: ...?access=unlocked
    if (hasAccessParam()) {
      unlock({ scroll: false, force: true });
      cleanAccessParam();
      return;
    }

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
