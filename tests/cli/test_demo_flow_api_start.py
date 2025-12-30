from __future__ import annotations

import socket
import sys

import pytest

from scripts.demo_flow import api


def test_repo_root_points_to_project_root():
    assert (api.REPO_ROOT / "pyproject.toml").exists()


def test_flask_command_prefers_python_executable():
    command = api._flask_command("127.0.0.1", 5000)
    assert command[0] == sys.executable
    assert command[1:4] == ["-m", "flask", "run"]
    assert "--host" in command
    assert "--port" in command


def test_select_port_skips_busy_socket(monkeypatch):
    host = "127.0.0.1"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0))
    sock.listen(1)
    busy_port = sock.getsockname()[1]
    try:
        selected = api._select_port(host, busy_port)
    finally:
        sock.close()

    assert selected != busy_port
    assert busy_port <= selected <= busy_port + 4
    assert not api._port_in_use(host, selected)


def test_select_port_raises_when_range_exhausted(monkeypatch):
    monkeypatch.setattr(api, "_port_in_use", lambda host, port: True)
    with pytest.raises(RuntimeError):
        api._select_port("127.0.0.1", 8000, attempts=2)
