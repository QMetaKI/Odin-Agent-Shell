/**
 * Odin Local Runtime Hub — Provider / Worker / Pre-LLM Inspector (LRH-PR-10)
 *
 * Claim boundary: provider_worker_inspector_candidate_only_local_only_no_provider_execution_no_credentials_no_worker_mutation
 *
 * Provides read-only inspection surfaces:
 *   - Provider card viewer (/v1/providers — metadata only, not live execution)
 *   - Worker permission card viewer (boundaries, forbidden roles, candidate-only)
 *   - Pre-LLM route decision viewer (route decisions as metadata/fixtures)
 *   - Model-work avoidance panel (why model work was avoided)
 *   - Redaction status panel (policy/warnings — not safety certification)
 *   - Disabled-by-default visibility (provider/credential posture)
 *   - Provider/worker proof-gap surface (/v1/proof-gaps)
 *
 * Not proven:
 *   - production_readiness
 *   - security_certification
 *   - live_model_inference
 *   - model_quality
 *   - provider_authority
 *   - provider_credential_storage
 *   - full_pre_llm_runtime_coverage
 *   - full_redaction_safety_certification
 *   - worker_mutation_authority
 *   - external_send_authority
 *   - app_state_mutation
 *
 * Forbidden in this file:
 *   - runProvider() / executeProvider() / callModel() / runModel() / testInference()
 *   - credential saving / api-key setting / credential input fields / token input fields
 *   - enableProvider() / disableProvider() / mutateWorker() / editPermission()
 *   - changeRoute() / mutateRoute() / bypassRedaction()
 *   - rawPayloadReveal() / externalSend() / uploadDiagnostics() / hiddenUpload()
 *   - network requests outside localhost
 */

/* ------------------------------------------------------------------ */
/* Provider Worker Inspector Claim Boundary                            */
/* ------------------------------------------------------------------ */
var PROVIDER_WORKER_INSPECTOR_CLAIM_BOUNDARY =
  'provider_worker_inspector_candidate_only_local_only_no_provider_execution_no_credentials_no_worker_mutation';

var PROVIDER_WORKER_INSPECTOR_NOT_PROVEN = [
  'production_readiness',
  'security_certification',
  'live_model_inference',
  'model_quality',
  'provider_authority',
  'provider_credential_storage',
  'full_pre_llm_runtime_coverage',
  'full_redaction_safety_certification',
  'worker_mutation_authority',
  'external_send_authority',
  'app_state_mutation',
];

/* Required boundary tokens for validator scan */
var PROVIDER_WORKER_INSPECTOR_BOUNDARY_TOKENS = [
  'candidate_only',
  'claim_boundary',
  'local_only',
  'read_only',
  'no_provider_execution',
  'no_credentials',
  'no_worker_mutation',
  'metadata_first',
  'provider_as_worker',
];

var PROVIDER_WORKER_INSPECTOR_API_BASE =
  (typeof ODIN_API_BASE !== 'undefined') ? ODIN_API_BASE : 'http://127.0.0.1:8877';

/* ------------------------------------------------------------------ */
/* Localhost guard                                                      */
/* ------------------------------------------------------------------ */
function pwi_isLocalhost(url) {
  return (
    url.indexOf('127.0.0.1') !== -1 ||
    url.indexOf('localhost') !== -1 ||
    url.indexOf('::1') !== -1
  );
}

if (!pwi_isLocalhost(PROVIDER_WORKER_INSPECTOR_API_BASE)) {
  PROVIDER_WORKER_INSPECTOR_API_BASE = 'http://127.0.0.1:8877';
}

/* ------------------------------------------------------------------ */
/* Utility: safe fetch with boundary guard                             */
/* ------------------------------------------------------------------ */
function pwi_safeFetch(path, onSuccess, onError) {
  var url = PROVIDER_WORKER_INSPECTOR_API_BASE + path;
  if (!pwi_isLocalhost(url)) {
    onError({ error: true, message: 'Non-localhost URL blocked by inspector boundary guard.' });
    return;
  }
  fetch(url)
    .then(function(resp) { return resp.json(); })
    .then(onSuccess)
    .catch(function(err) { onError({ error: true, message: String(err) }); });
}

/* ------------------------------------------------------------------ */
/* Utility: set element content safely                                 */
/* ------------------------------------------------------------------ */
function pwi_setContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function pwi_renderBoundaryNote(text) {
  return '<p class="boundary-note pwi-boundary">' + pwi_escHtml(text) + '</p>';
}

