/**
 * Odin Hub JS API Client — local API contract against /v1/*
 *
 * Claim boundary: local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim
 *
 * Defaults to http://127.0.0.1:8877 — localhost-only.
 * Rejects or warns on non-localhost base URLs.
 * No apply() method. No external_send() method.
 * No provider credential methods.
 *
 * not_proven:
 *   - production_readiness
 *   - live_model_inference
 *   - app_state_mutation
 *   - external_send_authority
 */

(function(global) {
  'use strict';

  var DEFAULT_BASE_URL = 'http://127.0.0.1:8877';

  /* ---------------------------------------------------------------- */
  /* Localhost guard                                                    */
  /* ---------------------------------------------------------------- */
  function isLocalhost(url) {
    try {
      var u = new URL(url);
      return (u.hostname === '127.0.0.1' || u.hostname === 'localhost' || u.hostname === '::1');
    } catch (e) {
      return false;
    }
  }

  function OdinApiClient(baseUrl) {
    var resolvedBase = (baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '');
    if (!isLocalhost(resolvedBase)) {
      var msg = 'OdinApiClient: non-localhost base URL is not allowed: ' + resolvedBase +
        '. This client is localhost-only. ' +
        'Claim boundary: local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim';
      if (typeof console !== 'undefined') { console.warn(msg); }
      throw new Error(msg);
    }
    this._base = resolvedBase;
  }

  /* ---------------------------------------------------------------- */
  /* Internal fetch                                                     */
  /* ---------------------------------------------------------------- */
  OdinApiClient.prototype._get = function(path) {
    var url = this._base + path;
    if (!isLocalhost(url)) {
      return Promise.reject(new Error('Blocked non-localhost request: ' + url));
    }
    return fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
      .then(function(r) {
        if (!r.ok) {
          return r.json().catch(function() { return {}; }).then(function(body) {
            var err = new Error('HTTP ' + r.status);
            err.status = r.status;
            err.body = body;
            throw err;
          });
        }
        return r.json();
      });
  };

  /* ---------------------------------------------------------------- */
  /* Public API methods — all read-only, all against /v1/*             */
  /* ---------------------------------------------------------------- */

  /** GET /v1/health — health check */
  OdinApiClient.prototype.getHealth = function() {
    return this._get('/v1/health');
  };

  /** GET /v1/status — runtime status */
  OdinApiClient.prototype.getStatus = function() {
    return this._get('/v1/status');
  };

  /** GET /v1/providers — provider list (read-only) */
  OdinApiClient.prototype.getProviders = function() {
    return this._get('/v1/providers');
  };

  /** GET /v1/proof-gaps — proof gap summary */
  OdinApiClient.prototype.getProofGaps = function() {
    return this._get('/v1/proof-gaps');
  };

  /** GET /v1/events — recent bus events */
  OdinApiClient.prototype.getEvents = function() {
    return this._get('/v1/events');
  };

  /** GET /v1/sessions/:id — candidate session (read-only) */
  OdinApiClient.prototype.getSession = function(sessionId) {
    return this._get('/v1/sessions/' + encodeURIComponent(sessionId));
  };

  /** GET /v1/candidates/:id — candidate artifact (read-only) */
  OdinApiClient.prototype.getCandidate = function(candidateId) {
    return this._get('/v1/candidates/' + encodeURIComponent(candidateId));
  };

  /* ---------------------------------------------------------------- */
  /* Factory / exports                                                  */
  /* ---------------------------------------------------------------- */

  function createOdinApiClient(baseUrl) {
    return new OdinApiClient(baseUrl || DEFAULT_BASE_URL);
  }

  var odinApiClient = {
    OdinApiClient: OdinApiClient,
    createOdinApiClient: createOdinApiClient,
    DEFAULT_BASE_URL: DEFAULT_BASE_URL,
    CLAIM_BOUNDARY: 'local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim',
    NOT_PROVEN: [
      'production_readiness',
      'live_model_inference',
      'app_state_mutation',
      'external_send_authority',
    ],
  };

  /* UMD export */
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = odinApiClient;
  } else if (typeof define === 'function' && define.amd) {
    define(function() { return odinApiClient; });
  } else {
    global.odinApiClient = odinApiClient;
  }

}(typeof globalThis !== 'undefined' ? globalThis : this));
