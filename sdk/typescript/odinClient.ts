/**
 * Odin SDK Bridge v1 — TypeScript client scaffold.
 *
 * candidate_only: true
 * app_owned_apply: true
 * external_send_default: false
 * localhost_only: true
 *
 * This SDK bridge allows host apps to:
 * - Health-check Odin
 * - Read status and providers
 * - Submit Universal Work (candidate-only result)
 * - Read Candidate Artifacts
 * - Read Sessions
 * - Read local events
 * - Read proof gaps
 *
 * It does NOT provide:
 * - apply() method
 * - externalSend() method
 * - provider credential defaults
 * - WAN/LAN network access
 * - live model inference
 * - app-state mutation
 */

const SDK_BRIDGE_CLAIM_BOUNDARY =
  "sdk_bridge_v1_candidate_only_no_app_apply_no_external_send_no_wan_lan_no_provider_credentials_no_live_model_proof";

const LOCALHOST_HOSTNAMES = new Set(["127.0.0.1", "localhost", "::1"]);

const SDK_BRIDGE_PROOF_BOUNDARIES = [
  "not_production_readiness_certification",
  "not_windows_service_tray_installer_proof",
  "not_signed_installer_proof",
  "not_live_model_inference_proof",
  "not_model_quality_proof",
  "not_security_certification",
  "not_public_network_api_proof",
  "not_app_state_mutation_proof",
  "not_external_send_authority_proof",
  "not_provider_credential_proof",
] as const;

export class OdinSDKError extends Error {
  readonly code: string;
  readonly details: Record<string, unknown>;
  readonly candidate_only = true;
  readonly claim_boundary = SDK_BRIDGE_CLAIM_BOUNDARY;

  constructor(message: string, code = "sdk_error", details: Record<string, unknown> = {}) {
    super(message);
    this.name = "OdinSDKError";
    this.code = code;
    this.details = details;
  }
}

export class OdinSDKBoundaryError extends OdinSDKError {
  constructor(message: string) {
    super(message, "non_localhost_url_blocked");
    this.name = "OdinSDKBoundaryError";
  }
}

function checkLocalhostUrl(baseUrl: string): void {
  const url = new URL(baseUrl);
  const hostname = url.hostname.replace(/^\[|\]$/g, "").toLowerCase();
  if (!LOCALHOST_HOSTNAMES.has(hostname)) {
    throw new OdinSDKBoundaryError(
      `OdinSDKClient baseUrl must resolve to localhost (got ${JSON.stringify(hostname)}). ` +
        "The SDK Bridge is localhost-only by default."
    );
  }
}

export interface UniversalWorkOptions {
  callerManifest?: Record<string, unknown>;
  seedPack?: Record<string, unknown>;
  patternMine?: Record<string, unknown>;
}

export interface OdinSDKClientOptions {
  baseUrl?: string;
  allowNonLocalhost?: boolean;
  timeoutMs?: number;
}

export class OdinSDKClient {
  readonly baseUrl: string;
  readonly timeoutMs: number;

  constructor(options: OdinSDKClientOptions = {}) {
    this.baseUrl = (options.baseUrl ?? "http://127.0.0.1:8877").replace(/\/$/, "");
    this.timeoutMs = options.timeoutMs ?? 10000;
    if (!options.allowNonLocalhost) {
      checkLocalhostUrl(this.baseUrl);
    }
  }

  /** GET /v1/health — runtime health (candidate-only) */
  async health(): Promise<Record<string, unknown>> {
    return this.request("GET", "/v1/health");
  }

  /** GET /v1/status — runtime store status (candidate-only) */
  async status(): Promise<Record<string, unknown>> {
    return this.request("GET", "/v1/status");
  }

  /** GET /v1/providers — provider card list (candidate-only, not live inference proof) */
  async providers(): Promise<Record<string, unknown>> {
    return this.request("GET", "/v1/providers");
  }

  /** POST /v1/universal-work — submit work, receive candidate-only result.
   *  Does NOT apply app state. Does NOT send externally.
   */
  async submitUniversalWork(
    work: Record<string, unknown>,
    options: UniversalWorkOptions = {}
  ): Promise<Record<string, unknown>> {
    const payload: Record<string, unknown> = { work };
    if (options.callerManifest !== undefined) payload.caller_manifest = options.callerManifest;
    if (options.seedPack !== undefined) payload.seed_pack = options.seedPack;
    if (options.patternMine !== undefined) payload.pattern_mine = options.patternMine;
    return this.request("POST", "/v1/universal-work", payload);
  }

  /** GET /v1/sessions/{id} — read session record (candidate-only) */
  async getSession(sessionId: string): Promise<Record<string, unknown>> {
    return this.request("GET", `/v1/sessions/${encodeURIComponent(sessionId)}`);
  }

  /** GET /v1/candidates/{id} — read candidate artifact (candidate-only, app owns apply) */
  async getCandidate(candidateId: string): Promise<Record<string, unknown>> {
    return this.request("GET", `/v1/candidates/${encodeURIComponent(candidateId)}`);
  }

  /** GET /v1/events — read local bus events (candidate-only, local-only) */
  async events(): Promise<Record<string, unknown>> {
    return this.request("GET", "/v1/events");
  }

  /** GET /v1/proof-gaps — read known proof gaps summary */
  async proofGaps(): Promise<Record<string, unknown>> {
    return this.request("GET", "/v1/proof-gaps");
  }

  private async request(
    method: string,
    path: string,
    body?: Record<string, unknown>
  ): Promise<Record<string, unknown>> {
    const url = this.baseUrl + path;
    const init: RequestInit = {
      method,
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      signal: AbortSignal.timeout(this.timeoutMs),
    };
    if (body !== undefined) {
      init.body = JSON.stringify(body);
    }
    const resp = await fetch(url, init);
    const data = (await resp.json()) as Record<string, unknown>;
    if (!resp.ok) {
      throw new OdinSDKError(
        (data.message as string) ?? `HTTP ${resp.status}`,
        (data.code as string) ?? "http_error",
        data
      );
    }
    return data;
  }
}

export { SDK_BRIDGE_CLAIM_BOUNDARY, SDK_BRIDGE_PROOF_BOUNDARIES };
