/**
 * Cloudflare Pages Function: POST /api/lead-notify
 *
 * Called by scripts/hubspot-form.js AFTER a successful HubSpot submission,
 * only for forms marked data-hs-notify. Forwards the lead to a Slack
 * Workflow Builder webhook so the right person gets a DM.
 *
 * Env vars (Cloudflare Pages > Settings > Variables and Secrets):
 *   SLACK_WEBHOOK_DEALERSHIP_AI_SALES_AGENT  — webhook URL for the
 *     "Dealership AI Sales Agent Lead to Kodi" workflow.
 *
 * To notify on another form: add its data-hs-form-name to WEBHOOKS below
 * with a new env var, and put data-hs-notify on that <form>.
 */

var WEBHOOKS = {
  dealership_ai_sales_agent: 'SLACK_WEBHOOK_DEALERSHIP_AI_SALES_AGENT',
};

var ALLOWED_ORIGINS = [
  'https://abeckermarketing.com',
  'https://www.abeckermarketing.com',
];

function clean(v, max) {
  return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max || 500);
}

export async function onRequestPost(context) {
  var request = context.request;
  var env = context.env;

  var origin = request.headers.get('Origin') || '';
  var isPreview = /\.pages\.dev$/.test(new URL(origin || 'https://x.invalid').hostname);
  if (ALLOWED_ORIGINS.indexOf(origin) === -1 && !isPreview) {
    return new Response('Forbidden', { status: 403 });
  }

  var body;
  try {
    body = await request.json();
  } catch (e) {
    return new Response('Bad request', { status: 400 });
  }

  var formName = clean(body.form_name, 80);
  var envKey = WEBHOOKS[formName];
  if (!envKey) return new Response('Ignored', { status: 204 });

  var webhook = env[envKey];
  if (!webhook) {
    console.log('lead-notify: missing env var ' + envKey);
    return new Response('Not configured', { status: 204 });
  }

  var fields = body.fields || {};
  var payload = {
    name: clean(fields.firstname || fields.name, 120) || '(not provided)',
    email: clean(fields.email, 200) || '(not provided)',
    website: clean(fields.website, 300) || '(not provided)',
    message: clean(fields.message, 1500) || '(none)',
    page: clean(body.page, 300) || 'https://abeckermarketing.com/',
  };

  var res = await fetch(webhook, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  return new Response(res.ok ? 'OK' : 'Upstream error', {
    status: res.ok ? 200 : 502,
    headers: { 'Access-Control-Allow-Origin': origin },
  });
}

export function onRequestOptions(context) {
  var origin = context.request.headers.get('Origin') || '';
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}
