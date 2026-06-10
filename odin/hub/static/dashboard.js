/**
 * Odin Local Runtime Hub — Dashboard surfaces.
 *
 * Claim boundary: hub_runtime_dashboard_candidate_only_local_only_no_apply_no_external_send_no_production_health_claim
 *
 * Provides read-only dashboard surfaces:
 *   - Runtime status (running / not-running / unknown)
 *   - Health surface (/v1/health with candidate_only, claim_boundary)
 *   - Validation status surface (/v1/status)
 *   - Doctor result surface (read-only, fixture-compatible)
 *   - Support bundle surface (local-only, no upload)
 *   - Proof-gap summary (/v1/proof-gaps, does not claim closure)
 *   - Missing capability explanation
 *
 * Not proven:
 *   - production_readiness
 *   - live_model_inference
 *   - app_state_mutation
 *   - external_send_authority
 *   - production_health_certification
 *   - hidden_diagnostic_upload_absence_beyond_static_scan
 *
 * Forbidden in this file:
 *   - apply() / externalSend() / submitUniversalWork() methods
 *   - hidden upload / remote send
 *   - apply buttons or forms
 *   - provider credential input
 */

/* ------------------------------------------------------------------ */
/* Dashboard Claim Boundary                                             */
/* ------------------------------------------------------------------ */
var DASHBOARD_CLAIM_BOUNDARY =
  'hub_runtime_dashboard_candidate_only_local_only_no_apply_no_external_send_no_production_health_claim';

var DASHBOARD_NOT_PROVEN = [
  'production_readiness',
  'production_health_certification',
  'hosted_cloud_dashboard',
  'live_browser_runtime_e2e',
  'provider_execution',
  'app_state_mutation',
  'external_send_authority',
  'hidden_diagnostic_upload_absence_beyond_static_scan',
  'live_model_inference',
  'model_quality',
];

/* ------------------------------------------------------------------ */
/* Shared helpers (defined here so dashboard.js is self-contained)     */
/* ------------------------------------------------------------------ */
var DASHBOARD_API_BASE = (typeof ODIN_API_BASE !== 'undefined') ? ODIN_API_BASE : 'http://127.0.0.1:8877';

function dashIsLocalhost(url) {
  try {
    var u = new URL(url);
    return (u.hostname === '127.0.0.1' || u.hostname === 'localhost' || u.hostname === '::1');
  } catch (e) {
    return false;
  }
}

function dashFetch(path) {
  var url = DASHBOARD_API_BASE + path;
  if (!dashIsLocalhost(url)) {
    return Promise.reject(new Error('Dashboard: Non-localhost URL blocked: ' + url));
  }
  return fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
    .then(function(r) {
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json();
    });
}

function dashSetContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function dashRenderPre(obj) {
  return '<pre>' + dashEscape(JSON.stringify(obj, null, 2)) + '</pre>';
}

function dashEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function dashShowError(id, msg) {
  dashSetContent(id,
    '<p class="api-error">Unable to reach local API: ' + dashEscape(msg) +
    ' — ensure the Odin local runtime is running on ' + dashEscape(DASHBOARD_API_BASE) + '</p>'
  );
}

/* ------------------------------------------------------------------ */
/* Runtime Status Surface                                               */
/* Shows running / not-running / unknown — does not claim production   */
/* ------------------------------------------------------------------ */
function loadRuntimeStatus() {
  var el = document.getElementById('runtime-status-indicator');
  if (el) {
    el.textContent = 'Checking…';
    el.className = 'runtime-status-unknown';
  }
  dashFetch('/v1/health').then(function(data) {
    var st = data.status || 'unknown';
    var running = (st === 'ok' || st === 'running');
    var cls = running ? 'runtime-status-running' : 'runtime-status-not-running';
    var label = running ? 'Running' : 'Not Running / Unknown';
    if (el) {
      el.textContent = label;
      el.className = cls;
    }
    var detail = document.getElementById('runtime-status-detail');
    if (detail) {
      var html = '<p class="status-note">API status: <strong>' + dashEscape(st) + '</strong></p>';
      html += '<p class="status-note">API base: <code>' + dashEscape(DASHBOARD_API_BASE) + '</code></p>';
      html += '<p class="status-note">Localhost only: <strong>yes</strong></p>';
      if (data.candidate_only) {
        html += '<p class="status-note">candidate_only: <strong>true</strong></p>';
      }
      if (data.claim_boundary) {
        html += '<p class="status-note">claim_boundary: <code>' + dashEscape(data.claim_boundary) + '</code></p>';
      }
      html += '<p class="boundary-note">Not a production health certification. Not a hosted cloud dashboard.</p>';
      detail.innerHTML = html;
    }
  }).catch(function(e) {
    if (el) {
      el.textContent = 'Not Running / API Unreachable';
      el.className = 'runtime-status-not-running';
    }
    var detail = document.getElementById('runtime-status-detail');
    if (detail) {
      detail.innerHTML = '<p class="api-error">API unreachable: ' + dashEscape(e.message) + '</p>' +
        '<p class="boundary-note">Not a production health certification. Localhost only.</p>';
    }
  });
}

