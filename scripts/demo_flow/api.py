"""Shell helpers that start/stop the Flask demo API."""
from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Tuple

from enterprise_synthetic_data_hub.config import demo_profiles

REPO_ROOT = Path(__file__).resolve().parents[2]
PORT_FILE = REPO_ROOT / ".demo_api_port"
PID_FILE = REPO_ROOT / ".demo_api_pid"
LOG_FILE = REPO_ROOT / ".demo_api.log"
_PROCESS: subprocess.Popen[str] | None = None


def _build_env(profile: demo_profiles.DemoProfile) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("DEMO_PROFILE", profile.name)
    env.setdefault("DEMO_CONFIG_FILE", str(REPO_ROOT / "config" / "demo.yaml"))
    env.setdefault("FLASK_APP", "enterprise_synthetic_data_hub.api.app:app")
    env.setdefault("FLASK_ENV", "production")

    src_path = str(REPO_ROOT / "src")
    python_path = env.get("PYTHONPATH", "")
    if python_path:
        entries = python_path.split(os.pathsep)
        if src_path not in entries:
            env["PYTHONPATH"] = os.pathsep.join([src_path, python_path])
    else:
        env["PYTHONPATH"] = src_path
    return env


def _port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex((host, port)) == 0


def _select_port(host: str, base_port: int, attempts: int = 5) -> int:
    for offset in range(attempts):
        candidate = base_port + offset
        if _port_in_use(host, candidate):
            continue
        return candidate
    raise RuntimeError(f"Unable to find open port between {base_port} and {base_port + attempts - 1}.")


def _flask_command(host: str, port: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "flask",
        "run",
        "--host",
        host,
        "--port",
        str(port),
        "--no-debugger",
        "--no-reload",
    ]


def _write_metadata(port: int, pid: int) -> None:
    PORT_FILE.write_text(str(port), encoding="utf-8")
    PID_FILE.write_text(str(pid), encoding="utf-8")


def _check_health(base_url: str, health_endpoint: str, timeout: float = 5.0) -> None:
    url = f"{base_url.rstrip('/')}{health_endpoint}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310 - demo local call
        resp.read()


def _wait_for_health(base_url: str, health_endpoint: str, process: subprocess.Popen[str]) -> None:
    last_error: Exception | None = None
    deadline = time.time() + 10
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Flask API process exited before passing health check.")
        try:
            _check_health(base_url, health_endpoint)
            return
        except Exception as exc:  # pragma: no cover - transient health probe
            last_error = exc
            time.sleep(0.5)
    raise RuntimeError(f"Flask API failed health check: {last_error}")


def _terminate_pid(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return


def _terminate_process(process: subprocess.Popen[str]) -> None:
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def start_api(profile: demo_profiles.DemoProfile) -> Tuple[str, str]:
    """Start the Flask API via Python for cross-platform compatibility."""

    global _PROCESS
    api_settings = demo_profiles.get_api_settings()
    host = api_settings.host
    base_port = int(os.environ.get("DEMO_API_PORT", api_settings.port))
    port = _select_port(host, base_port)
    base_url = f"http://{host}:{port}"

    env = _build_env(profile)
    command = _flask_command(host, port)
    log_handle = LOG_FILE.open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(
            command,
            cwd=REPO_ROOT,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except Exception:
        log_handle.close()
        raise
    log_handle.close()

    _PROCESS = process
    _write_metadata(port, process.pid)
    try:
        _wait_for_health(base_url, api_settings.health_endpoint, process)
    except Exception:
        stop_api()
        raise

    return base_url, str(port)


def stop_api() -> None:
    """Stop the Flask API if it is running."""

    global _PROCESS
    process = _PROCESS
    _PROCESS = None

    if process and process.poll() is None:
        _terminate_process(process)
    elif PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text(encoding="utf-8").strip())
        except ValueError:
            pid = None
        if pid:
            _terminate_pid(pid)

    for path in (PID_FILE, PORT_FILE):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


__all__ = ["start_api", "stop_api", "PORT_FILE", "PID_FILE", "LOG_FILE", "_flask_command", "_select_port"]
