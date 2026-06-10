/**
 * Odin Local Runtime Hub — Candidate Store Viewer (LRH-PR-08)
 *
 * Claim boundary: candidate_store_viewer_candidate_only_local_only_no_apply_no_external_send_no_store_mutation_no_raw_payload
 *
 * Provides read-only viewer surfaces:
 *   - Sessions view (/v1/sessions/{id}, fixture-compatible placeholder)
 *   - Candidate artifact view (/v1/candidates/{id})
 *   - Store metadata view (metadata-first, no raw records, no mutation)
 *   - Proof gap viewer (/v1/proof-gaps — displays gaps, does not close them)
 *   - Candidate-only boundary banner on every surface
 *   - Not-applied truth warning on every candidate surface
 *   - Raw sensitive payload protection (redacted/not displayed by default)
 *
 * Not proven:
 *   - production_readiness
 *   - live_model_inference
 *   - app_state_mutation
 *   - external_send_authority
 *   - full_session_list_backend
 *   - full_candidate_backend_coverage
 *   - full_store_backend_coverage
 *   - raw_sensitive_payload_safety_certification
 *   - candidate_application
 *   - store_mutation
 *
 * Forbidden in this file:
 *   - applyCandidate() / apply() / externalSend() methods
 *   - apply button or form
 *   - store write/delete/mutation controls
 *   - raw sensitive payload display
 *   - external-send controls
 *   - provider credential input
 *   - hidden upload / remote send
 */

/* ------------------------------------------------------------------ */
/* Candidate Store Viewer Claim Boundary                               */
/* ------------------------------------------------------------------ */
var CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY =
  'candidate_store_viewer_candidate_only_local_only_no_apply_no_external_send_no_store_mutation_no_raw_payload';

/* Explicit boundary tokens required by validator */
var CANDIDATE_STORE_VIEWER_BOUNDARY_TOKENS = [
  'candidate_only',
  'claim_boundary',
  'not_applied_truth',
  'no_apply',
  'no_external_send',
  'no_store_mutation',
  'no_raw_payload',
];

var CANDIDATE_STORE_VIEWER_NOT_PROVEN = [
  'production_readiness',
  'live_model_inference',
  'app_state_mutation',
  'external_send_authority',
  'full_session_list_backend',
  'full_candidate_backend_coverage',
  'full_store_backend_coverage',
  'raw_sensitive_payload_safety_certification',
  'candidate_application',
  'store_mutation',
  'live_browser_runtime_e2e',
];

/* ------------------------------------------------------------------ */
/* Shared helpers                                                       */
/* ------------------------------------------------------------------ */
var CSV_API_BASE = (typeof ODIN_API_BASE !== 'undefined') ? ODIN_API_BASE : 'http://127.0.0.1:8877';

function csvIsLocalhost(url) {
  try {
    var u = new URL(url);
    return (u.hostname === '127.0.0.1' || u.hostname === 'localhost' || u.hostname === '::1');
  } catch (e) {
    return false;
  }
}

function csvFetch(path) {
  var url = CSV_API_BASE + path;
  if (!csvIsLocalhost(url)) {
    return Promise.reject(new Error('CandidateStoreViewer: Non-localhost URL blocked: ' + url));
  }
  return fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
    .then(function(r) {
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json();
    });
}

function csvSetContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function csvEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function csvShowError(id, msg) {
  csvSetContent(id,
    '<p class="api-error">Unable to reach local API: ' + csvEscape(msg) +
    ' — ensure the Odin local runtime is running on ' + csvEscape(CSV_API_BASE) + '</p>' +
    '<p class="boundary-note">Candidate-only. Not applied truth. No app apply.</p>'
  );
}

/* Redact any value that looks like a raw sensitive payload */
function csvRedactSensitive(key, value) {
  var sensitiveKeys = [
    'secret', 'token', 'password', 'key', 'credential', 'auth',
    'private', 'raw_payload', 'payload_raw', 'sensitive',
  ];
  var keyLower = String(key).toLowerCase();
  for (var i = 0; i < sensitiveKeys.length; i++) {
    if (keyLower.indexOf(sensitiveKeys[i]) !== -1) {
      return '[REDACTED — raw sensitive payload not displayed]';
    }
  }
  return value;
}

