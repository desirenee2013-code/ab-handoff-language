from __future__ import annotations
from pathlib import Path
import shlex

from .model import (
    Boundary,
    Branch,
    HandoffType,
    MutationAttempt,
    Program,
    Route,
    Scope,
    Widen,
)


class ParseError(ValueError):
    pass


def _csv(value: str) -> tuple[str, ...]:
    if value in {"", "none", "-"}:
        return ()
    return tuple(x for x in (part.strip() for part in value.split(",")) if x)


def _kv(tokens: list[str], line_no: int) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            raise ParseError(f"line {line_no}: expected key=value, got {token!r}")
        key, value = token.split("=", 1)
        out[key] = value
    return out


def parse_text(text: str) -> Program:
    p = Program()
    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tokens = shlex.split(line)
        kind = tokens[0]

        if kind == "runtime":
            if len(tokens) != 2:
                raise ParseError(f"line {line_no}: runtime requires one name")
            p.runtime = tokens[1]
            continue

        if len(tokens) < 2:
            raise ParseError(f"line {line_no}: {kind} requires a name")
        name = tokens[1]
        args = _kv(tokens[2:], line_no)

        if kind == "scope":
            p.scopes[name] = Scope(
                name=name,
                ground=args.get("ground", "local"),
                capabilities=_csv(args.get("capabilities", "")),
                accepts=_csv(args.get("accepts", "")),
            )
        elif kind == "handoff":
            p.handoffs[name] = HandoffType(
                name=name,
                fields=_csv(args.get("fields", "")),
                authority=args.get("authority", "none"),
            )
        elif kind == "boundary":
            p.boundaries[name] = Boundary(
                name=name,
                source=args["from"],
                destination=args["to"],
                allow=_csv(args.get("allow", "")),
                provenance=args.get("provenance", "required"),
            )
        elif kind == "branch":
            p.branches[name] = Branch(
                name=name,
                owner=args["owner"],
                accepts=args["accepts"],
                returns=args["returns"],
            )
        elif kind == "route":
            p.routes[name] = Route(
                name=name,
                source=args["from"],
                destination=args["to"],
                boundary=args["via"],
                handoff=args["handoff"],
            )
        elif kind == "widen":
            p.widens[name] = Widen(
                name=name,
                parent=args["parent"],
                inherit=args.get("inherit", "none"),
                add=_csv(args.get("add", "")),
                reconnect=args["reconnect"],
            )
        elif kind == "mutate":
            target = args["target"]
            if not target.endswith(".ground"):
                raise ParseError(f"line {line_no}: mutate target must be SCOPE.ground")
            p.mutations.append(
                MutationAttempt(name=name, source=args["from"], target_scope=target[:-7])
            )
        else:
            raise ParseError(f"line {line_no}: unknown statement {kind!r}")

    return p


def parse_file(path: str | Path) -> Program:
    return parse_text(Path(path).read_text(encoding="utf-8"))
