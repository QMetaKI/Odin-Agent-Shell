from __future__ import annotations

import socket
from typing import Any

PORTS_CLAIM_BOUNDARY = "local_runtime_ports_candidate_no_kill_no_external"


def check_port_in_use(host: str, port: int) -> dict[str, Any]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return {
                "status": "available",
                "host": host,
                "port": port,
                "claim_boundary": PORTS_CLAIM_BOUNDARY,
            }
        except OSError:
            return {
                "status": "in_use",
                "host": host,
                "port": port,
                "error": f"port {port} on {host} is already in use",
                "guidance": "choose a different port or stop the process using this port",
                "claim_boundary": PORTS_CLAIM_BOUNDARY,
            }


def is_port_available(host: str, port: int) -> bool:
    return check_port_in_use(host, port)["status"] == "available"
