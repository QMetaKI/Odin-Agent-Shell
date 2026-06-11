/**
 * Odin Local Runtime Hub — Universal Work Playground (LRH-PR-11)
 *
 * Claim boundary: uwp_candidate_only_local_only_no_apply_no_external_send_no_shell_no_provider
 *
 * Provides a local-only safe demo playground with:
 *   - Local-only Universal Work form (safe bounded fields only)
 *   - Safe demo work packet fixtures (candidate-only)
 *   - Candidate artifact result panel (not applied truth)
 *   - Proof boundary panel (no proof closure)
 *   - Validation/status panel (local receipt only)
 *   - Provider/worker boundary context (read-only, from PR-10)
 *
 * Not proven:
 *   - production_readiness
 *   - security_certification
 *   - live_model_inference
 *   - model_quality
 *   - app_apply_authority
 *   - external_send_authority
 *   - arbitrary_shell_execution
 *   - provider_execution
 *   - credential_handling
 *   - full_live_universal_work_backend_coverage
 *   - external_app_bridge
 *
 * Forbidden in this file:
 *   - No app-apply controls, no candidate-apply triggers.
 *   - No external-send or upload controls.
 *   - No shell/command/script execution controls.
 *   - No provider execution, model calls, or inference triggers.
 *   - No credential inputs, no api-key inputs, no token inputs.
 *   - No remote URL or webhook inputs.
 *   - No app-state mutation.
 *   - No network requests outside localhost.
 */

/* ------------------------------------------------------------------ */
/* Universal Work Playground Claim Boundary                            */
/* ------------------------------------------------------------------ */
var UWP_CLAIM_BOUNDARY =
  'uwp_candidate_only_local_only_no_apply_no_external_send_no_shell_no_provider_no_credentials';

var UWP_PROOF_BOUNDARIES = [
  'not_production_readiness_certification',
  'not_security_certification',
  'not_live_model_inference_proof',
  'not_model_quality_proof',
  'not_app_apply_proof',
  'not_app_state_mutation_proof',
  'not_external_send_authority_proof',
  'not_arbitrary_shell_execution_proof',
  'not_provider_execution_proof',
  'not_credential_handling_proof',
  'not_full_live_universal_work_backend_coverage',
  'not_external_app_bridge_proof',
  'candidate_result_not_applied_truth',
];

var UWP_KNOWN_NON_PROOFS = [
  'production_readiness',
  'live_model_inference',
  'app_state_mutation',
  'external_send_authority',
  'app_apply_authority',
  'arbitrary_shell_execution',
  'provider_execution',
  'credential_handling',
  'security_certification',
  'model_quality',
  'full_live_universal_work_backend_coverage',
  'external_app_bridge',
];

/* Required boundary tokens for validator scan */
var UWP_BOUNDARY_FLAGS = {
  candidate_only: true,
  claim_boundary: UWP_CLAIM_BOUNDARY,
  local_only: true,
  read_only: false,
  playground_only: true,
  safe_demo_only: true,
  no_app_apply: true,
  no_external_send: true,
  no_arbitrary_shell_execution: true,
  no_provider_execution: true,
  no_credentials: true,
  not_applied_truth: true,
  metadata_first: true,
  provider_as_worker_not_authority: true,
  disabled_by_default: true,
  proof_boundaries: UWP_PROOF_BOUNDARIES,
  known_non_proofs: UWP_KNOWN_NON_PROOFS,
};

var UWP_API_BASE =
  (typeof ODIN_API_BASE !== 'undefined') ? ODIN_API_BASE : 'http://127.0.0.1:8877';

/* ------------------------------------------------------------------ */
/* Embedded safe demo fixtures (local-only, no network fetch)          */
/* ------------------------------------------------------------------ */
var UWP_SAFE_DEMO_WORK_PACKET = {
  artifact_kind: 'odin_universal_work_playground_safe_demo_packet',
  candidate_only: true,
  local_only: true,
  external_send: false,
  app_apply: false,
  arbitrary_shell_execution: false,
  provider_execution: false,
  credential_required: false,
  claim_boundary: UWP_CLAIM_BOUNDARY,
  work_kind: 'safe_demo',
  title: 'Safe Demo Universal Work',
  intent: 'Demonstrate bounded Universal Work packet structure with visible proof boundaries.',
  input_text: 'Safe demo input. No shell commands, provider calls, or app state changes.',
  constraints: [
    'candidate_only',
    'local_only',
    'no_external_send',
    'no_app_apply',
    'no_arbitrary_shell_execution',
    'no_provider_execution',
    'no_credentials',
  ],
  expected_output_kind: 'candidate_artifact',
  proof_boundaries: UWP_PROOF_BOUNDARIES,
  known_non_proofs: UWP_KNOWN_NON_PROOFS,
};

