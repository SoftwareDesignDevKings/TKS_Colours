"""
Vercel Serverless Entry Point
-----------------------------
This module exposes the FastAPI app to Vercel's Python runtime.
Vercel expects a module-level ASGI `app` object in api/index.py.
"""
import os
import sys

# Ensure the backend root is on sys.path so `app.*` imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Signal to the app that we're running in serverless mode
os.environ.setdefault("VERCEL", "1")

from app.main import app  # noqa: E402, F401

# Vercel picks up the `app` variable automatically as an ASGI handler.