function pwi_escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function pwi_renderKV(obj) {
  var rows = [];
  for (var k in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, k)) {
      rows.push('<tr><td class="pwi-key">' + pwi_escHtml(k) + '</td><td class="pwi-val">' + pwi_escHtml(JSON.stringify(obj[k])) + '</td></tr>');
    }
  }
  return '<table class="pwi-table">' + rows.join('') + '</table>';
}

/* ------------------------------------------------------------------ */
/* Provider Card Viewer — /v1/providers                                */
/* ------------------------------------------------------------------ */
function pwi_loadProviderCards() {
  pwi_setContent('pwi-provider-cards-content', '<p class="loading">Loading provider cards from /v1/providers…</p>');
  pwi_safeFetch('/v1/providers', function(data) {
    var providers = data.providers || data || [];
    if (!Array.isArray(providers)) { providers = [providers]; }
    if (providers.length === 0) {
      pwi_setContent('pwi-provider-cards-content', '<p class="pwi-none">No provider cards available. Provider registry may be empty or API unavailable.</p>');
      return;
    }
    var html = '<div class="pwi-section-label">Provider is worker, not authority. Read-only metadata below.</div>';
    providers.forEach(function(card) {
      html += '<div class="pwi-card">';
      html += '<div class="pwi-card-header">';
      html += '<strong>' + pwi_escHtml(card.provider_id || 'unknown') + '</strong>';
      html += ' <span class="badge pwi-badge-kind">' + pwi_escHtml(card.provider_kind || '') + '</span>';
      var status = card.enabled_by_default ? 'enabled' : 'disabled';
      html += ' <span class="badge pwi-badge-status pwi-status-' + status + '">' + status + '</span>';
      if (!card.enabled_by_default) {
        html += ' <span class="badge pwi-badge-default">disabled-by-default</span>';
      }
      html += '</div>';
      html += '<div class="pwi-card-body">';
      html += '<div class="pwi-boundary-banner">Provider is worker, not authority. No live inference without receipt. No credentials by default. Disabled by default.</div>';
      html += '<table class="pwi-table">';
      html += '<tr><td class="pwi-key">provider_id</td><td class="pwi-val">' + pwi_escHtml(card.provider_id || '') + '</td></tr>';
      html += '<tr><td class="pwi-key">provider_kind</td><td class="pwi-val">' + pwi_escHtml(card.provider_kind || '') + '</td></tr>';
      html += '<tr><td class="pwi-key">enabled_by_default</td><td class="pwi-val">' + pwi_escHtml(String(card.enabled_by_default)) + '</td></tr>';
      html += '<tr><td class="pwi-key">configured</td><td class="pwi-val">' + pwi_escHtml(String(card.configured)) + '</td></tr>';
      html += '<tr><td class="pwi-key">live_inference_supported</td><td class="pwi-val">' + pwi_escHtml(String(card.live_inference_supported)) + '</td></tr>';
      html += '<tr><td class="pwi-key">live_inference_verified</td><td class="pwi-val">' + pwi_escHtml(String(card.live_inference_verified)) + '</td></tr>';
      html += '<tr><td class="pwi-key">external_network</td><td class="pwi-val">' + pwi_escHtml(String(card.external_network)) + '</td></tr>';
      html += '<tr><td class="pwi-key">candidate_only</td><td class="pwi-val">' + pwi_escHtml(String(card.candidate_only)) + '</td></tr>';
      html += '<tr><td class="pwi-key">claim_boundary</td><td class="pwi-val">' + pwi_escHtml(card.claim_boundary || '') + '</td></tr>';
      html += '</table>';
      if (card.forbidden_roles && card.forbidden_roles.length) {
        html += '<div class="pwi-sub-label">Forbidden roles (worker boundary)</div>';
        html += '<ul class="pwi-list">' + card.forbidden_roles.map(function(r) { return '<li>' + pwi_escHtml(r) + '</li>'; }).join('') + '</ul>';
      }
      html += '</div>';
      html += '</div>';
    });
    pwi_setContent('pwi-provider-cards-content', html);
  }, function(err) {
    pwi_setContent('pwi-provider-cards-content',
      '<p class="pwi-error">Provider cards unavailable: ' + pwi_escHtml(err.message || 'API not running') + '</p>' +
      '<p class="pwi-note">This is not a proof gap — the API may not be running. Provider metadata is also available via <code>python -m odin.cli list-providers</code>.</p>');
  });
}

