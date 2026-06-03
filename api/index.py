"""
Vercel Serverless Entry Point
-----------------------------
This module exposes the FastAPI app to Vercel's Python runtime.
Vercel expects a module-level ASGI `app` object or a handler function.
"""
import os
import sys

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Signal to the app that we're running in serverless mode
os.environ.setdefault("VERCEL", "1")

from app.main import app  # noqa: E402, F401

# Vercel picks up the `app` variable automatically as an ASGI handler.
