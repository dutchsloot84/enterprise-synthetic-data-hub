"""Shim for backward compatibility. Use src/api/api_server.py instead."""
from src.api.api_server import app, main

if __name__ == "__main__":  # pragma: no cover
    main()
