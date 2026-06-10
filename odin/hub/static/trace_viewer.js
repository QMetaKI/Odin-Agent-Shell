/**
 * Odin Local Runtime Hub — Bus / Worklet / Atom Trace Viewer (LRH-PR-09)
 *
 * Claim boundary: trace_viewer_candidate_only_local_only_no_event_mutation_no_public_bus_no_raw_payload
 *
 * Provides read-only trace inspection surfaces:
 *   - Bus event timeline (/v1/events — metadata-first, redacted)
 *   - Worklet trace view (worklet_id, type, state, input/output metadata)
 *   - Work atom trace view (atom_id, kind, status, digest metadata)
 *   - Runtime digest view (runtime_digest, trace_digest, counts — not a cert)
 *   - Local-only trace filters (type, status, source, target — local only)
 *   - Redacted payload preview policy (sensitive payloads never shown raw)
 *   - Proof boundary display on every surface
 *
 * Not proven:
 *   - production_readiness
 *   - live_model_inference
 *   - app_state_mutation
 *   - external_send_authority
 *   - full_bus_backend_coverage
 *   - full_worklet_backend_coverage
 *   - full_work_atom_backend_coverage
 *   - raw_sensitive_payload_safety_certification
 *   - event_mutation_authority
 *   - worklet_execution_authority
 *   - atom_mutation_authority
 *   - public_bus_exposure
 *   - security_certification
 *   - live_browser_runtime_e2e
 *
 * Forbidden in this file:
 *   - publishEvent() / replayEvent() / deleteEvent() / ackEvent() / mutateEvent()
 *   - executeWorklet() / retryWorklet()
 *   - mutateAtom() / deleteAtom() / applyTrace()
 *   - externalSend() / uploadTrace() / hiddenUpload()
 *   - raw sensitive payload display
 *   - public bus controls
 *   - network requests outside localhost
 */

/* ------------------------------------------------------------------ */
/* Trace Viewer Claim Boundary                                          */
/* ------------------------------------------------------------------ */
var TRACE_VIEWER_CLAIM_BOUNDARY =
  'trace_viewer_candidate_only_local_only_no_event_mutation_no_public_bus_no_raw_payload';

var TRACE_VIEWER_NOT_PROVEN = [
  'production_readiness',
  'security_certification',
  'live_browser_runtime_e2e',
  'full_bus_backend_coverage',
  'full_worklet_backend_coverage',
  'full_work_atom_backend_coverage',
  'raw_sensitive_payload_safety_certification',
  'event_mutation_authority',
  'worklet_execution_authority',
  'atom_mutation_authority',
  'public_bus_exposure',
  'external_send_authority',
  'live_model_inference',
  'model_quality',
  'app_state_mutation',
];

/* Required boundary tokens */
var TRACE_VIEWER_BOUNDARY_TOKENS = [
  'candidate_only',
  'claim_boundary',
  'local_only',
  'read_only',
  'no_event_mutation',
  'no_raw_payload',
  'metadata_first',
];

var TRACE_VIEWER_API_BASE = (typeof ODIN_API_BASE !== 'undefined') ? ODIN_API_BASE : 'http://127.0.0.1:8877';

/* ------------------------------------------------------------------ */
/* Localhost guard                                                      */
/* ------------------------------------------------------------------ */
function tvIsLocalhost(url) {
  try {
    var u = new URL(url);
    return (u.hostname === '127.0.0.1' || u.hostname === 'localhost' || u.hostname === '::1');
  } catch (e) {
    return false;
  }
}

/* ------------------------------------------------------------------ */
/* Minimal fetch wrapper — localhost only                              */
/* ------------------------------------------------------------------ */
function tvFetch(path) {
  var url = TRACE_VIEWER_API_BASE + path;
  if (!tvIsLocalhost(url)) {
    return Promise.reject(new Error('TraceViewer: Non-localhost URL blocked: ' + url));
  }
  return fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
    .then(function(r) {
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json();
    });
}

