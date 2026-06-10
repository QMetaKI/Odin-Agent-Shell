# Windows IPC Endpoint Contracts v7.1

## Purpose

Define endpoint classes before implementation so Codex does not invent unsafe local communication patterns.

## Endpoint classes

### Named pipe endpoint

Used for host, daemon, tray and hub. Must use local machine identity and scoped permissions. Must reject unauthenticated clients.

### Localhost HTTP endpoint

Used for app bridges. Must bind to loopback only. Must require pairing token and caller manifest reference.

### WebSocket update endpoint

Optional. Used only for Hub status streams. Must not accept work submission unless routed through the same auth and boundary gates.

## Forbidden endpoints

- public WAN binding;
- LAN binding by default;
- anonymous control endpoint;
- seed-pack-driven endpoint creation;
- model-generated endpoint creation;
- plugin-created endpoint;
- endpoint that can apply app state.

## Endpoint family table

| Family | Transport | Auth | Allowed use |
|---|---|---|---|
| host-daemon | named pipe | local scoped token | lifecycle and status |
| hub-daemon | named pipe/WebSocket | local scoped token | UI state and commands |
| app-bridge | localhost HTTP | pairing token | Universal Work and candidate returns |
| support-export | local file | user-approved export | diagnostics bundle |

## Failure states

- `endpoint_bind_denied`
- `pairing_token_invalid`
- `caller_manifest_missing`
- `unauthorized_capability`
- `loopback_binding_failed`
- `unsupported_transport`
- `external_binding_blocked`
