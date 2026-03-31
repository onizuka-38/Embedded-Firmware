# Common Engineering Standards

## Branching
- Use short-lived feature branches per milestone.
- Keep commits scoped to one verified change.

## Definition of Done
- Build succeeds in CI and locally.
- Unit/integration tests for changed logic pass.
- Hardware test notes are written in `docs/`.
- Risk and rollback notes are updated.

## Traceability
- Every task maps to a requirement ID.
- Every verification result maps to a test ID.

## Artifact Rules
- `docs/`: architecture, decisions, plans, reports
- `firmware/`: target code only
- `hardware/`: pin map, schematic, BOM
- `sim/` or `ml/`: simulation or model pipeline assets
