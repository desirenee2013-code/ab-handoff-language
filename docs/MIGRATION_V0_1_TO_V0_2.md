# Terminology migration: v0.1 -> v0.2

v0.1 used biological scaffolding directly in the programming surface. v0.2 keeps the structural distinctions while translating them into ordinary programming terms.

| v0.1 | v0.2 | Job preserved |
| --- | --- | --- |
| member | scope | locally bounded owner of Local Ground / semantics |
| capsule | handoff | typed material prepared for transfer |
| membrane | boundary | validates a crossing without owning receiver semantics |
| handoff declaration | route | binds source, destination, boundary, and handoff type |
| widened member | widened scope | temporary widened context with no privilege increase |
| ABML | ABHL | A/B Handoff Language |

The change is surface vocabulary, not a change to the underlying architecture.
