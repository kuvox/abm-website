(function () {
  'use strict';

  var PORTAL_ID = '14501596';
  var FORM_ID = '5c51c724-f0f0-485e-8166-c178b2d5822a';
  var ENDPOINT =
    'https://api.hsforms.com/submissions/v3/integration/submit/' +
    PORTAL_ID +
    '/' +
    FORM_ID;

  function getHutk() {
    var match = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : undefined;
  }

  function initForm(form) {
    var emailInput = form.querySelector('input[type="email"]');
    var status = form.querySelector('.abm-newsletter-status');
    var button = form.querySelector('button[type="submit"]');
    if (!emailInput || !button) return;

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var email = (emailInput.value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (status) {
          status.hidden = false;
          status.textContent = 'Enter a valid email address.';
          status.classList.add('is-error');
          status.classList.remove('is-success');
        }
        return;
      }

      button.disabled = true;
      if (status) {
        status.hidden = false;
        status.textContent = 'Submitting…';
        status.classList.remove('is-error', 'is-success');
      }

      var payload = {
        fields: [{ name: 'email', value: email }],
        context: {
          pageUri: window.location.href,
          pageName: document.title,
        },
      };
      var hutk = getHutk();
      if (hutk) payload.context.hutk = hutk;

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          if (!res.ok) throw new Error('submit failed');
          if (status) {
            status.textContent = 'Thanks — you are subscribed.';
            status.classList.add('is-success');
            status.classList.remove('is-error');
          }
          form.reset();

          // Conversion signal for GTM/GA4 — genuine success only.
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            event: 'lead_form_submit',
            form_id: FORM_ID,
            form_name: 'newsletter',
            form_location: form.closest('.newsletter-cta') ? 'newsletter_section' : 'inline',
            page_path: window.location.pathname,
          });
        })
        .catch(function () {
          if (status) {
            status.textContent = 'Something went wrong. Please try again.';
            status.classList.add('is-error');
            status.classList.remove('is-success');
          }
        })
        .finally(function () {
          button.disabled = false;
        });
    });
  }

  function init() {
    document.querySelectorAll('form.abm-newsletter-form').forEach(initForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
