# Related architectures — structural neighbors, not identity claims

ABHL is not built from a blank slate. Several established programming traditions already preserve parts of the same shape. This file exists to keep **borrowed scaffolding != native A/B structure** explicit.

## Actor systems

Actor-model systems isolate local state and communicate through messages rather than shared mutable state. This is close to ABHL's `scope` + typed handoff discipline.

What ABHL adds at the present scaffold layer is A/B-specific bookkeeping around target/layer resolution, branch ownership, result -> re-grounding, and temporary widening/reconnection.

Examples:

- Pony: https://github.com/ponylang/ponyc
- Ensemble (small typed actor framework): https://github.com/d-buckner/ensemble

## Object-capability / secure-compartment systems

Endo/SES and Agoric are particularly close to the **availability != authority** side of the architecture. Compartments receive only explicitly endowed capabilities, and communication across isolated execution contexts is controlled.

Important difference: object-capability systems may intentionally pass capabilities. ABHL v0.2 currently freezes the opposite test constraint for its handoff records: `authority=none`.

Examples:

- Endo / SES: https://github.com/endojs/endo
- Agoric SwingSet / vats: https://github.com/Agoric/agoric-sdk

## Capability RPC

Cap'n Proto combines typed schemas with capability-based RPC. It is a strong neighbor for typed cross-boundary calls and receiver-facing interfaces.

Difference: Cap'n Proto messages can intentionally carry capability references. ABHL currently keeps handoff data and reusable authority separate.

- Cap'n Proto: https://github.com/capnproto/capnproto

## Capability microkernels

seL4 is a much lower-level relative: explicit capabilities and controlled IPC isolate authority and component state. It is useful as a security-architecture comparison, not as an A/B implementation model.

- seL4: https://github.com/seL4/seL4

## Durable workflows

Temporal gives another partial neighbor: durable, replayable workflows with typed calls and message handlers, where changed durable state affects subsequent execution.

Difference: Temporal is primarily workflow orchestration. It does not supply A/B's distinction-resolution / typed-handoff / widened-reconnection semantics.

- Temporal Python SDK: https://github.com/temporalio/sdk-python

## Current conclusion

The pieces are established. The **exact combination** currently being tested in ABHL is not being claimed as novel, and this small survey cannot establish uniqueness.

The useful comparison is:

```text
actor isolation
+ explicit capability separation
+ typed cross-boundary handoff
+ receiver-owned semantics
+ result -> re-ground recurrence
+ temporary widening without privilege growth
+ A/B-specific OPEN / PINNED / handoff discipline
```

The first four have strong existing relatives. The latter A/B-specific recurrence and widening rules are where this scaffold should be compared most carefully against existing systems before making any novelty claim.