function csvSafeRenderObject(obj, depth) {
  depth = depth || 0;
  if (depth > 2) { return '<em class="muted">[nested — not expanded]</em>'; }
  if (obj === null || obj === undefined) { return csvEscape(String(obj)); }
  if (typeof obj !== 'object') { return csvEscape(String(obj)); }
  if (Array.isArray(obj)) {
    if (obj.length === 0) { return '<em class="muted">(empty)</em>'; }
    return '<ul>' + obj.map(function(item) {
      return '<li>' + csvSafeRenderObject(item, depth + 1) + '</li>';
    }).join('') + '</ul>';
  }
  var rows = Object.keys(obj).map(function(k) {
    var raw = obj[k];
    var val = csvRedactSensitive(k, raw);
    var rendered = (val !== raw) ? csvEscape(val) : csvSafeRenderObject(raw, depth + 1);
    return '<tr><td class="key-cell">' + csvEscape(k) + '</td><td>' + rendered + '</td></tr>';
  }).join('');
  return '<table class="csv-table"><tbody>' + rows + '</tbody></table>';
}

/* ------------------------------------------------------------------ */
/* Candidate-Only Boundary Banner                                       */
/* Required on every viewer surface                                     */
/* ------------------------------------------------------------------ */
function csvBoundaryBanner(extra) {
  return '<div class="csv-boundary-banner" aria-label="Candidate-Only Boundary">' +
    '<strong>Candidate-only</strong> — ' +
    '<span class="boundary-item">Not applied truth</span> · ' +
    '<span class="boundary-item">App-owned apply</span> · ' +
    '<span class="boundary-item">No app apply</span> · ' +
    '<span class="boundary-item">No external send</span> · ' +
    '<span class="boundary-item">No store mutation</span> · ' +
    '<span class="boundary-item">No raw sensitive payload display</span>' +
    (extra ? ' · <span class="boundary-item">' + csvEscape(extra) + '</span>' : '') +
    '</div>';
}

function csvNotAppliedWarning() {
  return '<p class="csv-not-applied-warning">' +
    'Not applied truth — candidate artifacts are candidate-only. ' +
    'The app owns apply, state, external sends, and domain authority.' +
    '</p>';
}

