# §13 Proof Semantics

## Overview

This document defines the semantics of proofs and verification in the Eightbells system, with particular focus on the relationship between different verification levels and how they interact through reconciliation.

## Verification Levels and Their Semantics

### L0: Unit Tests (Empirical)

**Semantics**: Direct execution of individual functions and components with specific inputs, observing outputs and side effects.

**Strength**: High confidence for tested scenarios; limited to code-level behavior.

**Limitations**: 
- Does not verify integration between components
- May miss emergent system-level behaviors
- Coverage is limited to written test cases

### L1: Integration Tests (Empirical)

**Semantics**: Execution of interactions between multiple components or subsystems, verifying that they work together correctly.

**Strength**: Validates component interactions and data flow; catches integration issues.

**Limitations**:
- May not cover all user-facing scenarios
- Can miss end-to-end workflow issues
- Limited to tested integration points

### L2: End-to-End Tests (Empirical)

**Semantics**: Execution of complete user-facing workflows from start to finish, simulating real user interactions.

**Strength**: Highest confidence for user-visible behavior; validates complete workflows.

**Limitations**:
- Expensive to write and maintain
- May be slow to execute
- Coverage limited to scripted scenarios

### L3: Specification Proofs (Formal)

**Semantics**: Mathematical proofs that the implementation satisfies formal specifications, mechanically verified.

**Strength**: Provides mathematical certainty about proven properties; exhaustive for proven properties.

**Limitations**:
- Requires formal specification (which may be incomplete)
- Expensive to create and maintain
- May not cover all relevant properties

### L4: UserGoal Probes (Aspirational)

**Semantics**: Attempts to verify that the implementation meets high-level user intent and goals.

**Nature**: Aspirational and interpretive rather than definitive.

**Strength**: Captures high-level intent; can identify gaps in user experience.

**Limitations**:
- Subjective and context-dependent
- Difficult to formalize completely
- May fail even when implementation is correct
- Subject to interpretation and evolution

## L4 Probe Semantics and Reconciliation

### The Nature of L4 Probes

L4 probes are fundamentally different from empirical tests (L0-L2):

1. **Aspirational vs. Definitive**: L4 probes represent desired outcomes that may be difficult to verify mechanically, while L0-L2 tests provide definitive pass/fail results.

2. **Interpretive vs. Objective**: L4 probes often require interpretation of user intent, while L0-L2 tests have objective success criteria.

3. **Evolving vs. Stable**: L4 goals may evolve as understanding of user needs improves, while L0-L2 tests remain stable for a given implementation.

### Reconciliation Against Empirical Evidence

When L4 probes conflict with empirical test evidence, the system applies **reconciliation** to resolve the conflict:

#### Principle: Empirical Evidence as Ground Truth

The reconciliation logic treats empirical test evidence (L0-L2) as ground truth when it is complete and passing:

- **Complete empirical evidence** = All of L0, L1, and L2 present and passing
- **Incomplete empirical evidence** = Any of L0, L1, or L2 absent or failing

#### Reconciliation Rules

1. **L4 fails + Complete empirical evidence (L0-L2 all pass)**
   - **Decision**: Allow progression
   - **Rationale**: The implementation demonstrably works correctly for concrete, tested scenarios. The L4 failure likely indicates:
     - The L4 probe is too strict or aspirational
     - The L4 probe doesn't fully capture the nuance of user intent
     - The user goal may need refinement
   - **Action**: Log L4 failure with reconciliation decision; allow progression

2. **L4 fails + Incomplete empirical evidence**
   - **Decision**: Block progression
   - **Rationale**: Without complete empirical evidence, we cannot be confident the implementation is correct. The L4 failure may indicate real problems.
   - **Action**: Block progression; require fixing empirical tests or L4 probe

3. **L4 passes**
   - **Decision**: Allow progression (normal case)
   - **Rationale**: No conflict to reconcile
   - **Action**: Standard progression

### Semantic Justification

The reconciliation logic is justified by the semantic properties of each level:

1. **Empirical tests are executable and observable**: They directly demonstrate that the implementation produces correct outputs for specific inputs.

2. **L4 probes are aspirational and interpretive**: They attempt to capture intent that may be imperfectly formalized.

3. **Complete empirical coverage provides strong evidence**: When all three empirical levels pass, we have evidence at:
   - Code level (L0)
   - Integration level (L1)
   - User-facing level (L2)

4. **L4 failure with empirical success suggests probe refinement needed**: The conflict indicates the L4 probe may need adjustment rather than the implementation being wrong.

## Proof Composition

### Horizontal Composition

Proofs at the same level compose horizontally:
- Multiple L0 tests together provide broader coverage
- Multiple L2 scenarios together cover more workflows

### Vertical Composition

Proofs at different levels compose vertically:
- L0 tests support L1 tests (components must work before integration)
- L1 tests support L2 tests (integration must work before E2E)
- L0-L2 together support L4 (empirical evidence supports aspirational goals)

### Reconciliation as Vertical Composition

L4 reconciliation is a form of vertical composition where:
- Lower levels (L0-L2) provide foundational evidence
- Higher level (L4) provides aspirational goals
- Conflicts are resolved in favor of foundational evidence when it is complete

## Observability and Audit

All reconciliation decisions are logged with:
- The L4 failure details
- The state of all L0-L2 probes
- The reconciliation decision and rationale
- Whether progression was allowed or blocked

This provides a complete audit trail for understanding why progression decisions were made.

## Evolution and Refinement

The reconciliation system supports evolution:

1. **L4 probes can be refined** based on reconciliation patterns
2. **Empirical tests can be expanded** to cover gaps identified by L4
3. **User goals can evolve** as understanding improves

The system provides feedback loops for continuous improvement of both tests and goals.
