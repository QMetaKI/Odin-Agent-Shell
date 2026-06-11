/**
 * Odin Local Runtime Hub — Local Config Safe Settings surface.
 * LRH-PR-14
 *
 * Claim boundary: local_config_safe_settings_candidate_only_local_only_settings_visibility_only_no_app_apply_no_external_send_no_credentials_no_wan_lan_default
 *
 * candidate_only: true
 * local_only: true
 * read_only: true
 * settings_visibility_only: true
 * redaction_status_not_security_certification: true
 * provider_settings_disabled_by_default: true
 * no_app_apply: true
 * no_external_send: true
 * no_credentials: true
 * no_raw_payload_reveal: true
 * no_redaction_bypass: true
 *
 * proof_boundaries:
 *   not_production_readiness_certification
 *   not_security_certification
 *   not_redaction_safety_certification
 *   not_provider_credential_storage_proof
 *   not_public_network_api_proof
 *   not_app_apply_proof
 *   not_app_state_mutation_proof
 *   not_external_send_authority_proof
 *   not_live_model_inference_proof
 *   not_model_quality_proof
 *   not_raw_payload_reveal_proof
 *   settings_visibility_only
 *   redaction_status_not_security_certification
 *   provider_settings_disabled_by_default
 *
 * known_non_proofs:
 *   production_readiness
 *   security_certification
 *   redaction_safety_certification
 *   provider_credential_storage
 *   app_apply_authority
 *   external_send_authority
 *   live_model_inference
 *   model_quality
 *   windows_service_tray_installer
 *   signed_distribution
 */