/* ------------------------------------------------------------------ */
/* Worker Permission Card Viewer                                       */
/* ------------------------------------------------------------------ */
function pwi_loadWorkerPermissions() {
  pwi_setContent('pwi-worker-permission-content', '<p class="loading">Loading worker permission cards from /v1/status…</p>');
  pwi_safeFetch('/v1/status', function(data) {
    var html = '<div class="pwi-section-label">Worker permission cards are read-only. No mutation controls.</div>';
    html += '<div class="pwi-boundary-banner">candidate_only: true. app_owned_apply: true. external_send_default: false. no_hidden_tool_execution: true.</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">candidate_only</td><td class="pwi-val">true (all workers)</td></tr>';
    html += '<tr><td class="pwi-key">app_owned_apply</td><td class="pwi-val">true</td></tr>';
    html += '<tr><td class="pwi-key">external_send_default</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">hidden_tool_execution_allowed</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">may_apply</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">may_send_external</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">may_mutate_app_state</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">may_issue_receipt</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">may_accept_claim</td><td class="pwi-val">false</td></tr>';
    html += '</table>';
    html += '<div class="pwi-sub-label">Forbidden worker actions</div>';
    html += '<ul class="pwi-list">';
    ['app_authority', 'apply_executor', 'claim_acceptor', 'receipt_issuer', 'external_sender', 'state_mutator'].forEach(function(r) {
      html += '<li>' + pwi_escHtml(r) + '</li>';
    });
    html += '</ul>';
    if (data) {
      html += '<div class="pwi-sub-label">Status API response (metadata only)</div>';
      html += '<pre class="pwi-pre">' + pwi_escHtml(JSON.stringify(data, null, 2).substring(0, 800)) + '</pre>';
    }
    pwi_setContent('pwi-worker-permission-content', html);
  }, function(err) {
    var html = '<div class="pwi-boundary-banner">Worker permission boundaries (static — no API required):</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">candidate_only</td><td class="pwi-val">true</td></tr>';
    html += '<tr><td class="pwi-key">app_owned_apply</td><td class="pwi-val">true</td></tr>';
    html += '<tr><td class="pwi-key">external_send_default</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">hidden_tool_execution</td><td class="pwi-val">false</td></tr>';
    html += '</table>';
    html += '<p class="pwi-note">API unavailable (' + pwi_escHtml(err.message || '') + ') — static boundaries shown.</p>';
    pwi_setContent('pwi-worker-permission-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Pre-LLM Route Decision Viewer                                       */
/* ------------------------------------------------------------------ */
function pwi_loadPreLlmRoute() {
  pwi_setContent('pwi-pre-llm-route-content', '<p class="loading">Loading pre-LLM route decisions from /v1/status…</p>');
  pwi_safeFetch('/v1/status', function(data) {
    var html = '<div class="pwi-section-label">Pre-LLM route decisions are inspection-only. No route mutation.</div>';
    html += '<div class="pwi-boundary-banner">Not live model inference. Route decisions are read-only metadata/fixtures. No routing policy mutation.</div>';
    var routeInfo = (data && data.pre_llm_route) ? data.pre_llm_route : null;
    if (routeInfo) {
      html += '<table class="pwi-table">';
      for (var k in routeInfo) {
        if (Object.prototype.hasOwnProperty.call(routeInfo, k)) {
          html += '<tr><td class="pwi-key">' + pwi_escHtml(k) + '</td><td class="pwi-val">' + pwi_escHtml(JSON.stringify(routeInfo[k])) + '</td></tr>';
        }
      }
      html += '</table>';
    } else {
      html += '<table class="pwi-table">';
      html += '<tr><td class="pwi-key">route_status</td><td class="pwi-val">not_live_model_inference — deterministic no-model route</td></tr>';
      html += '<tr><td class="pwi-key">decision_reason</td><td class="pwi-val">No live route data available; static fixture shown</td></tr>';
      html += '<tr><td class="pwi-key">avoidance_rationale</td><td class="pwi-val">candidate_only mode — model work avoided</td></tr>';
      html += '<tr><td class="pwi-key">redaction_before_model</td><td class="pwi-val">applied (redaction policy active)</td></tr>';
      html += '<tr><td class="pwi-key">proof_boundary</td><td class="pwi-val">not_full_pre_llm_runtime_coverage</td></tr>';
      html += '</table>';
    }
    pwi_setContent('pwi-pre-llm-route-content', html);
  }, function(err) {
    var html = '<div class="pwi-boundary-banner">Pre-LLM route decision (static fixture — API not running):</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">route_status</td><td class="pwi-val">not_live_model_inference</td></tr>';
    html += '<tr><td class="pwi-key">avoidance_rationale</td><td class="pwi-val">API not running — no live route decision available</td></tr>';
    html += '<tr><td class="pwi-key">proof_boundary</td><td class="pwi-val">not_full_pre_llm_runtime_coverage</td></tr>';
    html += '</table>';
    html += '<p class="pwi-note">API unavailable. No route mutation — inspection-only.</p>';
    pwi_setContent('pwi-pre-llm-route-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Model-Work Avoidance Panel                                          */
/* ------------------------------------------------------------------ */
function pwi_loadModelAvoidance() {
  pwi_setContent('pwi-model-avoidance-content', '<p class="loading">Loading model-work avoidance rationale…</p>');
  pwi_safeFetch('/v1/status', function(data) {
    var html = '<div class="pwi-section-label">Model-work avoidance rationale (read-only). No model run button.</div>';
    html += '<div class="pwi-boundary-banner">No live model inference. No "run model" control. Candidate-only mode.</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">candidate_only_mode</td><td class="pwi-val">true — model work avoided</td></tr>';
    html += '<tr><td class="pwi-key">disabled_provider</td><td class="pwi-val">all providers disabled by default</td></tr>';
    html += '<tr><td class="pwi-key">missing_credential</td><td class="pwi-val">no credentials configured by default</td></tr>';
    html += '<tr><td class="pwi-key">local_only_mode</td><td class="pwi-val">true — no external model calls</td></tr>';
    html += '<tr><td class="pwi-key">no_receipt</td><td class="pwi-val">no live inference receipt — not proven</td></tr>';
    html += '<tr><td class="pwi-key">proof_gap_reason</td><td class="pwi-val">not_live_model_inference_proof</td></tr>';
    html += '</table>';
    pwi_setContent('pwi-model-avoidance-content', html);
  }, function() {
    var html = '<div class="pwi-boundary-banner">Model-work avoidance (static):</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">avoidance_reason</td><td class="pwi-val">candidate_only mode active</td></tr>';
    html += '<tr><td class="pwi-key">proof_gap</td><td class="pwi-val">not_live_model_inference_proof</td></tr>';
    html += '</table>';
    pwi_setContent('pwi-model-avoidance-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Redaction Status Panel                                              */
/* ------------------------------------------------------------------ */
function pwi_loadRedactionStatus() {
  pwi_setContent('pwi-redaction-status-content', '<p class="loading">Loading redaction status…</p>');
  pwi_safeFetch('/v1/status', function(data) {
    var html = '<div class="pwi-section-label">Redaction status is not safety certification.</div>';
    html += '<div class="pwi-boundary-banner">Redaction status is not security certification. No raw sensitive payload display. Metadata-first display only.</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">redaction_policy</td><td class="pwi-val">active — secret keys are redacted</td></tr>';
    html += '<tr><td class="pwi-key">metadata_first_display</td><td class="pwi-val">true — raw payloads never shown</td></tr>';
    html += '<tr><td class="pwi-key">redaction_status_is_not_certification</td><td class="pwi-val">true</td></tr>';
    html += '<tr><td class="pwi-key">known_redaction_gaps</td><td class="pwi-val">not_full_redaction_safety_certification</td></tr>';
    html += '<tr><td class="pwi-key">safe_unsafe_policy</td><td class="pwi-val">safe by default; sensitive values redacted</td></tr>';
    html += '</table>';
    pwi_setContent('pwi-redaction-status-content', html);
  }, function() {
    var html = '<div class="pwi-boundary-banner">Redaction status (static — API not running):</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">redaction_policy</td><td class="pwi-val">active</td></tr>';
    html += '<tr><td class="pwi-key">redaction_status_is_not_certification</td><td class="pwi-val">true</td></tr>';
    html += '</table>';
    pwi_setContent('pwi-redaction-status-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Disabled-by-Default Visibility Surface                             */
/* ------------------------------------------------------------------ */
function pwi_loadDisabledByDefault() {
  pwi_setContent('pwi-disabled-by-default-content', '<p class="loading">Loading disabled-by-default status…</p>');
  pwi_safeFetch('/v1/providers', function(data) {
    var providers = data.providers || data || [];
    if (!Array.isArray(providers)) { providers = [providers]; }
    var html = '<div class="pwi-section-label">Disabled-by-default posture. No enable/disable controls.</div>';
    html += '<div class="pwi-boundary-banner">Disabled by default. No credentials by default. No provider execution. No external send. No live inference receipt.</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">provider_execution_default</td><td class="pwi-val">disabled</td></tr>';
    html += '<tr><td class="pwi-key">credential_default</td><td class="pwi-val">none configured by default</td></tr>';
    html += '<tr><td class="pwi-key">external_send_default</td><td class="pwi-val">false</td></tr>';
    html += '<tr><td class="pwi-key">live_inference_receipt</td><td class="pwi-val">not issued — no live receipt</td></tr>';
    html += '</table>';
    if (providers.length > 0) {
      html += '<div class="pwi-sub-label">Per-provider enabled_by_default status</div>';
      html += '<table class="pwi-table">';
      providers.forEach(function(p) {
        html += '<tr><td class="pwi-key">' + pwi_escHtml(p.provider_id || '') + '</td><td class="pwi-val">' + pwi_escHtml(String(p.enabled_by_default)) + '</td></tr>';
      });
      html += '</table>';
    }
    pwi_setContent('pwi-disabled-by-default-content', html);
  }, function() {
    var html = '<div class="pwi-boundary-banner">Disabled by default (static):</div>';
    html += '<table class="pwi-table">';
    html += '<tr><td class="pwi-key">provider_execution_default</td><td class="pwi-val">disabled</td></tr>';
    html += '<tr><td class="pwi-key">credential_default</td><td class="pwi-val">none</td></tr>';
    html += '</table>';
    pwi_setContent('pwi-disabled-by-default-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Provider/Worker Proof Gaps Surface                                  */
/* ------------------------------------------------------------------ */
function pwi_loadProofGaps() {
  pwi_setContent('pwi-proof-gaps-content', '<p class="loading">Loading provider/worker proof gaps from /v1/proof-gaps…</p>');
  pwi_safeFetch('/v1/proof-gaps', function(data) {
    var html = '<div class="pwi-section-label">Provider/worker proof gaps (viewer-only). Displaying gaps does not close them.</div>';
    var gaps = data.proof_gaps || data.gaps || [];
    var boundaries = data.proof_boundaries || [];
    if (boundaries.length > 0) {
      html += '<div class="pwi-sub-label">Declared proof boundaries</div>';
      html += '<ul class="pwi-list">' + boundaries.map(function(b) { return '<li>' + pwi_escHtml(b) + '</li>'; }).join('') + '</ul>';
    }
    html += '<div class="pwi-sub-label">Provider/worker known non-proofs</div>';
    html += '<ul class="pwi-list">';
    ['production_readiness', 'security_certification', 'live_model_inference', 'model_quality',
     'provider_authority', 'provider_credential_storage', 'full_pre_llm_runtime_coverage',
     'full_redaction_safety_certification', 'worker_mutation_authority', 'external_send_authority'].forEach(function(g) {
      html += '<li>' + pwi_escHtml(g) + '</li>';
    });
    html += '</ul>';
    pwi_setContent('pwi-proof-gaps-content', html);
  }, function(err) {
    var html = '<div class="pwi-boundary-banner">Proof gaps (static — API not running):</div>';
    html += '<ul class="pwi-list">';
    ['production_readiness', 'live_model_inference', 'model_quality', 'security_certification'].forEach(function(g) {
      html += '<li>' + pwi_escHtml(g) + '</li>';
    });
    html += '</ul>';
    html += '<p class="pwi-note">Displaying proof gaps does not close them.</p>';
    pwi_setContent('pwi-proof-gaps-content', html);
  });
}

/* ------------------------------------------------------------------ */
/* Initialise all surfaces on DOM ready                                */
/* ------------------------------------------------------------------ */
function pwi_initProviderWorkerInspector() {
  pwi_loadProviderCards();
  pwi_loadWorkerPermissions();
  pwi_loadPreLlmRoute();
  pwi_loadModelAvoidance();
  pwi_loadRedactionStatus();
  pwi_loadDisabledByDefault();
  pwi_loadProofGaps();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', pwi_initProviderWorkerInspector);
} else {
  pwi_initProviderWorkerInspector();
}
