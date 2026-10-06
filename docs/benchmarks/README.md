# RelayBoard Benchmarks

Status: PILOT SCENARIOS FROZEN

The first pilot benchmark consists of three scenarios:

- [S01 Tiny Reversible Change](./S01_TINY_CHANGE.md)
- [S02 Ambiguous Requirement](./S02_AMBIGUOUS_REQUIREMENT.md)
- [S04 Deterministic Hard Bug](./S04_HARD_BUG.md)

The evaluator protocol and scoring rules are:

- [Evaluator Protocol v0](./EVALUATOR_PROTOCOL_V0.md)
- [Scoring v0](./SCORING_V0.md)

## Full-workflow arms

The system-level comparison uses four frozen arms:

1. Neutral/plain agent control.
2. Pinned pstack workflow.
3. Pinned Matt Pocock workflow.
4. FIRST-mode v0.

Mechanism-isolation experiments may add narrower arms, but they must use the same frozen scenario start state and oracle.

## Freeze rule

After the first controlled run begins, do not change:

- scenario prompt;
- starting commit;
- operator oracle;
- oracle intent;
- scoring rubric;
- acceptance behavior.

Any substantive change creates a new scenario version and a new round.
