# EXP-0014 staged-screening v0.1 orchestrator handoff

You are the orchestrator, not a contestant.

Read this directory first. Execute **Stage 1 only**. Do not launch any Stage 2 contestant in the same orchestration task unless Stage 1 has finished, all four dispositions are durable, the predeclared continuation rule has been mechanically evaluated, and the resulting authorized Stage 2 run set has been persisted.

Use the inherited frozen S02-v0.1 task and exact M0-M3 mechanism blobs pinned in COHORT.json. Do not modify them.

For every contestant:
- fresh fork_turns=none context;
- request GPT-6.1 Sol / High where supported;
- clean independent-history fixture at frozen Pilot Start State v0.1;
- assigned task + assigned method only;
- no oracle/evaluator/reference solution/Round1/Round2/peer outcome delivery;
- answer only genuinely asked PRODUCT_OR_PREFERENCE questions from the frozen oracle;
- preserve questions, classifications, answers, checkpoints, diffs and tests;
- terminate contestant/helpers before independent hidden evaluation;
- no hidden feedback to same contestant;
- no silent retry of contamination/host failure;
- no merge to main.

After all four Stage 1 dispositions:
1. compute M0 discovery metrics;
2. apply STAGED_PROTOCOL.md exactly;
3. persist SCREENING_DECISION.json with the arithmetic and authorized Stage 2 run IDs;
4. if no mechanism qualifies, stop the cohort as SCREEN_STOP_NO_STRONG_SIGNAL;
5. if any qualify/inconclusive, launch only the predeclared M0 R2/R3 plus qualifying/inconclusive arms' R2/R3, respecting the frozen relative Stage 2 order.

Passing screening or transfer gates never changes FIRST-mode automatically.