(function() {
  'use strict';

  var LCSS_CLAIM_BOUNDARY = 'local_config_safe_settings_candidate_only_local_only_settings_visibility_only_no_app_apply_no_external_send_no_credentials_no_wan_lan_default';
  var LCSS_PROOF_BOUNDARIES = [
    'not_production_readiness_certification',
    'not_security_certification',
    'not_redaction_safety_certification',
    'not_provider_credential_storage_proof',
    'not_public_network_api_proof',
    'not_app_apply_proof',
    'not_app_state_mutation_proof',
    'not_external_send_authority_proof',
    'not_live_model_inference_proof',
    'not_model_quality_proof',
    'not_raw_payload_reveal_proof',
    'settings_visibility_only',
    'redaction_status_not_security_certification',
    'provider_settings_disabled_by_default'
  ];
  var LCSS_KNOWN_NON_PROOFS = [
    'production_readiness',
    'security_certification',
    'redaction_safety_certification',
    'provider_credential_storage',
    'app_apply_authority',
    'external_send_authority',
    'live_model_inference',
    'model_quality',
    'windows_service_tray_installer',
    'signed_distribution'
  ];

  /* Safe defaults - these are the only allowed values */
  var SAFE_CONFIG_DEFAULTS = {
    localhost_only: true,
    bind_host: '127.0.0.1',
    public_network_enabled: false,
    external_send_enabled: false,
    app_apply_enabled: false,
    provider_credentials_enabled: false,
    raw_payload_reveal_enabled: false,
    redaction_enabled: true,
    providers_enabled_by_default: false,
    candidate_only: true
  };

  /* Unsafe settings block list - for display only */
  var UNSAFE_BLOCK_LIST = [
    { field: 'bind_host', blocked: ['0.0.0.0', '::'], reason: 'blocked because unsafe network default' },
    { field: 'public_network_enabled', blocked: [true], reason: 'blocked because external send is not Odin authority' },
    { field: 'external_send_enabled', blocked: [true], reason: 'blocked because external send is not Odin authority' },
    { field: 'app_apply_enabled', blocked: [true], reason: 'blocked because app apply is host-owned' },
    { field: 'provider_credentials_enabled', blocked: [true], reason: 'blocked because provider credentials must not be enabled by default' },
    { field: 'raw_payload_reveal_enabled', blocked: [true], reason: 'blocked because raw payload reveal is not allowed' },
    { field: 'log_secrets', blocked: [true], reason: 'blocked because secrets must not appear in logs' },
    { field: 'redaction_enabled', blocked: [false], reason: 'blocked because redaction must remain enabled' },
    { field: 'providers.enabled_by_default', blocked: [true], reason: 'blocked because provider credentials must not be enabled by default' }
  ];

  function lcssEscapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function lcssSetContent(id, html) {
    var el = document.getElementById(id);
    if (el) { el.innerHTML = html; }
  }

  function lcssRenderStatusRow(label, value, ok) {
    var cls = ok ? 'status-ok' : 'status-blocked';
    var icon = ok ? '&#10003;' : '&#10007;';
    return '<div class="lcss-status-row ' + cls + '">' +
      '<span class="lcss-status-icon">' + icon + '</span>' +
      '<span class="lcss-status-label">' + lcssEscapeHtml(label) + '</span>' +
      '<span class="lcss-status-value">' + lcssEscapeHtml(String(value)) + '</span>' +
      '</div>';
  }

  function lcssRenderLocalConfigStatus() {
    var html = '<div class="lcss-config-status">';
    html += lcssRenderStatusRow('localhost_only', SAFE_CONFIG_DEFAULTS.localhost_only, true);
    html += lcssRenderStatusRow('bind_host', SAFE_CONFIG_DEFAULTS.bind_host, true);
    html += lcssRenderStatusRow('public_network_enabled', SAFE_CONFIG_DEFAULTS.public_network_enabled, true);
    html += lcssRenderStatusRow('external_send_enabled', SAFE_CONFIG_DEFAULTS.external_send_enabled, true);
    html += lcssRenderStatusRow('app_apply_enabled', SAFE_CONFIG_DEFAULTS.app_apply_enabled, true);
    html += lcssRenderStatusRow('provider_credentials_enabled', SAFE_CONFIG_DEFAULTS.provider_credentials_enabled, true);
    html += lcssRenderStatusRow('raw_payload_reveal_enabled', SAFE_CONFIG_DEFAULTS.raw_payload_reveal_enabled, true);
    html += lcssRenderStatusRow('redaction_enabled', SAFE_CONFIG_DEFAULTS.redaction_enabled, true);
    html += lcssRenderStatusRow('providers.enabled_by_default', SAFE_CONFIG_DEFAULTS.providers_enabled_by_default, true);
    html += lcssRenderStatusRow('candidate_only', SAFE_CONFIG_DEFAULTS.candidate_only, true);
    html += '</div>';
    html += '<p class="boundary-note">Settings visibility only. Not a security certification. Not a production readiness certification. Read-only. No edit controls.</p>';
    return html;
  }

  function lcssRenderUnsafeBlockList() {
    var html = '<div class="lcss-block-list">';
    html += '<h4>Unsafe Setting Block List</h4>';
    html += '<table class="lcss-block-table"><thead><tr><th>Field</th><th>Blocked Values</th><th>Reason</th></tr></thead><tbody>';
    UNSAFE_BLOCK_LIST.forEach(function(item) {
      html += '<tr>' +
        '<td class="lcss-field">' + lcssEscapeHtml(item.field) + '</td>' +
        '<td class="lcss-blocked">' + lcssEscapeHtml(item.blocked.join(', ')) + '</td>' +
        '<td class="lcss-reason">' + lcssEscapeHtml(item.reason) + '</td>' +
        '</tr>';
    });
    html += '</tbody></table>';
    html += '</div>';
    html += '<p class="boundary-note">Block list is deterministic local validation. Not a security certification. Not a redaction bypass. Read-only display.</p>';
    return html;
  }

  function lcssRenderRedactionStatus() {
    var html = '<div class="lcss-redaction-status">';
    html += '<div class="lcss-status-row status-ok">';
    html += '<span class="lcss-status-icon">&#10003;</span>';
    html += '<span class="lcss-status-label">Redaction enabled</span>';
    html += '<span class="lcss-status-value">true</span>';
    html += '</div>';
    html += '<div class="lcss-redaction-marker-info">';
    html += '<span class="lcss-label">Redaction marker:</span> ';
    html += '<code>[REDACTED]</code>';
    html += '</div>';
    html += '</div>';
    html += '<p class="boundary-note">Redaction status is not a security certification. No raw sensitive payload display. No redaction bypass control. Not a redaction safety certification.</p>';
    return html;
  }

  function lcssRenderProviderDisabledByDefault() {
    var html = '<div class="lcss-provider-disabled">';
    html += lcssRenderStatusRow('providers.enabled_by_default', false, true);
    html += '<p class="boundary-note">Provider settings are disabled by default. Explicit config required before provider enablement. This is provider settings visibility only. Not a provider execution proof. Not a credential storage proof.</p>';
    html += '<ul class="lcss-boundary-list">';
    html += '<li>No provider run button</li>';
    html += '<li>No provider enable toggle</li>';
    html += '<li>No credential field</li>';
    html += '<li>No API key field</li>';
    html += '<li>No token field</li>';
    html += '</ul>';
    html += '</div>';
    return html;
  }

  function lcssRenderProofBoundaries() {
    var html = '<div class="lcss-proof-boundaries">';
    html += '<h4>Proof Boundaries</h4>';
    html += '<ul class="lcss-boundary-list">';
    LCSS_PROOF_BOUNDARIES.forEach(function(b) {
      html += '<li class="boundary-item">' + lcssEscapeHtml(b) + '</li>';
    });
    html += '</ul>';
    html += '<h4>Known Non-Proofs</h4>';
    html += '<ul class="lcss-non-proof-list">';
    LCSS_KNOWN_NON_PROOFS.forEach(function(np) {
      html += '<li class="muted">' + lcssEscapeHtml(np) + '</li>';
    });
    html += '</ul>';
    html += '<p class="boundary-note">claim_boundary: ' + lcssEscapeHtml(LCSS_CLAIM_BOUNDARY) + '</p>';
    html += '</div>';
    return html;
  }

  function lcssInit() {
    /* Config status panel */
    lcssSetContent('lcss-config-status-content', lcssRenderLocalConfigStatus());

    /* Unsafe block list panel */
    lcssSetContent('lcss-unsafe-block-list-content', lcssRenderUnsafeBlockList());

    /* Redaction status panel */
    lcssSetContent('lcss-redaction-status-content', lcssRenderRedactionStatus());

    /* Provider disabled-by-default panel */
    lcssSetContent('lcss-provider-disabled-content', lcssRenderProviderDisabledByDefault());

    /* Proof boundaries panel */
    lcssSetContent('lcss-proof-boundaries-content', lcssRenderProofBoundaries());
  }

  /* Initialise when DOM is ready */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', lcssInit);
  } else {
    lcssInit();
  }

  /* Export for validator scan */
  window.LCSS_CLAIM_BOUNDARY = LCSS_CLAIM_BOUNDARY;
  window.LCSS_PROOF_BOUNDARIES = LCSS_PROOF_BOUNDARIES;
  window.LCSS_SAFE_CONFIG_DEFAULTS = SAFE_CONFIG_DEFAULTS;
  window.LCSS_UNSAFE_BLOCK_LIST = UNSAFE_BLOCK_LIST;

})();
