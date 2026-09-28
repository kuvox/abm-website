(function () {
  'use strict';

  // Generic HubSpot form wiring.
  // Usage: <form data-hs-form="FORM_GUID"> ... </form>
  // - Field NAMES must match HubSpot internal property names
  //   (firstname, lastname, email, phone, company, website, message, ...).
  // - Submits to HubSpot's Forms API with page URL + title so HubSpot
  //   records the source page on the contact.
  // - Optional: data-hs-success="Custom thank you message" on the form.

  var PORTAL_ID = '14501596';

  function getHutk() {
    var match = document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : undefined;
  }

  function collectFields(form) {
    var fields = [];
    var seen = {};
    var els = form.querySelectorAll('input[name], select[name], textarea[name]');

    Array.prototype.forEach.call(els, function (el) {
      var name = el.name;
      var type = (el.type || '').toLowerCase();
      if (type === 'submit' || type === 'button' || type === 'reset') return;

      if (type === 'radio') {
        if (!el.checked) return;
        fields.push({ name: name, value: el.value });
        return;
      }

      if (type === 'checkbox') {
        if (!el.checked) return;
        if (seen[name] !== undefined) {
          fields[seen[name]].value += ';' + el.value; // HubSpot multi-checkbox format
        } else {
          seen[name] = fields.length;
          fields.push({ name: name, value: el.value });
        }
        return;
      }

      var value = (el.value || '').trim();
      if (value === '') return; // omit empty optional fields
      if (name === 'website' && !/^https?:\/\//i.test(value)) value = 'https://' + value;
      fields.push({ name: name, value: value });
    });

    return fields;
  }

  function setStatus(form, message, isError) {
    var status = form.querySelector('.hs-form-status');
    if (!status) {
      status = document.createElement('p');
      status.className = 'hs-form-status';
      status.setAttribute('role', 'status');
      form.appendChild(status);
    }
    status.hidden = false;
    status.textContent = message;
    status.classList.toggle('is-error', !!isError);
    status.classList.toggle('is-success', !isError);
  }

  function initForm(form) {
    var formId = form.getAttribute('data-hs-form');
    if (!formId) return;

    var endpoint =
      'https://api.hsforms.com/submissions/v3/integration/submit/' +
      PORTAL_ID + '/' + formId;

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      if (typeof form.checkValidity === 'function' && !form.checkValidity()) {
        if (typeof form.reportValidity === 'function') form.reportValidity();
        return;
      }

      var button = form.querySelector('button[type="submit"], input[type="submit"]');
      if (button) button.disabled = true;
      setStatus(form, 'Sending…');

      var payload = {
        fields: collectFields(form),
        context: {
          pageUri: window.location.href,
          pageName: document.title,
        },
      };
      var hutk = getHutk();
      if (hutk) payload.context.hutk = hutk;

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          if (!res.ok) {
            return res.json().catch(function () { return {}; }).then(function (body) {
              throw new Error((body && body.message) || 'Submit failed');
            });
          }
          var message =
            form.getAttribute('data-hs-success') ||
            "Thanks — we've received your message and will be in touch soon.";
          // Hide everything except the status line. Use inline display:none
          // (not the hidden attribute) so display:grid rows like .form-row-split
          // can't override it; also hide any intro copy in the form's parent
          // that's marked data-hs-hide-on-success.
          Array.prototype.forEach.call(form.children, function (el) {
            if (!el.classList.contains('hs-form-status')) el.style.display = 'none';
          });
          Array.prototype.forEach.call(
            form.parentNode.querySelectorAll('[data-hs-hide-on-success]'),
            function (el) { el.style.display = 'none'; }
          );
          form.classList.add('is-submitted');
          setStatus(form, message);
          if (typeof form.reset === 'function') form.reset();

          // Conversion signal for GTM/GA4 — genuine success only (never in .catch()).
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            event: 'lead_form_submit',
            form_id: formId,
            form_name: form.getAttribute('data-hs-form-name') || 'contact',
            page_path: window.location.pathname,
          });
        })
        .catch(function () {
          setStatus(form, 'Something went wrong. Please try again, or email us directly.', true);
          if (button) button.disabled = false;
        });
    });
  }

  function init() {
    var forms = document.querySelectorAll('form[data-hs-form]');
    Array.prototype.forEach.call(forms, initForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
