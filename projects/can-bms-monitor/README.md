# CAN BMS Monitor

## Scope
- Multi-ID CAN frame parser (`0x180..0x183`)
- Pack/cell/temperature/current state tracking
- Warning flag derivation from threshold rules

## Firmware Quality Points
- Endian-safe parsing helpers
- Centralized warning rule evaluation
- Structured state with freshness timestamp

## Verification Checklist
1. Each CAN ID updates only its designated fields.
2. Over/under thresholds toggle correct warning bits.
3. Signed current/temperature parsing is correct.
