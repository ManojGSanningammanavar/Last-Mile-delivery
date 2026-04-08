from __future__ import annotations

import os
import socket
import uvicorn
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def find_available_port(host: str, preferred_port: int, max_tries: int = 20) -> int:
    """Return the first available port starting from preferred_port."""
    for port in range(preferred_port, preferred_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        f"No available port found in range {preferred_port}-{preferred_port + max_tries - 1}"
    )


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    preferred_port = int(os.getenv("PORT", "8000"))
    port = find_available_port(host, preferred_port)

    if port != preferred_port:
        print(f"Port {preferred_port} is busy. Starting API on port {port} instead.")

    uvicorn.run("src.main:app", host=host, port=port, reload=False)
