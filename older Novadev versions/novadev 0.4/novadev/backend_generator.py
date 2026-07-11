from __future__ import annotations

"""Backend project generator for NovaDev 0.4.

The heavy lifting lives in `codegen.py`. This module gives Prototype 0.4 a clear
filename for backend generation while preserving the older `BackendGenerator`
API used by the CLI and tests.
"""

from .codegen import BackendGenerator


__all__ = ["BackendGenerator"]
