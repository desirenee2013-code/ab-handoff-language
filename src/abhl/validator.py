from __future__ import annotations
from dataclasses import dataclass
from .model import Program


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str


class ValidationError(ValueError):
    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        super().__init__("\n".join(f"{d.code}: {d.message}" for d in diagnostics))


def validate(program: Program) -> list[Diagnostic]:
    d: list[Diagnostic] = []

    if not program.runtime:
        d.append(Diagnostic("E001", "runtime name is required"))

    for s in program.scopes.values():
        if s.ground != "local":
            d.append(Diagnostic("E100", f"scope {s.name}: ground must be local in v0.2"))

    for h in program.handoffs.values():
        if h.authority != "none":
            d.append(Diagnostic(
                "E201",
                f"handoff {h.name}: authority transfer is forbidden; handoffs carry data, not reusable authority",
            ))

    for boundary in program.boundaries.values():
        if boundary.source not in program.scopes:
            d.append(Diagnostic("E300", f"boundary {boundary.name}: unknown source scope {boundary.source}"))
        if boundary.destination not in program.scopes:
            d.append(Diagnostic("E301", f"boundary {boundary.name}: unknown destination scope {boundary.destination}"))
        for handoff in boundary.allow:
            if handoff not in program.handoffs:
                d.append(Diagnostic("E302", f"boundary {boundary.name}: unknown handoff type {handoff}"))

    for b in program.branches.values():
        if b.owner not in program.scopes:
            d.append(Diagnostic("E400", f"branch {b.name}: unknown owner scope {b.owner}"))
        if b.accepts not in program.handoffs:
            d.append(Diagnostic("E401", f"branch {b.name}: unknown accepted handoff {b.accepts}"))
        if b.returns not in program.handoffs:
            d.append(Diagnostic("E402", f"branch {b.name}: unknown return handoff {b.returns}"))
        owner = program.scopes.get(b.owner)
        if owner and b.accepts not in owner.accepts:
            d.append(Diagnostic(
                "E403",
                f"branch {b.name}: owner {b.owner} does not declare acceptance of handoff {b.accepts}",
            ))

    for r in program.routes.values():
        if r.source not in program.scopes:
            d.append(Diagnostic("E500", f"route {r.name}: unknown source scope {r.source}"))
        if r.destination not in program.scopes:
            d.append(Diagnostic("E501", f"route {r.name}: unknown destination scope {r.destination}"))
        if r.boundary not in program.boundaries:
            d.append(Diagnostic("E502", f"route {r.name}: unknown boundary {r.boundary}"))
        if r.handoff not in program.handoffs:
            d.append(Diagnostic("E503", f"route {r.name}: unknown handoff {r.handoff}"))

        boundary = program.boundaries.get(r.boundary)
        if boundary:
            if boundary.source != r.source or boundary.destination != r.destination:
                d.append(Diagnostic(
                    "E504",
                    f"route {r.name}: route endpoints do not match boundary {boundary.name}",
                ))
            if r.handoff not in boundary.allow:
                d.append(Diagnostic(
                    "E505",
                    f"route {r.name}: boundary {boundary.name} does not allow handoff {r.handoff}",
                ))

        destination = program.scopes.get(r.destination)
        if destination and r.handoff not in destination.accepts:
            d.append(Diagnostic(
                "E506",
                f"route {r.name}: destination {r.destination} does not accept handoff {r.handoff}",
            ))

    for w in program.widens.values():
        if w.parent not in program.scopes:
            d.append(Diagnostic("E600", f"widen {w.name}: unknown parent scope {w.parent}"))
        if w.reconnect not in program.scopes:
            d.append(Diagnostic("E601", f"widen {w.name}: unknown reconnect scope {w.reconnect}"))
        if w.add:
            d.append(Diagnostic(
                "E602",
                f"widen {w.name}: widening cannot add capabilities ({', '.join(w.add)})",
            ))
        if w.inherit not in {"capabilities", "none"}:
            d.append(Diagnostic("E603", f"widen {w.name}: inherit must be capabilities or none"))

    for m in program.mutations:
        if m.source not in program.scopes:
            d.append(Diagnostic("E700", f"mutate {m.name}: unknown source scope {m.source}"))
        if m.target_scope not in program.scopes:
            d.append(Diagnostic("E701", f"mutate {m.name}: unknown target scope {m.target_scope}"))
        if m.source != m.target_scope:
            d.append(Diagnostic(
                "E702",
                f"mutate {m.name}: scope {m.source} may not directly mutate {m.target_scope}.ground; use a typed handoff route",
            ))

    return d


def require_valid(program: Program) -> None:
    diagnostics = validate(program)
    if diagnostics:
        raise ValidationError(diagnostics)