var UWP_SAFE_DEMO_CANDIDATE_RESULT = {
  artifact_kind: 'odin_universal_work_playground_safe_demo_candidate_result',
  candidate_artifact_id: 'UWP-DEMO-CANDIDATE-001',
  source_work_packet_id: 'UWP-DEMO-PACKET-001',
  candidate_only: true,
  applied_truth: false,
  app_state_mutated: false,
  external_send: false,
  candidate_kind: 'safe_demo_candidate',
  candidate_status: 'pending_app_review',
  candidate_summary: 'Safe demo candidate artifact — not applied truth, not final state, not executed.',
  claim_boundary: 'uwp_candidate_result_candidate_only_not_applied_truth_no_app_state_mutation',
  proof_boundaries: UWP_PROOF_BOUNDARIES,
  known_non_proofs: UWP_KNOWN_NON_PROOFS,
};

/* ------------------------------------------------------------------ */
/* Localhost guard                                                      */
/* ------------------------------------------------------------------ */
function uwp_isLocalhost(url) {
  return (
    url.indexOf('127.0.0.1') !== -1 ||
    url.indexOf('localhost') !== -1 ||
    url.indexOf('::1') !== -1
  );
}

function uwp_safeFetch(path, opts) {
  var url = UWP_API_BASE + path;
  if (!uwp_isLocalhost(url)) {
    return Promise.reject(new Error('UWP: non-localhost URL blocked: ' + url));
  }
  return fetch(url, opts || {});
}

/* ------------------------------------------------------------------ */
/* DOM helpers                                                         */
/* ------------------------------------------------------------------ */
function uwp_setContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function uwp_escape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ------------------------------------------------------------------ */
/* Universal Work form (safe bounded fields only)                      */
/* ------------------------------------------------------------------ */
function uwp_buildWorkForm() {
  return (
    '<form id="uwp-safe-demo-form">' +
    '<fieldset>' +
    '<legend>Safe Demo Universal Work — local-only, candidate-only</legend>' +
    '<p class="boundary-note">' +
    'This form submits a safe demo work packet only. ' +
    'No shell commands. No external sends. No app apply. No provider execution. No credentials. ' +
    'Candidate-only. Local-only. Safe demo only.' +
    '</p>' +
    '<div class="form-group">' +
    '<label for="uwp-work-kind">Work Kind</label>' +
    '<select id="uwp-work-kind" name="work_kind">' +
    '<option value="safe_demo" selected>safe_demo</option>' +
    '</select>' +
    '<span class="boundary-note">Safe demo kind only. No arbitrary execution kinds.</span>' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="uwp-title">Title</label>' +
    '<input type="text" id="uwp-title" name="title" maxlength="200" value="Safe Demo Universal Work" autocomplete="off">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="uwp-intent">Intent</label>' +
    '<input type="text" id="uwp-intent" name="intent" maxlength="500" value="Demonstrate bounded Universal Work packet structure." autocomplete="off">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="uwp-input-text">Input Text</label>' +
    '<textarea id="uwp-input-text" name="input_text" rows="3" maxlength="1000">Safe demo input. No shell commands, provider calls, or app state changes.</textarea>' +
    '</div>' +
    '<div class="form-group">' +
    '<label>Constraints (fixed — all safety boundaries enforced)</label>' +
    '<ul class="constraint-list">' +
    '<li><input type="checkbox" value="candidate_only" checked disabled> candidate_only</li>' +
    '<li><input type="checkbox" value="local_only" checked disabled> local_only</li>' +
    '<li><input type="checkbox" value="no_external_send" checked disabled> no_external_send</li>' +
    '<li><input type="checkbox" value="no_app_apply" checked disabled> no_app_apply</li>' +
    '<li><input type="checkbox" value="no_arbitrary_shell_execution" checked disabled> no_arbitrary_shell_execution</li>' +
    '<li><input type="checkbox" value="no_provider_execution" checked disabled> no_provider_execution</li>' +
    '<li><input type="checkbox" value="no_credentials" checked disabled> no_credentials</li>' +
    '</ul>' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="uwp-output-kind">Expected Output Kind</label>' +
    '<select id="uwp-output-kind" name="expected_output_kind">' +
    '<option value="candidate_artifact" selected>candidate_artifact</option>' +
    '</select>' +
    '</div>' +
    '<p class="boundary-note">' +
    'Candidate-only marker: true. Local-only marker: true. ' +
    'No external destination. No remote URL. No credentials by default.' +
    '</p>' +
    '<button type="submit" id="uwp-submit-btn" class="uwp-btn">Submit Safe Demo Work</button>' +
    '<p class="boundary-note">Submitting produces a fixture-backed candidate result. No app apply. No external send.</p>' +
    '</fieldset>' +
    '</form>'
  );
}

