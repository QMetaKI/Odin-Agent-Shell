# Odin Windows Host Handoff v0.8.6

This folder is a Windows handoff candidate. It prepares launch, dev install, daemon start, hub opening, diagnostics and service/tray stubs.

Boundary:
- no Windows service proof is claimed here
- no tray proof is claimed here
- no MSIX/winget/code-signing proof is claimed here
- all scripts are developer handoff candidates until executed on a Windows host

Recommended Codex/host sequence:
1. Run `install_dev.ps1` from the repo root.
2. Run `run_odin.ps1`.
3. Run `start_daemon.ps1`.
4. Run `open_hub.ps1`.
5. Run `emit_support_bundle.ps1`.
6. Convert service/tray stubs only after CLI and local API are green on target host.
