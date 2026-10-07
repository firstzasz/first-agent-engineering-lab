# Throughput checkpoint

1. Blocking first steps. Read task/method, traced subsystem, baseline public suite, operator pause semantics, and choose the data shape before any implementation. Complete.
2. Independent workstreams. Tests/evidence and production changes are conceptually separable, but the same helper owns the cohesive cross-file feature. Native parallel work is n/a under the frozen serial port.
3. Shared mutable state. Job rows and the local branch are shared. Store is the single pause writer. Only one helper edits at a time; the lead does not edit its assigned files until it finishes.
4. Smallest safe decomposition. One bounded feature owner writes tests and four application modules; the lead reviews and verifies; a later fresh serial helper reviews diff and evidence. This avoids fragmented state ownership for a small feature.
