from __future__ import annotations
from dataclasses import asdict
from .model import Program
from .validator import require_valid


def compile_manifest(program: Program) -> dict:
    require_valid(program)
    return {
        "runtime": program.runtime,
        "scopes": {k: asdict(v) for k, v in program.scopes.items()},
        "handoffs": {k: asdict(v) for k, v in program.handoffs.items()},
        "boundaries": {k: asdict(v) for k, v in program.boundaries.items()},
        "branches": {k: asdict(v) for k, v in program.branches.items()},
        "routes": {k: asdict(v) for k, v in program.routes.items()},
        "widens": {k: asdict(v) for k, v in program.widens.items()},
    }