/* ------------------------------------------------------------------ */
/* Helpers                                                              */
/* ------------------------------------------------------------------ */
function tvSetContent(id, html) {
  var el = document.getElementById(id);
  if (el) { el.innerHTML = html; }
}

function tvEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function tvShowError(id, msg) {
  tvSetContent(id,
    '<p class="api-error">Unable to reach local API: ' + tvEscape(msg) +
    ' — ensure the Odin local runtime is running on ' + tvEscape(TRACE_VIEWER_API_BASE) + '</p>' +
    '<p class="boundary-note">Trace viewer is read-only and local-only. No event mutation.</p>'
  );
}

/* Redact sensitive fields — raw sensitive payloads are never displayed */
function tvRedactSensitive(key, value) {
  var sensitiveKeys = [
    'secret', 'token', 'password', 'key', 'credential', 'auth',
    'private', 'raw_payload', 'payload_raw', 'sensitive', 'payload',
  ];
  var keyLower = String(key).toLowerCase();
  for (var i = 0; i < sensitiveKeys.length; i++) {
    if (keyLower.indexOf(sensitiveKeys[i]) !== -1) {
      return '[REDACTED — raw sensitive payload not displayed by default]';
    }
  }
  if (typeof value === 'object' && value !== null) {
    return '[object — metadata-first display only]';
  }
  return value;
}

/* ------------------------------------------------------------------ */
/* Trace Viewer Boundary Banner                                         */
/* Required on every trace surface                                      */
/* ------------------------------------------------------------------ */
function tvBoundaryBanner(extra) {
  return '<div class="tv-boundary-banner" aria-label="Trace Viewer Boundary">' +
    '<strong>Trace viewer — read-only, local-only</strong> · ' +
    '<span class="boundary-item">No event mutation</span> · ' +
    '<span class="boundary-item">No bus publish</span> · ' +
    '<span class="boundary-item">No worklet execution</span> · ' +
    '<span class="boundary-item">No atom mutation</span> · ' +
    '<span class="boundary-item">No raw sensitive payload display</span> · ' +
    '<span class="boundary-item">metadata_first</span>' +
    (extra ? ' · <span class="boundary-item">' + tvEscape(extra) + '</span>' : '') +
    '</div>';
}

function tvReadOnlyNote() {
  return '<p class="boundary-note tv-read-only-note">' +
    'Read-only trace viewer — candidate_only. ' +
    'No event mutation. No bus publish, replay, delete, or ack. ' +
    'No worklet execution. No atom mutation. No external send.' +
    '</p>';
}

/* ------------------------------------------------------------------ */
/* Local-only trace filter state                                        */
/* Filters are applied locally — no remote search, no network fetch   */
/* ------------------------------------------------------------------ */
var tvFilterState = {
  eventType: '',
  status: '',
  source: '',
  target: '',
};

function tvRenderFilters(containerId) {
  var container = document.getElementById(containerId);
  if (!container) { return; }
  container.innerHTML =
    '<div class="tv-filters" aria-label="Local-only trace filters">' +
    '<p class="boundary-note">Local-only trace filters — no remote search, no network fetch outside localhost.</p>' +
    '<label>Event type: <input type="text" id="tv-filter-type" value="' + tvEscape(tvFilterState.eventType) +
      '" placeholder="e.g. runtime.event" oninput="tvApplyFilter()" /></label> ' +
    '<label>Status: <input type="text" id="tv-filter-status" value="' + tvEscape(tvFilterState.status) +
      '" placeholder="e.g. ok" oninput="tvApplyFilter()" /></label> ' +
    '<label>Source: <input type="text" id="tv-filter-source" value="' + tvEscape(tvFilterState.source) +
      '" placeholder="source" oninput="tvApplyFilter()" /></label> ' +
    '<label>Target: <input type="text" id="tv-filter-target" value="' + tvEscape(tvFilterState.target) +
      '" placeholder="target" oninput="tvApplyFilter()" /></label>' +
    '</div>';
}

