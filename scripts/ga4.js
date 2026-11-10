(function () {
  // All tags, including GA4 (G-1W20WVXCT6), are managed in Google Tag Manager.
  // The container loads through Google tag gateway on Cloudflare, so it is
  // served first-party from /a9rb/ instead of googletagmanager.com.
  var GTM_ID = 'GTM-NN575G4';
  var GATEWAY_PATH = '/a9rb/';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };

  if (!window.__abmGtmLoaded) {
    window.__abmGtmLoaded = true;
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var gtm = document.createElement('script');
    gtm.async = true;
    gtm.src = GATEWAY_PATH + '?id=' + GTM_ID;
    document.head.appendChild(gtm);
  }
})();