/* ------------------------------------------------------------------ */
/* Candidate result panel                                              */
/* ------------------------------------------------------------------ */
function uwp_showCandidateResult(result, source) {
  var sourceNote = (source === 'fixture')
    ? '<span class="badge badge-fixture">fixture-backed</span>'
    : '<span class="badge">local-api</span>';

  var proofList = (result.proof_boundaries || [])
    .map(function(p) { return '<li class="proof-item">' + uwp_escape(p) + '</li>'; })
    .join('');

  var nonProofList = (result.known_non_proofs || [])
    .map(function(p) { return '<li class="non-proof-item">' + uwp_escape(p) + '</li>'; })
    .join('');

  uwp_setContent('uwp-candidate-result-content',
    '<div class="candidate-result-panel">' +
    '<div class="candidate-header">' +
    '<span class="badge badge-candidate">CANDIDATE ONLY</span> ' +
    '<span class="badge badge-warning">NOT APPLIED TRUTH</span> ' +
    sourceNote +
    '</div>' +
    '<table class="result-table">' +
    '<tr><th>candidate_artifact_id</th><td>' + uwp_escape(result.candidate_artifact_id || '') + '</td></tr>' +
    '<tr><th>candidate_kind</th><td>' + uwp_escape(result.candidate_kind || '') + '</td></tr>' +
    '<tr><th>source_work_packet_id</th><td>' + uwp_escape(result.source_work_packet_id || '') + '</td></tr>' +
    '<tr><th>candidate_status</th><td>' + uwp_escape(result.candidate_status || '') + '</td></tr>' +
    '<tr><th>candidate_only</th><td>' + uwp_escape(String(result.candidate_only)) + '</td></tr>' +
    '<tr><th>applied_truth</th><td>' + uwp_escape(String(result.applied_truth)) + '</td></tr>' +
    '<tr><th>app_state_mutated</th><td>' + uwp_escape(String(result.app_state_mutated)) + '</td></tr>' +
    '<tr><th>external_send</th><td>' + uwp_escape(String(result.external_send)) + '</td></tr>' +
    '<tr><th>claim_boundary</th><td>' + uwp_escape(result.claim_boundary || '') + '</td></tr>' +
    '</table>' +
    '<p class="candidate-summary">' + uwp_escape(result.candidate_summary || '') + '</p>' +
    '<div class="proof-section"><h4>Proof Boundaries</h4><ul>' + proofList + '</ul></div>' +
    '<div class="non-proof-section"><h4>Known Non-Proofs</h4><ul>' + nonProofList + '</ul></div>' +
    '<p class="boundary-note">' +
    '<strong>Candidate-only.</strong> Candidate result is not applied truth. ' +
    'App owns apply. No app apply was performed. No external send was performed. ' +
    'No arbitrary shell execution. No provider execution. No credentials used. ' +
    'This does not prove production readiness. This does not prove model quality.' +
    '</p>' +
    '</div>'
  );
}