/* ------------------------------------------------------------------ */
/* Sessions View                                                        */
/* Uses /v1/sessions/{id} — no bulk list endpoint assumed              */
/* Falls back to fixture-compatible placeholder if API absent           */
/* ------------------------------------------------------------------ */
function loadSessionsView(sessionId) {
  var container = document.getElementById('csv-sessions-content');
  if (!container) { return; }

  container.innerHTML = csvBoundaryBanner('read-only') + csvNotAppliedWarning() +
    '<p class="loading">Loading session data…</p>';

  var path = sessionId ? ('/v1/sessions/' + encodeURIComponent(sessionId)) : '/v1/sessions/current';

  csvFetch(path).then(function(data) {
    var html = csvBoundaryBanner('read-only') + csvNotAppliedWarning();
    html += '<div class="csv-session-record">';

    var sessionIdVal = data.session_id || data.id || sessionId || '(unknown)';
    html += '<p><strong>Session ID:</strong> <code>' + csvEscape(String(sessionIdVal)) + '</code></p>';

    if (data.status) {
      var cls = (data.status === 'active' || data.status === 'ok') ? 'status-ok' : 'status-warn';
      html += '<p><strong>Status:</strong> <span class="' + cls + '">' + csvEscape(String(data.status)) + '</span></p>';
    }

    if (data.created_at || data.created) {
      html += '<p><strong>Created:</strong> ' + csvEscape(String(data.created_at || data.created)) + '</p>';
    }
    if (data.updated_at || data.updated) {
      html += '<p><strong>Updated:</strong> ' + csvEscape(String(data.updated_at || data.updated)) + '</p>';
    }

    var candidateCount = data.candidate_count || (data.candidates && data.candidates.length) || null;
    if (candidateCount !== null) {
      html += '<p><strong>Candidate count:</strong> ' + csvEscape(String(candidateCount)) + '</p>';
    }

    if (data.claim_boundary) {
      html += '<p><strong>claim_boundary:</strong> <code>' + csvEscape(String(data.claim_boundary)) + '</code></p>';
    }
    if (data.candidate_only !== undefined) {
      html += '<p><strong>candidate_only:</strong> <code>' + csvEscape(String(data.candidate_only)) + '</code></p>';
    }

    html += '</div>';
    html += '<p class="boundary-note">Session view is read-only. No session mutation. candidate_only.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = csvBoundaryBanner('read-only') + csvNotAppliedWarning();
    html += '<p class="api-error">Session data unavailable: ' + csvEscape(e.message) + '</p>';
    html += '<div class="csv-fixture-placeholder">';
    html += '<p class="boundary-note">Sessions endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><strong>Proof gap:</strong> full_session_list_backend not proven.</p>';
    html += '<p>To query a session: <code>GET ' + csvEscape(CSV_API_BASE) + '/v1/sessions/{session_id}</code></p>';
    html += csvSafeRenderObject({
      session_id: '(fixture-placeholder)',
      status: 'unknown',
      candidate_only: true,
      claim_boundary: CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY,
      note: 'Session list backend not available — proof gap recorded'
    });
    html += '</div>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Candidate Artifact View                                              */
/* Uses /v1/candidates/{id}                                            */
/* Does NOT show candidate as applied truth                            */
/* Does NOT display raw sensitive payloads                             */
/* ------------------------------------------------------------------ */
function loadCandidateView(candidateId) {
  var container = document.getElementById('csv-candidate-content');
  if (!container) { return; }

  container.innerHTML = csvBoundaryBanner() + csvNotAppliedWarning() +
    '<p class="loading">Loading candidate data…</p>';

  var path = candidateId ? ('/v1/candidates/' + encodeURIComponent(candidateId)) : '/v1/candidates/latest';

  csvFetch(path).then(function(data) {
    var html = csvBoundaryBanner() + csvNotAppliedWarning();
    html += '<div class="csv-candidate-record">';

    var cidVal = data.candidate_id || data.id || candidateId || '(unknown)';
    html += '<p><strong>Candidate ID:</strong> <code>' + csvEscape(String(cidVal)) + '</code></p>';

    if (data.session_id) {
      html += '<p><strong>Session ID:</strong> <code>' + csvEscape(String(data.session_id)) + '</code></p>';
    }

    if (data.status) {
      var cls = (data.status === 'ok' || data.status === 'ready') ? 'status-ok' : 'status-warn';
      html += '<p><strong>Status:</strong> <span class="' + cls + '">' + csvEscape(String(data.status)) + '</span></p>';
    }

    if (data.artifact_kind) {
      html += '<p><strong>Artifact kind:</strong> <code>' + csvEscape(String(data.artifact_kind)) + '</code></p>';
    }

    if (data.claim_boundary) {
      html += '<p><strong>claim_boundary:</strong> <code>' + csvEscape(String(data.claim_boundary)) + '</code></p>';
    }
    if (data.candidate_only !== undefined) {
      html += '<p><strong>candidate_only:</strong> <code>' + csvEscape(String(data.candidate_only)) + '</code></p>';
    }
    if (data.app_owned_apply !== undefined) {
      html += '<p><strong>app_owned_apply:</strong> <code>' + csvEscape(String(data.app_owned_apply)) + '</code></p>';
    }

    if (data.proof_boundaries && data.proof_boundaries.length) {
      html += '<p><strong>proof_boundaries:</strong></p><ul class="proof-gap-list">';
      data.proof_boundaries.forEach(function(pb) {
        html += '<li>' + csvEscape(String(pb)) + '</li>';
      });
      html += '</ul>';
    }

    /* Safe summary only — raw payload is never rendered */
    if (data.summary || data.description) {
      html += '<p><strong>Summary (safe):</strong> ' + csvEscape(String(data.summary || data.description)) + '</p>';
    }

    /* Redacted safe preview of remaining safe fields */
    var safeFields = {};
    var skipKeys = ['summary', 'description', 'candidate_id', 'id', 'session_id', 'status',
                    'artifact_kind', 'claim_boundary', 'candidate_only', 'app_owned_apply', 'proof_boundaries'];
    Object.keys(data).forEach(function(k) {
      if (skipKeys.indexOf(k) === -1) {
        safeFields[k] = csvRedactSensitive(k, data[k]);
      }
    });
    if (Object.keys(safeFields).length > 0) {
      html += '<p class="muted"><em>Additional fields (redacted where sensitive):</em></p>';
      html += csvSafeRenderObject(safeFields);
    }

    html += '</div>';
    html += '<p class="csv-not-applied-warning">This candidate is <strong>not applied truth</strong>. App owns apply.</p>';
    html += '<p class="boundary-note">No apply action. No external send. Raw sensitive payloads not displayed.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = csvBoundaryBanner() + csvNotAppliedWarning();
    html += '<p class="api-error">Candidate data unavailable: ' + csvEscape(e.message) + '</p>';
    html += '<div class="csv-fixture-placeholder">';
    html += '<p class="boundary-note">Candidates endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><strong>Proof gap:</strong> full_candidate_backend_coverage not proven.</p>';
    html += '<p>To query a candidate: <code>GET ' + csvEscape(CSV_API_BASE) + '/v1/candidates/{candidate_id}</code></p>';
    html += csvSafeRenderObject({
      candidate_id: '(fixture-placeholder)',
      status: 'unknown',
      candidate_only: true,
      app_owned_apply: true,
      claim_boundary: CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY,
      note: 'Candidates backend not available — proof gap recorded'
    });
    html += '</div>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Store Metadata View                                                  */
/* Metadata-first. No raw records. No mutation controls.               */
/* ------------------------------------------------------------------ */
function loadStoreMetadataView() {
  var container = document.getElementById('csv-store-content');
  if (!container) { return; }

  container.innerHTML = csvBoundaryBanner('metadata-only') + csvNotAppliedWarning() +
    '<p class="loading">Loading store metadata…</p>';

  /* Store APIs are not assumed — show metadata-first placeholder */
  /* No bulk store list endpoint is invented — document as proof gap */
  var html = csvBoundaryBanner('metadata-only') + csvNotAppliedWarning();
  html += '<div class="csv-store-record">';
  html += '<p class="boundary-note"><strong>Store view is read-only and metadata-first.</strong></p>';
  html += '<p class="boundary-note">No mutation controls. No raw record display. No store write actions.</p>';

  /* Attempt to fetch store status via /v1/status which may include store info */
  csvFetch('/v1/status').then(function(data) {
    var storeStatus = data.store_status || data.store || null;
    var storeCount = data.store_record_count || data.record_count || null;
    var storeCategories = data.store_categories || data.categories || null;
    var storeMeta = data.store_metadata || data.store_meta || null;

    var inner = csvBoundaryBanner('metadata-only') + csvNotAppliedWarning();
    inner += '<div class="csv-store-record">';
    inner += '<p class="boundary-note">Store view is read-only and metadata-first. No mutation controls.</p>';
    inner += '<span class="badge">readonly</span>';

    if (storeStatus) {
      var cls2 = (storeStatus === 'ok') ? 'status-ok' : 'status-warn';
      inner += '<p><strong>Store status:</strong> <span class="' + cls2 + '">' + csvEscape(String(storeStatus)) + '</span></p>';
    } else {
      inner += '<p class="status-warn">Store status: not available from /v1/status</p>';
    }
    if (storeCount !== null) {
      inner += '<p><strong>Record count:</strong> ' + csvEscape(String(storeCount)) + '</p>';
    }
    if (storeCategories) {
      inner += '<p><strong>Categories:</strong> ' + csvEscape(JSON.stringify(storeCategories)) + '</p>';
    }
    if (storeMeta) {
      inner += '<p><strong>Store metadata (safe):</strong></p>';
      inner += csvSafeRenderObject(storeMeta);
    }

    inner += '<p class="boundary-note"><strong>Proof gap:</strong> full_store_backend_coverage not proven.</p>';
    inner += '<p class="boundary-note">Store mutation not available through this viewer.</p>';
    inner += '<p class="boundary-note">Raw sensitive payloads are not displayed.</p>';
    inner += '</div>';
    container.innerHTML = inner;
  }).catch(function(e) {
    var inner = csvBoundaryBanner('metadata-only') + csvNotAppliedWarning();
    inner += '<p class="api-error">Store metadata unavailable: ' + csvEscape(e.message) + '</p>';
    inner += '<div class="csv-fixture-placeholder">';
    inner += '<p class="boundary-note">Store APIs not available — showing fixture-compatible placeholder.</p>';
    inner += '<p><strong>Proof gap:</strong> full_store_backend_coverage not proven.</p>';
    inner += csvSafeRenderObject({
      store_status: '(fixture-placeholder)',
      record_count: 0,
      categories: [],
      readonly: true,
      candidate_only: true,
      claim_boundary: CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY,
      note: 'Store backend not available — proof gap recorded'
    });
    inner += '</div>';
    container.innerHTML = inner;
  });
}

/* ------------------------------------------------------------------ */
/* Proof Gap Viewer                                                     */
/* Displays proof gaps. Does NOT close, resolve, or certify gaps.      */
/* ------------------------------------------------------------------ */
function loadProofGapViewer() {
  var container = document.getElementById('csv-proof-gaps-content');
  if (!container) { return; }

  container.innerHTML = csvBoundaryBanner('proof-gaps') +
    '<p class="loading">Loading proof gaps…</p>';

  csvFetch('/v1/proof-gaps').then(function(data) {
    var gaps = data.proof_gaps || data.gaps || [];
    var boundaries = data.proof_boundaries || [];
    var knownNonProofs = data.known_non_proofs || [];
    var missing = data.missing_capabilities || [];
    var nextPr = data.next_recommended_pr || null;

    var html = csvBoundaryBanner('proof-gaps');
    html += '<p class="boundary-note">Displaying proof gaps does not close them. Viewer-only.</p>';

    if (gaps.length === 0) {
      html += '<p class="status-warn">No proof gaps reported by API — gaps may still exist locally.</p>';
    } else {
      html += '<p>Known proof gaps (' + gaps.length + '):</p><ul class="proof-gap-list">';
      gaps.forEach(function(g) {
        html += '<li>' + csvEscape(typeof g === 'string' ? g : JSON.stringify(g)) + '</li>';
      });
      html += '</ul>';
    }

    /* Known non-proofs */
    var allNonProofs = CANDIDATE_STORE_VIEWER_NOT_PROVEN.concat(knownNonProofs.filter(function(np) {
      return CANDIDATE_STORE_VIEWER_NOT_PROVEN.indexOf(np) === -1;
    }));
    html += '<p><strong>Known not-proven (this viewer):</strong></p><ul class="proof-gap-list">';
    allNonProofs.forEach(function(np) {
      html += '<li>' + csvEscape(String(np)) + '</li>';
    });
    html += '</ul>';

    if (boundaries.length) {
      html += '<p><strong>Proof boundaries:</strong></p><ul class="proof-gap-list">';
      boundaries.forEach(function(b) {
        html += '<li>' + csvEscape(typeof b === 'string' ? b : JSON.stringify(b)) + '</li>';
      });
      html += '</ul>';
    }

    if (missing.length) {
      html += '<p><strong>Missing capabilities:</strong></p><ul class="proof-gap-list">';
      missing.forEach(function(m) {
        html += '<li>' + csvEscape(typeof m === 'string' ? m : JSON.stringify(m)) + '</li>';
      });
      html += '</ul>';
    }

    if (nextPr) {
      html += '<p><strong>Next recommended PR:</strong> ' + csvEscape(String(nextPr)) + '</p>';
    }

    html += '<p class="boundary-note">claim_boundary: <code>' + csvEscape(CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY) + '</code></p>';
    html += '<p class="boundary-note">Proof gaps displayed here are not resolved by being displayed.</p>';
    html += '<p class="boundary-note">No app apply. No external send. No store mutation. Candidate-only.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = csvBoundaryBanner('proof-gaps');
    html += '<p class="api-error">Proof gaps unavailable from API: ' + csvEscape(e.message) + '</p>';
    html += '<p class="boundary-note">Displaying proof gaps does not close them.</p>';
    html += '<p><strong>Known not-proven (this viewer):</strong></p><ul class="proof-gap-list">';
    CANDIDATE_STORE_VIEWER_NOT_PROVEN.forEach(function(np) {
      html += '<li>' + csvEscape(np) + '</li>';
    });
    html += '</ul>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Candidate Store Viewer initialisation                               */
/* ------------------------------------------------------------------ */
function initCandidateStoreViewer() {
  loadSessionsView(null);
  loadCandidateView(null);
  loadStoreMetadataView();
  loadProofGapViewer();
}

document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('csv-sessions-content') ||
      document.getElementById('csv-candidate-content') ||
      document.getElementById('csv-store-content') ||
      document.getElementById('csv-proof-gaps-content')) {
    initCandidateStoreViewer();
  }
});

/* No apply, applyCandidate, externalSend, store-write, store-delete, raw-payload-reveal,
 * or provider credential methods defined in this file.
 * Candidate-only. Not applied truth. No store mutation.
 */
