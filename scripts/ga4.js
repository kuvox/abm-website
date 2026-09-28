(function () {
  var MEASUREMENT_ID = 'G-1W20WVXCT6';
  var GTM_ID = 'GTM-NN575G4';
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID);

  var script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
  document.head.appendChild(script);

  // Google Tag Manager — loaded here so every page that includes ga4.js
  // (hand-maintained and generated) gets the container without per-page edits.
  if (!window.__abmGtmLoaded) {
    window.__abmGtmLoaded = true;
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var gtm = document.createElement('script');
    gtm.async = true;
    gtm.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    document.head.appendChild(gtm);
  }
})();