/* ------------------------------------------------------------------ */
/* Proof boundary panel                                                */
/* ------------------------------------------------------------------ */
function uwp_showProofPanel() {
  var proofList = UWP_PROOF_BOUNDARIES
    .map(function(p) { return '<li class="proof-item">' + uwp_escape(p) + '</li>'; })
    .join('');
  var nonProofList = UWP_KNOWN_NON_PROOFS
    .map(function(p) { return '<li class="non-proof-item">' + uwp_escape(p) + '</li>'; })
    .join('');

  uwp_setContent('uwp-proof-boundary-content',
    '<div class="proof-boundary-panel">' +
    '<p class="boundary-note">' +
    '<strong>Proof Boundary Panel.</strong> ' +
    'Displaying proof boundaries does not close the proof gaps.' +
    '</p>' +
    '<div class="proof-grid">' +
    '<div class="proof-col">' +
    '<h4>Proof Boundaries (what this cannot prove)</h4>' +
    '<ul>' + proofList + '</ul>' +
    '</div>' +
    '<div class="proof-col">' +
    '<h4>Known Non-Proofs</h4>' +
    '<ul>' + nonProofList + '</ul>' +
    '</div>' +
    '</div>' +
    '<div class="boundary-flags">' +
    '<h4>Active Boundary Flags</h4>' +
    '<ul>' +
    '<li>No app apply</li>' +
    '<li>No external send</li>' +
    '<li>No arbitrary shell execution</li>' +
    '<li>No provider execution</li>' +
    '<li>No credentials by default</li>' +
    '<li>No live model quality claim</li>' +
    '<li>No production readiness claim</li>' +
    '<li>No security certification claim</li>' +
    '<li>Candidate result is not applied truth</li>' +
    '<li>App-owned apply — Odin does not apply</li>' +
    '<li>Provider is worker, not authority</li>' +
    '<li>Disabled by default</li>' +
    '<li>Local-only</li>' +
    '<li>Candidate-only</li>' +
    '<li>Safe demo only</li>' +
    '</ul>' +
    '</div>' +
    '<p class="boundary-note">claim_boundary: <code>' + uwp_escape(UWP_CLAIM_BOUNDARY) + '</code></p>' +
    '</div>'
  );
}

/* ------------------------------------------------------------------ */
/* Validation / status panel                                           */
/* ------------------------------------------------------------------ */
function uwp_showValidationPanel(validated, gaps) {
  var gapList = (gaps || [])
    .map(function(g) { return '<li>' + uwp_escape(g) + '</li>'; })
    .join('');

  uwp_setContent('uwp-validation-status-content',
    '<div class="validation-panel">' +
    '<p class="boundary-note">Validation receipt is local-only. Does not prove production readiness or model quality.</p>' +
    '<table class="result-table">' +
    '<tr><th>safe_demo_work_validated</th><td>' + (validated ? 'true' : 'false') + '</td></tr>' +
    '<tr><th>candidate_generated</th><td>true (fixture-backed)</td></tr>' +
    '<tr><th>local_only</th><td>true</td></tr>' +
    '<tr><th>candidate_only</th><td>true</td></tr>' +
    '<tr><th>no_app_apply</th><td>true</td></tr>' +
    '<tr><th>no_external_send</th><td>true</td></tr>' +
    '</table>' +
    (gapList
      ? '<h4>Known Gaps / Not Proven</h4><ul>' + gapList + '</ul>'
      : '<p>No blocking gaps detected.</p>'
    ) +
    '<p class="boundary-note">not_proven: production_readiness, live_model_inference, model_quality, app_apply_authority, external_send_authority.</p>' +
    '</div>'
  );
}

/* ------------------------------------------------------------------ */
/* Provider / worker boundary context (PR-10 boundary awareness)       */
/* ------------------------------------------------------------------ */
function uwp_showProviderWorkerContext() {
  uwp_setContent('uwp-provider-worker-context-content',
    '<div class="provider-context-panel">' +
    '<p class="boundary-note">' +
    'Provider/worker boundary context. ' +
    'Providers are workers, not authority. ' +
    'No live inference without receipt. No credentials by default. ' +
    'Disabled by default. No provider execution from playground.' +
    '</p>' +
    '<ul>' +
    '<li>Provider is worker, not authority</li>' +
    '<li>Disabled by default</li>' +
    '<li>No credentials by default</li>' +
    '<li>No live inference without receipt</li>' +
    '<li>No provider execution from playground</li>' +
    '<li>Pre-LLM routes block unsafe work before any model call</li>' +
    '<li>Model-work avoidance active</li>' +
    '<li>Redaction applied before any model work</li>' +
    '</ul>' +
    '<p class="boundary-note">' +
    'Provider execution is not available from the Universal Work Playground. ' +
    'This does not prove provider safety, model quality, or inference correctness.' +
    '</p>' +
    '</div>'
  );
}

