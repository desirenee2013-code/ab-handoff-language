from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Scope:
    name: str
    ground: str = "local"
    capabilities: tuple[str, ...] = ()
    accepts: tuple[str, ...] = ()


@dataclass(frozen=True)
class HandoffType:
    name: str
    fields: tuple[str, ...] = ()
    authority: str = "none"


@dataclass(frozen=True)
class Boundary:
    name: str
    source: str
    destination: str
    allow: tuple[str, ...] = ()
    provenance: str = "required"


@dataclass(frozen=True)
class Branch:
    name: str
    owner: str
    accepts: str
    returns: str


@dataclass(frozen=True)
class Route:
    name: str
    source: str
    destination: str
    boundary: str
    handoff: str


@dataclass(frozen=True)
class Widen:
    name: str
    parent: str
    inherit: str
    add: tuple[str, ...]
    reconnect: str


@dataclass(frozen=True)
class MutationAttempt:
    name: str
    source: str
    target_scope: str


@dataclass
class Program:
    runtime: str | None = None
    scopes: dict[str, Scope] = field(default_factory=dict)
    handoffs: dict[str, HandoffType] = field(default_factory=dict)
    boundaries: dict[str, Boundary] = field(default_factory=dict)
    branches: dict[str, Branch] = field(default_factory=dict)
    routes: dict[str, Route] = field(default_factory=dict)
    widens: dict[str, Widen] = field(default_factory=dict)
    mutations: list[MutationAttempt] = field(default_factory=list)
