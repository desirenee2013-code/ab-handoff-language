# ABHL v0.2 Specification

## 1. Purpose

ABHL is a boundary-and-handoff language for the candidate A/B runtime.

It exists so the programming layer can be attacked with executable invariants without turning A/B itself into a general-purpose language.

The language describes **who owns local semantics, what may cross a boundary, and what must not be smuggled across with it**.

## 2. Non-goals

ABHL is not:

- the language of every resolved branch;
- a replacement for Python, SQL, mathematics, chemistry notation, etc.;
- a universal decomposition oracle;
- a truth engine;
- a permission-minting system;
- proof that the present scaffold is A/B's final native computational form.

## 3. Core programming-layer entities

### 3.1 `runtime`
Names one ABHL manifest.

```abhl
runtime ci_demo
```

### 3.2 `scope`
Declares a locally bounded runtime context.

```abhl
scope dependency ground=local capabilities=inspect_repo accepts=ci_failure
```

Properties:

- `ground` must be `local` in v0.2;
- `capabilities` are externally supplied abilities already available to the scope;
- `accepts` lists handoff types the scope can receive.

A scope owns its Local Ground. Another scope may not directly mutate it.

### 3.3 `handoff`
Declares a typed transfer payload.

```abhl
handoff integration_handoff fields=target,constraints,provenance,return_route authority=none
```

`authority=none` is mandatory in v0.2.

A handoff may carry data about an intended operation. It does not carry receiver-owned meaning or reusable authority.

### 3.4 `boundary`
Declares a legal crossing between two scopes.

```abhl
boundary dep_to_integration from=dependency to=integration allow=integration_handoff provenance=required
```

A boundary validates crossing. It does not own branch semantics.

### 3.5 `branch`
Declares receiver-owned branch semantics.

```abhl
branch integration_check owner=integration accepts=integration_handoff returns=integration_result
```

The branch belongs to its owner. The sender does not dictate how the branch interprets the handoff internally.

### 3.6 `route`
Declares a typed path through one boundary.

```abhl
route dep_handoff from=dependency to=integration via=dep_to_integration handoff=integration_handoff
```

The route is valid only when:

- boundary source equals route source;
- boundary destination equals route destination;
- boundary allows the handoff type;
- destination scope accepts the handoff type.

### 3.7 `widen`
Declares a temporary widened scope used when a local loop cannot reconnect.

```abhl
widen environment_repair parent=dependency inherit=capabilities add=none reconnect=dependency
```

In v0.2:

- widened scopes may inherit existing capabilities;
- they may add **no** capabilities;
- widening therefore cannot function as privilege escalation.

The runtime semantics expected above this declaration remain:

```text
A/B -> handoff -> branch -> re-ground -> A/B again -> reconnect
```

The widened scope must complete that local recurrence before reconnecting.

### 3.8 `mutate`
`mutate` exists only as an explicit attack surface in v0.2 so the validator can reject forbidden remote Ground mutation.

```abhl
mutate bad_write from=dependency target=integration.ground
```

A scope may refer to its own Ground internally, but cross-scope Ground mutation is illegal.

## 4. Frozen invariants

### I1 — Local Ground ownership

```text
scope A cannot directly mutate scope B's Ground
```

### I2 — Crossing does not transfer semantics

```text
sender payload != receiver semantics
```

### I3 — Crossing does not transfer authority

```text
handoff data != capability grant
```

### I4 — Widening does not increase privilege

```text
widened scope != privilege escalation
```

### I5 — Boundary validates crossing, not branch truth

```text
boundary validity != branch validity
```

### I6 — Result is not Ground by itself

A branch result may participate in re-grounding. It does not automatically replace Local Ground.

## 5. Grammar — v0.2 line form

ABHL deliberately starts with a small line-oriented grammar.

```text
runtime NAME
scope NAME ground=local capabilities=CSV accepts=CSV
handoff NAME fields=CSV authority=none
boundary NAME from=NAME to=NAME allow=CSV provenance=required|optional
branch NAME owner=NAME accepts=NAME returns=NAME
route NAME from=NAME to=NAME via=NAME handoff=NAME
widen NAME parent=NAME inherit=capabilities|none add=none reconnect=NAME
mutate NAME from=NAME target=NAME.ground
```

Blank lines and `# comments` are ignored.

## 6. Why the language is intentionally small

The method layer is already dense. ABHL should earn every construct by preserving a distinction whose collapse would matter to validity, handoff, authority, or recoverability.

If a future construct cannot pass that test, it should remain outside the language.
