# Frozen Adversarial Validation Protocol

**Version:** 0.1

This document freezes adjudication rules before running comparative A/B trials.

The purpose is to prevent the evaluator from redefining success after seeing the A/B result.

## 1. Comparison

For each case, compare:

```text
ordinary competent handling
vs.
explicit A/B handling
```

The same case materials, time limits, branch tools, and success criteria must be used for both conditions unless the case explicitly studies one of those variables.

## 2. Blinding and gold records

Before either condition is run, the case designer creates a **gold record** containing:

- true/accepted referent for the case;
- admissible target set;
- admissible layer/unit set;
- branch that owns each admissible operation;
- minimum evidence/distinctions required before handoff;
- provenance facts that must remain recoverable;
- known ambiguity that is intentionally unresolved;
- expected cost ceiling for decomposition when relevant.

Where more than one target/layer is legitimately admissible, the gold record lists the set rather than forcing one answer.

The evaluator scoring traces should not know which condition produced which trace when practical.

## 3. Failure adjudication

### F1 — wrong target accepted
Count F1 when the final accepted target is outside the predeclared admissible target set and the mismatch changes the operation, evidence, handoff, or answer-bearing unit.

### F2 — wrong layer/unit accepted
Count F2 when the accepted layer/unit is outside the predeclared admissible set **and** causes a downstream mismatch in target, operation, evidence, or branch ownership.

A mere naming difference does not count.

### F3 — wrong branch selected
Count F3 when the handoff goes to a branch that does not own the required operation according to the gold record.

### F4 — ill-typed operation licensed
Count F4 when an operation is applied to an operand/unit outside the operation's predeclared domain for the case.

### F5 — live uncertainty silently collapsed
Count F5 when the case marks an uncertainty as unresolved but the trace proceeds as though one alternative were established without recording the uncertainty as OPEN/PINNED/equivalent.

### F6 — provenance distinction lost
Count F6 when the trace can no longer recover a required distinction such as source vs inference, inherited wording vs current wording, or earlier result vs later correction.

### F7 — premature handoff
Before the trial, list the **minimum handoff conditions** for the case. Count F7 when handoff occurs before those conditions are present in the trace.

This does not require the eventual branch conclusion to be correct; it tests whether the handoff was legitimate at the moment it occurred.

### F8 — unnecessary decomposition
Before the trial, declare a cost measure: steps, time, tokens, or interactions.

A decomposition step counts as unnecessary only if removing it would not alter any of:

- accepted target;
- admissible operation;
- relevant evidence;
- branch/handoff;
- uncertainty status;
- recoverability/provenance;

and its cumulative cost exceeds the predeclared threshold.

This prevents "I didn't like the extra steps" from becoming an after-the-fact criterion.

### F9 — arbitrary relabel used to rescue failed loop
Count F9 when a failed reconnection is "repaired" only by assigning a new layer label that does not change target, operation, evidence, branch, or handoff conditions.

### F10 — reachable handoff not reached
The gold record must identify at least one reachable legitimate handoff. Count F10 when the trace terminates or remains unresolved after the case's predeclared resource limit without reaching any admissible handoff.

## 4. Positive outcomes

Do not score "A/B success" as one binary variable.

Record separately whether explicit A/B:

- reduces a specific predeclared failure class;
- increases a specific failure class;
- changes time/step/token cost;
- improves provenance recoverability;
- changes false-resolution rate;
- changes frequency of legitimate OPEN/PINNED outcomes.

Mixed results are valid results.

## 5. Interpretation

```text
same performance
    -> no demonstrated comparative gain on that case

better on predeclared failure classes
    -> evidence for that specific practical contribution

worse / more costly
    -> evidence of cost or over-decomposition

mixed
    -> narrow the claim to the observed tradeoff
```

Internal coherence is not comparative validation.
