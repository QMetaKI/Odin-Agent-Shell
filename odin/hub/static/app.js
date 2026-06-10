/**
 * Odin Local Runtime Hub — browser shell app.
 * Local static only. No external network. No apply. No external send.
 * Candidate-only. Localhost API only.
 *
 * Claim boundary: browser_hub_shell_candidate_only_no_apply_no_external_send
 */

/* Import the API client (loaded separately as api_client.js is in parent dir,
   so we inline the client calls here for the static shell context). */

var ODIN_API_BASE = 'http://127.0.0.1:8877';

/* ------------------------------------------------------------------ */
/* Safe localhost-only URL guard                                        */
/* ------------------------------------------------------------------ */
function isLocalhostUrl(url) {
  try {
    var u = new URL(url);
    return (u.hostname === '127.0.0.1' || u.hostname === 'localhost' || u.hostname === '::1');
  } catch (e) {
    return false;
  }
}

/* ------------------------------------------------------------------ */
/* Minimal fetch wrapper — never reaches non-localhost                 */
/* ------------------------------------------------------------------ */
function apiFetch(path) {
  var url = ODIN_API_BASE + path;
  if (!isLocalhostUrl(url)) {
    return Promise.reject(new Error('Non-localhost URL blocked: ' + url));
  }
  return fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
    .then(function(r) {
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json();
    });
}

/* ------------------------------------------------------------------ */
/* Panel update helpers                                                 */
/* ------------------------------------------------------------------ */
function setContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function renderPre(obj) {
  return '<pre>' + escapeHtml(JSON.stringify(obj, null, 2)) + '</pre>';
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function showError(id, msg) {
  setContent(id, '<p class="api-error">Unable to reach local API: ' + escapeHtml(msg) +
    ' — ensure the Odin local runtime is running on ' + escapeHtml(ODIN_API_BASE) + '</p>');
}

/* ------------------------------------------------------------------ */
/* Health panel                                                         */
/* ------------------------------------------------------------------ */
function loadHealth() {
  apiFetch('/v1/health').then(function(data) {
    var status = data.status || 'unknown';
    var cls = status === 'ok' ? 'status-ok' : 'status-warn';
    var html = '<p class="' + cls + '">Status: <strong>' + escapeHtml(status) + '</strong></p>';
    if (data.candidate_only) {
      html += '<p class="status-warn">candidate_only: true</p>';
    }
    html += renderPre(data);
    setContent('health-content', html);
  }).catch(function(e) {
    showError('health-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Status panel                                                         */
/* ------------------------------------------------------------------ */
function loadStatus() {
  apiFetch('/v1/status').then(function(data) {
    setContent('status-content', renderPre(data));
  }).catch(function(e) {
    showError('status-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Providers panel (read-only)                                          */
/* ------------------------------------------------------------------ */
function loadProviders() {
  apiFetch('/v1/providers').then(function(data) {
    var providers = data.providers || [];
    if (providers.length === 0) {
      setContent('providers-content', '<p class="provider-disabled">No providers registered.</p>');
      return;
    }
    var items = providers.map(function(p) {
      var enabled = p.enabled_by_default || p.enabled || false;
      var cls = enabled ? 'provider-enabled' : 'provider-disabled';
      var name = escapeHtml(p.provider_id || p.id || '(unknown)');
      var badge = enabled ? 'enabled' : 'disabled';
      return '<li class="' + cls + '">' + name + ' — ' + badge + '</li>';
    }).join('');
    setContent('providers-content', '<ul class="provider-list">' + items + '</ul>');
  }).catch(function(e) {
    showError('providers-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Proof gaps panel                                                     */
/* ------------------------------------------------------------------ */
function loadProofGaps() {
  apiFetch('/v1/proof-gaps').then(function(data) {
    var gaps = data.proof_gaps || data.gaps || [];
    if (gaps.length === 0) {
      setContent('proof-gaps-content', '<p class="status-ok">No proof gaps reported.</p>');
      return;
    }
    var items = gaps.map(function(g) {
      return '<li>' + escapeHtml(typeof g === 'string' ? g : JSON.stringify(g)) + '</li>';
    }).join('');
    setContent('proof-gaps-content', '<ul class="proof-gap-list">' + items + '</ul>');
  }).catch(function(e) {
    showError('proof-gaps-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Initialise                                                           */
/* ------------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', function() {
  // Display resolved API base URL
  var baseEl = document.getElementById('api-base-url');
  if (baseEl) { baseEl.textContent = ODIN_API_BASE; }

  loadHealth();
  loadStatus();
  loadProviders();
  loadProofGaps();
});

/* No apply(), external_send(), submitUniversalWork(), or provider credential methods. */
