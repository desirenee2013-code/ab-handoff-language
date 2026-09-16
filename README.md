# A/B Handoff Language (ABHL)

**Status:** experimental programming-layer scaffold, v0.2.0

ABHL is a small declarative language for expressing the current A/B programming-layer architecture without pretending to replace branch-native languages.

Its job is narrow: declare **local scopes**, **typed handoffs**, **handoff boundaries**, **receiver-owned branches**, **routes**, and **temporary widened scopes** while preserving the distinctions that matter to the runtime.

> A/B does not replace the language of a resolved branch. It gets the work to the correct branch.

The earlier v0.1 vocabulary borrowed `member`, `capsule`, and `membrane` from the biological scaffold that helped expose the architecture. v0.2 keeps the structure but drops that surface vocabulary.

## Central invariant

> **permit relation without permitting collapse**

ABHL keeps these separate:

- Local Ground != global mutable state
- handoff != direct remote mutation
- payload != destination != permission != receiver semantics
- computational availability != authorization to act
- widened scope != privileged scope
- result != reusable authority
- branch result != new Ground

## Why these names?

A **scope** is a locally bounded runtime context that owns its Local Ground and branch semantics.

A **handoff** is typed data prepared to cross from one scope to another. It does not carry reusable authority in v0.2.

A **boundary** states what may cross between two scopes. It validates the crossing; it does not own branch semantics.

A **route** binds a source, destination, boundary, and handoff type into one declared transfer path.

These are programming terms, not biological claims and not new core A/B ontology.

## Tiny example

```abhl
runtime ci_demo

scope dependency ground=local capabilities=inspect_repo accepts=ci_failure,integration_result
scope integration ground=local capabilities=run_tests accepts=integration_handoff

handoff ci_failure fields=message,provenance authority=none
handoff integration_handoff fields=target,constraints,provenance,return_route authority=none
handoff integration_result fields=result,provenance,source_handoff authority=none

boundary dep_to_integration from=dependency to=integration allow=integration_handoff provenance=required
boundary integration_to_dep from=integration to=dependency allow=integration_result provenance=required

branch integration_check owner=integration accepts=integration_handoff returns=integration_result
route dep_handoff from=dependency to=integration via=dep_to_integration handoff=integration_handoff
route dep_result from=integration to=dependency via=integration_to_dep handoff=integration_result

widen environment_repair parent=dependency inherit=capabilities add=none reconnect=dependency
```

Compile/check it:

```bash
python -m abhl check examples/ci_demo.abhl
python -m abhl compile examples/ci_demo.abhl
```

## What v0.2 deliberately does not decide

ABHL does **not** define:

- a universal candidate generator;
- a universal rule for choosing the correct distinction;
- branch truth/evidence semantics;
- one universal re-ground function;
- one universal widening rule;
- a claim that all systems share one internal mechanism.

Those stay local.

## Executable invariants

The validator currently makes three architecture claims executable:

1. one scope cannot directly mutate another scope's Ground;
2. a handoff cannot transfer reusable semantic authority;
3. a widened scope cannot gain capabilities merely by widening.

These are tested adversarially in `tests/`.

## Repository map

- `src/abhl/` — parser, model, validator, CLI
- `examples/` — valid and deliberately invalid ABHL programs
- `docs/SPEC.md` — language specification
- `docs/VALIDATION_PROTOCOL.md` — frozen adversarial protocol for F1-F10
- `docs/RELATED_ARCHITECTURES.md` — nearby existing programming architectures and the differences that still matter
- `docs/MIGRATION_V0_1_TO_V0_2.md` — terminology migration
- `tests/` — compiler/validator attack tests

## Project note

The software implementation is a **test vehicle**, not proof of the method.

*Deduced by Sherlock Holmes :)*