function tvApplyFilter() {
  var typeEl = document.getElementById('tv-filter-type');
  var statusEl = document.getElementById('tv-filter-status');
  var sourceEl = document.getElementById('tv-filter-source');
  var targetEl = document.getElementById('tv-filter-target');
  if (typeEl) { tvFilterState.eventType = typeEl.value; }
  if (statusEl) { tvFilterState.status = statusEl.value; }
  if (sourceEl) { tvFilterState.source = sourceEl.value; }
  if (targetEl) { tvFilterState.target = targetEl.value; }
  loadBusEventTimeline();
}

function tvMatchesFilter(event) {
  if (tvFilterState.eventType && String(event.event_type || '').indexOf(tvFilterState.eventType) === -1) { return false; }
  if (tvFilterState.status && String(event.status || '').indexOf(tvFilterState.status) === -1) { return false; }
  if (tvFilterState.source && String(event.source || '').indexOf(tvFilterState.source) === -1) { return false; }
  if (tvFilterState.target && String(event.target || '').indexOf(tvFilterState.target) === -1) { return false; }
  return true;
}

/* ------------------------------------------------------------------ */
/* Bus Event Timeline                                                   */
/* Uses /v1/events — metadata-first, redacted, no mutation controls   */
/* ------------------------------------------------------------------ */
function loadBusEventTimeline() {
  var container = document.getElementById('tv-bus-events-content');
  if (!container) { return; }

  container.innerHTML = tvBoundaryBanner('bus-event-timeline') + tvReadOnlyNote() +
    '<p class="loading">Loading bus event timeline…</p>';

  tvFetch('/v1/events').then(function(data) {
    var events = data.events || data.items || [];
    var filteredEvents = events.filter(tvMatchesFilter);

    var html = tvBoundaryBanner('bus-event-timeline') + tvReadOnlyNote();
    html += '<div class="tv-filter-panel">';
    html += '<p class="boundary-note">Local-only trace filters — filter is applied in-browser, no remote search.</p>';
    html += '<div class="tv-filter-row">';
    html += '<label class="tv-filter-label">Type: <input type="text" class="tv-filter-input" id="tv-filter-type" value="' + tvEscape(tvFilterState.eventType) + '" placeholder="event type" oninput="tvApplyFilter()" /></label> ';
    html += '<label class="tv-filter-label">Status: <input type="text" class="tv-filter-input" id="tv-filter-status" value="' + tvEscape(tvFilterState.status) + '" placeholder="status" oninput="tvApplyFilter()" /></label> ';
    html += '<label class="tv-filter-label">Source: <input type="text" class="tv-filter-input" id="tv-filter-source" value="' + tvEscape(tvFilterState.source) + '" placeholder="source" oninput="tvApplyFilter()" /></label> ';
    html += '<label class="tv-filter-label">Target: <input type="text" class="tv-filter-input" id="tv-filter-target" value="' + tvEscape(tvFilterState.target) + '" placeholder="target" oninput="tvApplyFilter()" /></label>';
    html += '</div></div>';

    if (filteredEvents.length === 0) {
      html += '<p class="status-warn">No bus events available' + (events.length > 0 ? ' (filtered out)' : '') + '.</p>';
      html += '<p class="boundary-note"><strong>Proof gap:</strong> full_bus_backend_coverage not proven.</p>';
    } else {
      html += '<p>Bus events (' + filteredEvents.length + ' shown' + (events.length !== filteredEvents.length ? ' of ' + events.length + ' total' : '') + '):</p>';
      html += '<div class="tv-timeline">';
      filteredEvents.forEach(function(ev, idx) {
        var evType = ev.event_type || ev.type || '(unknown)';
        var evId = ev.event_id || ev.id || ('event-' + idx);
        var evStatus = ev.status || 'unknown';
        var evSource = ev.source || '';
        var evTarget = ev.target || '';
        var evTs = ev.timestamp || ev.created_at || '';
        var evSeq = ev.sequence !== undefined ? ev.sequence : '';
        var evCb = ev.claim_boundary || '';
        var evCandOnly = ev.candidate_only;
        var cls = (evStatus === 'ok' || evStatus === 'emitted') ? 'status-ok' : 'status-warn';
        html += '<div class="tv-event-row">';
        html += '<span class="tv-event-id"><code>' + tvEscape(String(evId)) + '</code></span>';
        html += ' <span class="tv-event-type"><strong>' + tvEscape(evType) + '</strong></span>';
        html += ' <span class="' + cls + '">' + tvEscape(evStatus) + '</span>';
        if (evTs) { html += ' <span class="tv-event-ts muted">' + tvEscape(evTs) + '</span>'; }
        if (evSeq !== '') { html += ' <span class="muted">seq:' + tvEscape(String(evSeq)) + '</span>'; }
        if (evSource) { html += ' <span class="muted">src:' + tvEscape(evSource) + '</span>'; }
        if (evTarget) { html += ' <span class="muted">→' + tvEscape(evTarget) + '</span>'; }
        if (evCb) { html += ' <code class="muted tv-small">' + tvEscape(evCb) + '</code>'; }
        if (evCandOnly !== undefined) { html += ' <span class="muted">candidate_only:' + tvEscape(String(evCandOnly)) + '</span>'; }
        /* Redacted payload summary — raw sensitive payload never shown */
        var payloadSummary = ev.payload_summary || ev.redacted_summary || null;
        if (payloadSummary) {
          html += '<br><span class="tv-payload-summary muted">summary: ' + tvEscape(String(payloadSummary)) + '</span>';
        } else if (ev.payload !== undefined) {
          html += '<br><span class="tv-payload-summary muted">[payload redacted — raw sensitive payload not displayed by default]</span>';
        }
        html += '</div>';
      });
      html += '</div>';
    }

    html += '<p class="boundary-note">Bus event timeline is read-only and local-only.</p>';
    html += '<p class="boundary-note">No event mutation. No bus publish, replay, delete, or ack controls.</p>';
    html += '<p class="boundary-note">No public bus exposure. No LAN/WAN trace endpoint by default.</p>';
    html += '<p class="boundary-note">Raw sensitive payloads are not displayed by default.</p>';
    html += '<p class="boundary-note">claim_boundary: <code>' + tvEscape(TRACE_VIEWER_CLAIM_BOUNDARY) + '</code></p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = tvBoundaryBanner('bus-event-timeline') + tvReadOnlyNote();
    html += '<p class="api-error">Bus event timeline unavailable: ' + tvEscape(e.message) + '</p>';
    html += '<div class="tv-fixture-placeholder">';
    html += '<p class="boundary-note">Events endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><strong>Proof gap:</strong> full_bus_backend_coverage not proven.</p>';
    html += '<p>To query events: <code>GET ' + tvEscape(TRACE_VIEWER_API_BASE) + '/v1/events</code></p>';
    html += '<p><em>Placeholder trace entry:</em></p>';
    html += '<div class="tv-event-row">';
    html += '<code>(fixture-placeholder)</code> <strong>runtime.bus.status</strong> ';
    html += '<span class="status-warn">unknown</span> ';
    html += '<span class="muted">candidate_only: true</span>';
    html += '</div>';
    html += '</div>';
    html += '<p class="boundary-note">No event mutation. No bus publish, replay, delete, or ack.</p>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Worklet Trace View                                                   */
/* Read-only inspection — no execute, retry, or apply controls        */
/* ------------------------------------------------------------------ */
function loadWorkletTraceView() {
  var container = document.getElementById('tv-worklet-trace-content');
  if (!container) { return; }

  container.innerHTML = tvBoundaryBanner('worklet-trace') + tvReadOnlyNote() +
    '<p class="loading">Loading worklet trace…</p>';

  /* Use /v1/status which may include worklet info; fall back to placeholder */
  tvFetch('/v1/status').then(function(data) {
    var worklets = data.worklets || data.active_worklets || [];
    var workletCount = data.worklet_count || (Array.isArray(worklets) ? worklets.length : null);

    var html = tvBoundaryBanner('worklet-trace') + tvReadOnlyNote();
    html += '<div class="tv-worklet-surface">';
    html += '<p class="boundary-note"><strong>Worklet trace view — read-only.</strong> No execute, retry, or apply controls.</p>';

    if (workletCount !== null) {
      html += '<p><strong>Worklet count:</strong> ' + tvEscape(String(workletCount)) + '</p>';
    }

    if (Array.isArray(worklets) && worklets.length > 0) {
      html += '<div class="tv-worklet-list">';
      worklets.forEach(function(w, idx) {
        var wId = w.worklet_id || w.id || ('worklet-' + idx);
        var wType = w.worklet_type || w.type || w.name || '(unknown)';
        var wStatus = w.status || w.state || 'unknown';
        var wCb = w.claim_boundary || '';
        var wCandOnly = w.candidate_only;
        var cls = (wStatus === 'ok' || wStatus === 'complete') ? 'status-ok' : 'status-warn';
        html += '<div class="tv-worklet-row">';
        html += '<strong>Worklet ID:</strong> <code>' + tvEscape(String(wId)) + '</code>';
        html += ' | <strong>Type:</strong> ' + tvEscape(wType);
        html += ' | <strong>Status:</strong> <span class="' + cls + '">' + tvEscape(wStatus) + '</span>';
        if (wCb) { html += ' | <code class="muted tv-small">' + tvEscape(wCb) + '</code>'; }
        if (wCandOnly !== undefined) { html += ' | candidate_only:' + tvEscape(String(wCandOnly)); }
        /* Input/output metadata — redacted, no raw payload */
        if (w.input_metadata) {
          html += '<br><span class="muted">input metadata (safe): ' + tvEscape(JSON.stringify(tvRedactSensitive('input_metadata', w.input_metadata))) + '</span>';
        }
        if (w.output_metadata) {
          html += '<br><span class="muted">output metadata (safe): ' + tvEscape(JSON.stringify(tvRedactSensitive('output_metadata', w.output_metadata))) + '</span>';
        }
        if (w.known_non_proofs && w.known_non_proofs.length) {
          html += '<br><span class="muted">known_non_proofs: ' + tvEscape(w.known_non_proofs.join(', ')) + '</span>';
        }
        html += '</div>';
      });
      html += '</div>';
    } else {
      html += '<p class="status-warn">No worklet trace data available from /v1/status.</p>';
      html += '<p class="boundary-note"><strong>Proof gap:</strong> full_worklet_backend_coverage not proven.</p>';
      html += '<p><em>Placeholder worklet trace:</em></p>';
      html += '<div class="tv-worklet-row">';
      html += '<code>(fixture-placeholder)</code> | <strong>Type:</strong> context_compress_worklet';
      html += ' | <strong>Status:</strong> <span class="status-warn">unknown</span>';
      html += ' | candidate_only: true';
      html += '</div>';
    }

    html += '</div>';
    html += '<p class="boundary-note">No execute, retry, or apply controls. No worklet state mutation.</p>';
    html += '<p class="boundary-note">Worklet trace is read-only. Raw sensitive payloads not displayed.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = tvBoundaryBanner('worklet-trace') + tvReadOnlyNote();
    html += '<p class="api-error">Worklet trace unavailable: ' + tvEscape(e.message) + '</p>';
    html += '<div class="tv-fixture-placeholder">';
    html += '<p class="boundary-note">Worklet trace endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><strong>Proof gap:</strong> full_worklet_backend_coverage not proven.</p>';
    html += '</div>';
    html += '<p class="boundary-note">No worklet execution. No worklet state mutation. Read-only trace.</p>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Work Atom Trace View                                                 */
/* Read-only inspection — no mutate, delete, or apply controls        */
/* ------------------------------------------------------------------ */
function loadWorkAtomTraceView() {
  var container = document.getElementById('tv-work-atom-trace-content');
  if (!container) { return; }

  container.innerHTML = tvBoundaryBanner('work-atom-trace') + tvReadOnlyNote() +
    '<p class="loading">Loading work atom trace…</p>';

  tvFetch('/v1/status').then(function(data) {
    var atoms = data.work_atoms || data.atoms || [];
    var atomCount = data.atom_count || data.work_atom_count || (Array.isArray(atoms) ? atoms.length : null);

    var html = tvBoundaryBanner('work-atom-trace') + tvReadOnlyNote();
    html += '<div class="tv-atom-surface">';
    html += '<p class="boundary-note"><strong>Work atom trace view — read-only.</strong> No mutate, delete, or apply controls.</p>';

    if (atomCount !== null) {
      html += '<p><strong>Work atom count:</strong> ' + tvEscape(String(atomCount)) + '</p>';
    }

    if (Array.isArray(atoms) && atoms.length > 0) {
      html += '<div class="tv-atom-list">';
      atoms.forEach(function(a, idx) {
        var aId = a.atom_id || a.id || ('atom-' + idx);
        var aKind = a.atom_kind || a.kind || a.type || '(unknown)';
        var aStatus = a.status || 'unknown';
        var aDeps = a.dependencies || [];
        var aDigest = a.digest || a.trace_id || '';
        var aCb = a.claim_boundary || '';
        var cls = (aStatus === 'ok' || aStatus === 'complete') ? 'status-ok' : 'status-warn';
        html += '<div class="tv-atom-row">';
        html += '<strong>Atom ID:</strong> <code>' + tvEscape(String(aId)) + '</code>';
        html += ' | <strong>Kind:</strong> ' + tvEscape(aKind);
        html += ' | <strong>Status:</strong> <span class="' + cls + '">' + tvEscape(aStatus) + '</span>';
        if (aDigest) { html += ' | <strong>Digest:</strong> <code class="muted">' + tvEscape(String(aDigest)) + '</code>'; }
        if (aDeps.length) { html += '<br><span class="muted">deps: ' + tvEscape(aDeps.join(', ')) + '</span>'; }
        if (aCb) { html += '<br><code class="muted tv-small">' + tvEscape(aCb) + '</code>'; }
        html += '</div>';
      });
      html += '</div>';
    } else {
      html += '<p class="status-warn">No work atom trace data available from /v1/status.</p>';
      html += '<p class="boundary-note"><strong>Proof gap:</strong> full_work_atom_backend_coverage not proven.</p>';
      html += '<p><em>Placeholder atom trace:</em></p>';
      html += '<div class="tv-atom-row">';
      html += '<code>(fixture-placeholder)</code> | <strong>Kind:</strong> context_compress_atom';
      html += ' | <strong>Status:</strong> <span class="status-warn">unknown</span>';
      html += ' | <strong>Digest:</strong> <code class="muted">(fixture)</code>';
      html += '</div>';
    }

    html += '</div>';
    html += '<p class="boundary-note">No mutate, delete, or apply controls. No atom state mutation.</p>';
    html += '<p class="boundary-note">Work atom trace is read-only. Raw sensitive payloads not displayed.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = tvBoundaryBanner('work-atom-trace') + tvReadOnlyNote();
    html += '<p class="api-error">Work atom trace unavailable: ' + tvEscape(e.message) + '</p>';
    html += '<div class="tv-fixture-placeholder">';
    html += '<p class="boundary-note">Work atom trace endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><strong>Proof gap:</strong> full_work_atom_backend_coverage not proven.</p>';
    html += '</div>';
    html += '<p class="boundary-note">No atom mutation. No atom deletion. Read-only trace.</p>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Runtime Digest View                                                  */
/* Local receipt only — not a production/security certification        */
/* ------------------------------------------------------------------ */
function loadRuntimeDigestView() {
  var container = document.getElementById('tv-runtime-digest-content');
  if (!container) { return; }

  container.innerHTML = tvBoundaryBanner('runtime-digest') + tvReadOnlyNote() +
    '<p class="loading">Loading runtime digest…</p>';

  tvFetch('/v1/health').then(function(healthData) {
    return tvFetch('/v1/status').then(function(statusData) {
      return { health: healthData, status: statusData };
    });
  }).then(function(combined) {
    var health = combined.health;
    var status = combined.status;

    var html = tvBoundaryBanner('runtime-digest') + tvReadOnlyNote();
    html += '<div class="tv-digest-surface">';
    html += '<div class="tv-not-cert-warning">';
    html += '<strong>Not a production or security certification.</strong> ';
    html += 'This digest is a local receipt only and does not prove production readiness or security.';
    html += '</div>';

    var runtimeDigest = health.runtime_digest || status.runtime_digest || health.digest || status.digest || null;
    var traceDigest = health.trace_digest || status.trace_digest || null;
    var eventCount = status.event_count || health.event_count || null;
    var workletCount = status.worklet_count || health.worklet_count || null;
    var atomCount = status.atom_count || status.work_atom_count || health.atom_count || null;
    var localStatus = health.status || status.status || 'unknown';
    var localCb = health.claim_boundary || status.claim_boundary || 'unknown';

    html += '<p><strong>Runtime status:</strong> ';
    var cls = (localStatus === 'ok') ? 'status-ok' : 'status-warn';
    html += '<span class="' + cls + '">' + tvEscape(localStatus) + '</span></p>';

    if (runtimeDigest) {
      html += '<p><strong>Runtime digest:</strong> <code>' + tvEscape(String(runtimeDigest)) + '</code></p>';
    } else {
      html += '<p class="muted"><em>runtime_digest: not available from local API</em></p>';
    }
    if (traceDigest) {
      html += '<p><strong>Trace digest:</strong> <code>' + tvEscape(String(traceDigest)) + '</code></p>';
    }
    if (eventCount !== null) {
      html += '<p><strong>Event count:</strong> ' + tvEscape(String(eventCount)) + '</p>';
    }
    if (workletCount !== null) {
      html += '<p><strong>Worklet count:</strong> ' + tvEscape(String(workletCount)) + '</p>';
    }
    if (atomCount !== null) {
      html += '<p><strong>Atom count:</strong> ' + tvEscape(String(atomCount)) + '</p>';
    }
    html += '<p><strong>claim_boundary:</strong> <code>' + tvEscape(localCb) + '</code></p>';

    html += '<p><strong>Known not-proven (this digest view):</strong></p>';
    html += '<ul class="proof-gap-list">';
    TRACE_VIEWER_NOT_PROVEN.forEach(function(np) {
      html += '<li>' + tvEscape(np) + '</li>';
    });
    html += '</ul>';

    html += '</div>';
    html += '<p class="boundary-note">Runtime digest is a local receipt. Not production certification. Not security certification.</p>';
    html += '<p class="boundary-note">No app apply. No external send. No provider execution. Candidate-only.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = tvBoundaryBanner('runtime-digest') + tvReadOnlyNote();
    html += '<p class="api-error">Runtime digest unavailable: ' + tvEscape(e.message) + '</p>';
    html += '<div class="tv-fixture-placeholder">';
    html += '<p class="boundary-note">Runtime digest endpoint not available — showing fixture-compatible placeholder.</p>';
    html += '<p><em>Placeholder digest:</em></p>';
    html += '<p><strong>Runtime digest:</strong> <code>(fixture-placeholder)</code></p>';
    html += '<p><strong>Not a production certification. Not a security certification.</strong></p>';
    html += '</div>';
    html += '<p class="boundary-note">No production readiness proof. No security certification proof.</p>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Trace Viewer Proof Gap Surface                                       */
/* Uses /v1/proof-gaps                                                  */
/* ------------------------------------------------------------------ */
function loadTraceProofGaps() {
  var container = document.getElementById('tv-proof-gaps-content');
  if (!container) { return; }

  container.innerHTML = tvBoundaryBanner('proof-gaps') +
    '<p class="loading">Loading trace proof gaps…</p>';

  tvFetch('/v1/proof-gaps').then(function(data) {
    var gaps = data.proof_gaps || data.gaps || [];
    var html = tvBoundaryBanner('proof-gaps');
    html += '<p class="boundary-note">Displaying proof gaps does not close them. Viewer-only.</p>';

    if (gaps.length === 0) {
      html += '<p class="status-warn">No proof gaps reported by API — gaps may still exist locally.</p>';
    } else {
      html += '<p>Proof gaps from API (' + gaps.length + '):</p><ul class="proof-gap-list">';
      gaps.forEach(function(g) {
        html += '<li>' + tvEscape(typeof g === 'string' ? g : JSON.stringify(g)) + '</li>';
      });
      html += '</ul>';
    }

    html += '<p><strong>Known not-proven (trace viewer):</strong></p><ul class="proof-gap-list">';
    TRACE_VIEWER_NOT_PROVEN.forEach(function(np) {
      html += '<li>' + tvEscape(np) + '</li>';
    });
    html += '</ul>';

    html += '<p class="boundary-note">claim_boundary: <code>' + tvEscape(TRACE_VIEWER_CLAIM_BOUNDARY) + '</code></p>';
    html += '<p class="boundary-note">Proof gaps displayed here are not resolved by being displayed.</p>';
    container.innerHTML = html;
  }).catch(function(e) {
    var html = tvBoundaryBanner('proof-gaps');
    html += '<p class="api-error">Proof gaps unavailable: ' + tvEscape(e.message) + '</p>';
    html += '<p><strong>Known not-proven (trace viewer):</strong></p><ul class="proof-gap-list">';
    TRACE_VIEWER_NOT_PROVEN.forEach(function(np) {
      html += '<li>' + tvEscape(np) + '</li>';
    });
    html += '</ul>';
    container.innerHTML = html;
  });
}

/* ------------------------------------------------------------------ */
/* Trace Viewer initialisation                                          */
/* ------------------------------------------------------------------ */
function initTraceViewer() {
  loadBusEventTimeline();
  loadWorkletTraceView();
  loadWorkAtomTraceView();
  loadRuntimeDigestView();
  loadTraceProofGaps();
}

document.addEventListener('DOMContentLoaded', function() {
  var hasTrace = (
    document.getElementById('tv-bus-events-content') ||
    document.getElementById('tv-worklet-trace-content') ||
    document.getElementById('tv-work-atom-trace-content') ||
    document.getElementById('tv-runtime-digest-content') ||
    document.getElementById('tv-proof-gaps-content')
  );
  if (hasTrace) {
    initTraceViewer();
  }
});

/*
 * No publishEvent(), replayEvent(), deleteEvent(), ackEvent(), mutateEvent(),
 * executeWorklet(), retryWorklet(), mutateAtom(), deleteAtom(), applyTrace(),
 * externalSend(), uploadTrace(), hiddenUpload(), rawPayloadReveal(), or
 * unsafePayloadToggle() defined in this file.
 *
 * Trace viewer is read-only, local-only, metadata-first, candidate-only.
 * No event mutation. No bus publish. No worklet execution. No atom mutation.
 * No raw sensitive payload display. No public bus exposure.
 */