/* ------------------------------------------------------------------ */
/* Health Surface                                                        */
/* Shows /v1/health with candidate_only, claim_boundary, known_non_proofs */
/* ------------------------------------------------------------------ */
function loadDashboardHealth() {
  dashFetch('/v1/health').then(function(data) {
    var st = data.status || 'unknown';
    var cls = st === 'ok' ? 'status-ok' : 'status-warn';
    var html = '<p class="' + cls + '">Status: <strong>' + dashEscape(st) + '</strong></p>';
    if (data.candidate_only) {
      html += '<p>candidate_only: <strong>true</strong></p>';
    }
    if (data.claim_boundary) {
      html += '<p>claim_boundary: <code>' + dashEscape(data.claim_boundary) + '</code></p>';
    }
    if (data.known_non_proofs && data.known_non_proofs.length) {
      html += '<p class="status-warn">known_non_proofs:</p><ul class="proof-gap-list">';
      data.known_non_proofs.forEach(function(np) {
        html += '<li>' + dashEscape(String(np)) + '</li>';
      });
      html += '</ul>';
    }
    html += dashRenderPre(data);
    html += '<p class="boundary-note">Not a production health certification. Localhost only. Candidate-only.</p>';
    dashSetContent('dashboard-health-content', html);
  }).catch(function(e) {
    dashShowError('dashboard-health-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Validation Status Surface                                             */
/* Shows /v1/status — local-receipt-compatible                          */
/* ------------------------------------------------------------------ */
function loadValidationStatus() {
  dashFetch('/v1/status').then(function(data) {
    var html = '';
    var validations = data.validations || data.validation_status || {};
    if (Object.keys(validations).length > 0) {
      html += '<table class="validation-table"><thead><tr><th>Validator</th><th>Status</th></tr></thead><tbody>';
      Object.keys(validations).forEach(function(k) {
        var v = validations[k];
        var ok = (v === 'ok' || v === true || v === 'pass');
        var cls = ok ? 'status-ok' : 'status-warn';
        html += '<tr><td>' + dashEscape(k) + '</td><td class="' + cls + '">' + dashEscape(String(v)) + '</td></tr>';
      });
      html += '</tbody></table>';
    } else {
      html += dashRenderPre(data);
    }
    html += '<p class="boundary-note">Validation status shown is local-receipt-compatible. Live validation not claimed without receipt.</p>';
    dashSetContent('validation-status-content', html);
  }).catch(function(e) {
    dashShowError('validation-status-content', e.message);
  });
}

/* ------------------------------------------------------------------ */
/* Doctor Result Surface                                                 */
/* Read-only placeholder — renders doctor data if available from API   */
/* Does not execute repair. Does not mutate config.                     */
/* ------------------------------------------------------------------ */
function loadDoctorResult() {
  dashFetch('/v1/health').then(function(data) {
    var html = '';
    var doctorStatus = data.doctor_status || data.doctor || null;
    var warnings = data.doctor_warnings || data.warnings || [];
    var errors = data.doctor_errors || data.errors || [];
    var failures = data.failure_reasons || [];

    if (doctorStatus) {
      var cls = (doctorStatus === 'ok' || doctorStatus === 'pass') ? 'status-ok' : 'status-warn';
      html += '<p class="' + cls + '">Doctor status: <strong>' + dashEscape(String(doctorStatus)) + '</strong></p>';
    } else {
      html += '<p class="status-warn">Doctor status: not available from API — showing health data</p>';
    }

    if (warnings.length) {
      html += '<p class="status-warn">Warnings:</p><ul>';
      warnings.forEach(function(w) { html += '<li>' + dashEscape(String(w)) + '</li>'; });
      html += '</ul>';
    }
    if (errors.length) {
      html += '<p class="status-error">Errors:</p><ul>';
      errors.forEach(function(e) { html += '<li>' + dashEscape(String(e)) + '</li>'; });
      html += '</ul>';
    }
    if (failures.length) {
      html += '<p class="status-error">Failure reasons:</p><ul>';
      failures.forEach(function(f) { html += '<li>' + dashEscape(String(f)) + '</li>'; });
      html += '</ul>';
    }

    var repairHint = data.repair_hint || 'Run: python -m odin.cli doctor && python -m odin.cli repair-local-runtime --plan-only';
    html += '<p class="boundary-note">Recommended plan-only repair hint: <code>' + dashEscape(repairHint) + '</code></p>';
    html += '<p class="boundary-note">Doctor surface is read-only. No repair executed. No config mutated.</p>';
    dashSetContent('doctor-content', html);
  }).catch(function(e) {
    dashSetContent('doctor-content',
      '<p class="api-error">Doctor data unavailable: ' + dashEscape(e.message) + '</p>' +
      '<p class="boundary-note">Run locally: <code>python -m odin.cli doctor</code></p>' +
      '<p class="boundary-note">Read-only. No repair. No mutation.</p>'
    );
  });
}

/* ------------------------------------------------------------------ */
/* Support Bundle Surface                                               */
/* Local-only. Diagnostics-only. No upload. No hidden send.            */
/* ------------------------------------------------------------------ */
function initSupportBundle() {
  var el = document.getElementById('support-bundle-content');
  if (!el) { return; }
  el.innerHTML =
    '<p class="boundary-note">Support bundle export is <strong>local-only</strong> and <strong>diagnostics-only</strong>.</p>' +
    '<p class="boundary-note">Redaction applied — no secrets in bundle.</p>' +
    '<p class="boundary-note">No hidden upload. No remote send. No diagnostic transport.</p>' +
    '<p>To export a local support bundle, run:</p>' +
    '<pre>python -m odin.cli emit-support-bundle --out .odin_runtime/support --diagnostics-only</pre>' +
    '<p class="boundary-note">Bundle output: local filesystem only. Not uploaded. Not sent externally.</p>' +
    '<p class="boundary-note">Diagnostics local only. Candidate-only.</p>';
}

/* ------------------------------------------------------------------ */
/* Proof-Gap Summary                                                     */
/* Shows proof gaps. Does not claim gaps are closed.                    */
/* ------------------------------------------------------------------ */
function loadProofGapSummary() {
  dashFetch('/v1/proof-gaps').then(function(data) {
    var gaps = data.proof_gaps || data.gaps || [];
    var boundaries = data.proof_boundaries || [];
    var html = '';

    if (gaps.length === 0) {
      html += '<p class="status-warn">No proof gaps reported by API — gaps may still exist locally.</p>';
    } else {
      html += '<p>Known proof gaps (' + gaps.length + '):</p><ul class="proof-gap-list">';
      gaps.forEach(function(g) {
        html += '<li>' + dashEscape(typeof g === 'string' ? g : JSON.stringify(g)) + '</li>';
      });
      html += '</ul>';
    }

    if (boundaries.length) {
      html += '<p>Proof boundaries:</p><ul class="proof-gap-list">';
      boundaries.forEach(function(b) {
        html += '<li>' + dashEscape(typeof b === 'string' ? b : JSON.stringify(b)) + '</li>';
      });
      html += '</ul>';
    }

    html += '<p class="boundary-note">Displaying proof gaps does not close them.</p>';
    html += '<p class="boundary-note">Not a production health certification. Not a hosted cloud dashboard.</p>';
    dashSetContent('proof-gap-summary-content', html);
  }).catch(function(e) {
    dashSetContent('proof-gap-summary-content',
      '<p class="api-error">Proof gaps unavailable from API: ' + dashEscape(e.message) + '</p>' +
      '<p class="boundary-note">Displaying proof gaps does not close them.</p>'
    );
  });
}

/* ------------------------------------------------------------------ */
/* Missing Capabilities Surface                                          */
/* Explains what is missing / not yet proven                            */
/* ------------------------------------------------------------------ */
function initMissingCapabilities() {
  var el = document.getElementById('missing-capabilities-content');
  if (!el) { return; }
  var items = DASHBOARD_NOT_PROVEN;
  var html = '<p>The following are <strong>not proven</strong> by this dashboard:</p>';
  html += '<ul class="proof-gap-list">';
  items.forEach(function(item) {
    html += '<li>' + dashEscape(item) + '</li>';
  });
  html += '</ul>';
  html += '<p class="boundary-note">claim_boundary: <code>' + dashEscape(DASHBOARD_CLAIM_BOUNDARY) + '</code></p>';
  html += '<p class="boundary-note">No app apply. No external send. No provider execution. Localhost only.</p>';
  el.innerHTML = html;
}

/* ------------------------------------------------------------------ */
/* Dashboard initialisation                                              */
/* ------------------------------------------------------------------ */
function initDashboard() {
  loadRuntimeStatus();
  loadDashboardHealth();
  loadValidationStatus();
  loadDoctorResult();
  initSupportBundle();
  loadProofGapSummary();
  initMissingCapabilities();
}

document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('dashboard-panel')) {
    initDashboard();
  }
});

/* No apply(), externalSend(), submitUniversalWork(), or provider credential methods. */