/* ------------------------------------------------------------------ */
/* Live API attempt (fixture fallback if unavailable)                  */
/* ------------------------------------------------------------------ */
function uwp_tryLiveWork(packet) {
  return uwp_safeFetch('/v1/universal-work', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(packet),
  })
    .then(function(resp) {
      if (!resp.ok) { return null; }
      return resp.json();
    })
    .then(function(data) {
      if (data && data.candidate_only === true) { return data; }
      return null;
    })
    .catch(function() { return null; });
}

function uwp_loadProofGaps() {
  return uwp_safeFetch('/v1/proof-gaps')
    .then(function(resp) {
      if (!resp.ok) { return []; }
      return resp.json();
    })
    .then(function(data) {
      return Array.isArray(data && data.gaps) ? data.gaps : [];
    })
    .catch(function() { return []; });
}

/* ------------------------------------------------------------------ */
/* Form submit handler                                                  */
/* ------------------------------------------------------------------ */
function uwp_handleFormSubmit(formEl) {
  var titleEl = formEl.querySelector('#uwp-title');
  var intentEl = formEl.querySelector('#uwp-intent');
  var inputEl = formEl.querySelector('#uwp-input-text');

  var packet = {
    artifact_kind: UWP_SAFE_DEMO_WORK_PACKET.artifact_kind,
    candidate_only: true,
    local_only: true,
    external_send: false,
    app_apply: false,
    arbitrary_shell_execution: false,
    provider_execution: false,
    credential_required: false,
    claim_boundary: UWP_CLAIM_BOUNDARY,
    work_kind: 'safe_demo',
    title: titleEl ? titleEl.value.slice(0, 200) : 'Safe Demo Universal Work',
    intent: intentEl ? intentEl.value.slice(0, 500) : 'Demonstrate bounded Universal Work.',
    input_text: inputEl ? inputEl.value.slice(0, 1000) : '',
    constraints: UWP_SAFE_DEMO_WORK_PACKET.constraints,
    expected_output_kind: 'candidate_artifact',
    proof_boundaries: UWP_PROOF_BOUNDARIES,
    known_non_proofs: UWP_KNOWN_NON_PROOFS,
  };

  uwp_setContent('uwp-candidate-result-content', '<p class="loading">Generating safe demo candidate…</p>');

  uwp_tryLiveWork(packet).then(function(liveResult) {
    if (liveResult && liveResult.candidate_only === true) {
      uwp_showCandidateResult(liveResult, 'live-local');
    } else {
      uwp_showCandidateResult(UWP_SAFE_DEMO_CANDIDATE_RESULT, 'fixture');
    }
  });

  uwp_loadProofGaps().then(function(gaps) {
    var allGaps = ['no_live_backend_connected', 'full_live_universal_work_backend_coverage_not_available']
      .concat(gaps || []);
    uwp_showValidationPanel(true, allGaps);
  });
}

/* ------------------------------------------------------------------ */
/* Init                                                                 */
/* ------------------------------------------------------------------ */
function initUniversalWorkPlayground() {
  uwp_setContent('uwp-work-form-content', uwp_buildWorkForm());

  var form = document.getElementById('uwp-safe-demo-form');
  if (form) {
    form.addEventListener('submit', function(evt) {
      evt.preventDefault();
      uwp_handleFormSubmit(form);
    });
  }

  uwp_showCandidateResult(UWP_SAFE_DEMO_CANDIDATE_RESULT, 'fixture');
  uwp_showProofPanel();
  uwp_showValidationPanel(false, [
    'no_live_backend_connected',
    'full_live_universal_work_backend_coverage_not_available',
  ]);
  uwp_showProviderWorkerContext();
}

document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('uwp-work-form-content')) {
    initUniversalWorkPlayground();
  }
});
