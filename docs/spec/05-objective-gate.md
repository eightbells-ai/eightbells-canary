# §5 Objective Gate / Leveled Verification

## Overview

The Objective Gate implements a multi-level verification system that determines whether a change can progress based on evidence from different verification levels. The system recognizes five levels of verification:

- **L0**: Unit tests (empirical, code-level)
- **L1**: Integration tests (empirical, system-level)
- **L2**: End-to-end tests (empirical, user-facing)
- **L3**: Specification proofs (formal)
- **L4**: UserGoal probes (aspirational, user intent)

## Verification Levels

### Empirical Levels (L0-L2)

The empirical levels provide concrete, executable evidence that the implementation behaves correctly:

- **L0 (Unit)**: Tests individual functions and components in isolation
- **L1 (Integration)**: Tests interactions between components and subsystems
- **L2 (E2E)**: Tests complete user-facing workflows and scenarios

These levels are considered the strongest evidence of correctness because they directly execute and observe the implementation's behavior.

### Formal Level (L3)

L3 provides formal proofs that the implementation satisfies its specification. These proofs are mechanically verified and provide mathematical certainty about specific properties.

### Aspirational Level (L4)

L4 UserGoal probes attempt to verify that the implementation meets high-level user intent and goals. These probes are aspirational in nature—they represent desired outcomes that may be difficult to fully capture or verify mechanically.

## L4 Reconciliation

### Motivation

L4 probes are inherently aspirational and may fail even when the implementation is correct. They attempt to capture user intent, which is often:

- Subjective or context-dependent
- Difficult to formalize completely
- Subject to interpretation
- Evolving over time

Meanwhile, empirical tests (L0-L2) provide strong, concrete evidence that the implementation works correctly for specific, well-defined scenarios.

### Reconciliation Logic

The gate implements **L4 reconciliation** to balance aspirational goals with empirical evidence:

1. **L4 fails, L0-L2 all pass** → **Allow progression**
   - The empirical evidence (L0-L2) demonstrates that the implementation works correctly
   - The L4 failure is logged with reconciliation decision
   - Progression is allowed based on strong empirical evidence
   - Rationale: Empirical test evidence overrides aspirational probe failure

2. **L4 fails, any L0-L2 fail or absent** → **Block progression**
   - Without complete empirical evidence, L4 failure is treated as blocking
   - The implementation has not demonstrated correctness at the empirical levels
   - Both L4 and empirical evidence indicate problems
   - Rationale: Insufficient evidence to override L4 failure

3. **L4 passes** → **Allow progression** (normal case)
   - No reconciliation needed
   - All verification levels agree

### Logging and Observability

When L4 reconciliation is applied, the system logs:

- The L4 failure message and details
- The reconciliation decision and rationale
- The state of all L0-L2 probes
- Whether progression was allowed or blocked

This provides full visibility into reconciliation decisions for audit and debugging.

## Gate Evaluation

The gate evaluation process:

1. Collect probe results from all levels
2. Check non-L4 levels for failures
3. Apply L4 reconciliation logic
4. Log reconciliation decision if applicable
5. Return final progression decision

## Example Scenarios

### Scenario 1: L4 Reconciliation Applied

```
L0: PASS - All unit tests pass
L1: PASS - All integration tests pass
L2: PASS - All E2E tests pass
L4: FAIL - User goal "intuitive workflow" not fully met

Decision: ALLOW PROGRESSION
Reason: L4 failed but L0-L2 all passed; empirical evidence overrides L4
```

### Scenario 2: L4 Reconciliation Not Applied (Blocking)

```
L0: PASS - All unit tests pass
L1: FAIL - Integration test timeout
L2: PASS - All E2E tests pass
L4: FAIL - User goal not met

Decision: BLOCK PROGRESSION
Reason: L4 failed and L0-L2 not all passing; blocking progression
```

### Scenario 3: No Reconciliation Needed

```
L0: PASS - All unit tests pass
L1: PASS - All integration tests pass
L2: PASS - All E2E tests pass
L4: PASS - User goal met

Decision: ALLOW PROGRESSION
Reason: All levels pass; no reconciliation needed
```

## Implementation

The reconciliation logic is implemented in:

- `src/eightbells/verification/leveled_verifier.py` - Core verification logic
- `src/eightbells/gates/objective_gate.py` - Gate implementation

See the code for detailed implementation and logging behavior.
