"""
Leveled verification system with L4 reconciliation.

This module implements a multi-level verification system where:
- L0: Unit tests (empirical, code-level)
- L1: Integration tests (empirical, system-level)
- L2: End-to-end tests (empirical, user-facing)
- L3: Specification proofs (formal)
- L4: UserGoal probes (aspirational, user intent)

L4 reconciliation: When L4 fails but L0-L2 all pass, the L4 failure is logged
but does not block progression. This recognizes that empirical test evidence
(L0-L2) provides strong signal that the implementation is correct, while L4
probes may be aspirational or imperfect in capturing user intent.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)


class ProbeLevel(Enum):
    """Verification levels in the proof system."""
    L0 = "L0_unit"
    L1 = "L1_integration"
    L2 = "L2_e2e"
    L3 = "L3_spec"
    L4 = "L4_usergoal"


class ProbeResult(Enum):
    """Result of a verification probe."""
    PASS = "pass"
    FAIL = "fail"
    ABSENT = "absent"


@dataclass
class ProbeOutcome:
    """Outcome of a single verification probe."""
    level: ProbeLevel
    result: ProbeResult
    message: Optional[str] = None
    details: Optional[Dict] = None


@dataclass
class ReconciliationDecision:
    """Decision made during L4 reconciliation."""
    l4_failed: bool
    l0_l2_all_passed: bool
    reconciliation_applied: bool
    blocks_progression: bool
    reason: str


class LeveledVerifier:
    """
    Verifier that implements leveled verification with L4 reconciliation.
    
    The reconciliation logic:
    1. If L4 fails AND all L0-L2 pass → log L4 failure, allow progression
    2. If L4 fails AND any L0-L2 fail/absent → block progression
    3. If L4 passes → allow progression (normal case)
    """
    
    def __init__(self):
        self.probe_outcomes: List[ProbeOutcome] = []
        self.reconciliation_decision: Optional[ReconciliationDecision] = None
    
    def add_probe_outcome(self, outcome: ProbeOutcome) -> None:
        """Add a probe outcome to the verification results."""
        self.probe_outcomes.append(outcome)
        logger.debug(f"Added probe outcome: {outcome.level.value} = {outcome.result.value}")
    
    def get_outcome_by_level(self, level: ProbeLevel) -> Optional[ProbeOutcome]:
        """Get the probe outcome for a specific level."""
        for outcome in self.probe_outcomes:
            if outcome.level == level:
                return outcome
        return None
    
    def _check_empirical_levels_pass(self) -> bool:
        """
        Check if all empirical levels (L0-L2) pass.
        
        Returns True only if all L0, L1, and L2 are present and pass.
        """
        empirical_levels = [ProbeLevel.L0, ProbeLevel.L1, ProbeLevel.L2]
        
        for level in empirical_levels:
            outcome = self.get_outcome_by_level(level)
            if outcome is None or outcome.result != ProbeResult.PASS:
                return False
        
        return True
    
    def _apply_l4_reconciliation(self) -> ReconciliationDecision:
        """
        Apply L4 reconciliation logic.
        
        Returns a ReconciliationDecision that determines whether progression
        should be blocked.
        """
        l4_outcome = self.get_outcome_by_level(ProbeLevel.L4)
        
        # If L4 is not present or passes, no reconciliation needed
        if l4_outcome is None:
            return ReconciliationDecision(
                l4_failed=False,
                l0_l2_all_passed=False,
                reconciliation_applied=False,
                blocks_progression=False,
                reason="L4 probe absent, no reconciliation needed"
            )
        
        if l4_outcome.result == ProbeResult.PASS:
            return ReconciliationDecision(
                l4_failed=False,
                l0_l2_all_passed=False,
                reconciliation_applied=False,
                blocks_progression=False,
                reason="L4 probe passed, no reconciliation needed"
            )
        
        # L4 failed - check empirical levels
        l0_l2_all_passed = self._check_empirical_levels_pass()
        
        if l0_l2_all_passed:
            # L4 failed but L0-L2 all pass → reconciliation applies
            logger.warning(
                "L4 reconciliation: L4 UserGoal probe failed but all empirical "
                "tests (L0-L2) passed. Allowing progression based on empirical evidence. "
                f"L4 failure: {l4_outcome.message}"
            )
            return ReconciliationDecision(
                l4_failed=True,
                l0_l2_all_passed=True,
                reconciliation_applied=True,
                blocks_progression=False,
                reason="L4 failed but L0-L2 all passed; empirical evidence overrides L4"
            )
        else:
            # L4 failed and L0-L2 not all passing → block progression
            logger.error(
                "L4 reconciliation: L4 UserGoal probe failed and empirical tests "
                "(L0-L2) did not all pass. Blocking progression. "
                f"L4 failure: {l4_outcome.message}"
            )
            return ReconciliationDecision(
                l4_failed=True,
                l0_l2_all_passed=False,
                reconciliation_applied=False,
                blocks_progression=True,
                reason="L4 failed and L0-L2 not all passing; blocking progression"
            )
    
    def verify(self) -> bool:
        """
        Run verification with L4 reconciliation.
        
        Returns True if progression should be allowed, False if blocked.
        """
        # Check all non-L4 levels first
        all_pass = True
        for outcome in self.probe_outcomes:
            if outcome.level != ProbeLevel.L4:
                if outcome.result == ProbeResult.FAIL:
                    logger.error(f"{outcome.level.value} failed: {outcome.message}")
                    all_pass = False
        
        # Apply L4 reconciliation
        self.reconciliation_decision = self._apply_l4_reconciliation()
        
        # Log reconciliation decision
        if self.reconciliation_decision.reconciliation_applied:
            logger.info(
                f"L4 reconciliation decision: {self.reconciliation_decision.reason}"
            )
        
        # Determine final result
        if self.reconciliation_decision.blocks_progression:
            return False
        
        # If L4 reconciliation doesn't block, check other levels
        return all_pass
    
    def get_verification_summary(self) -> Dict:
        """Get a summary of verification results including reconciliation."""
        summary = {
            "outcomes": [
                {
                    "level": outcome.level.value,
                    "result": outcome.result.value,
                    "message": outcome.message
                }
                for outcome in self.probe_outcomes
            ]
        }
        
        if self.reconciliation_decision:
            summary["reconciliation"] = {
                "l4_failed": self.reconciliation_decision.l4_failed,
                "l0_l2_all_passed": self.reconciliation_decision.l0_l2_all_passed,
                "reconciliation_applied": self.reconciliation_decision.reconciliation_applied,
                "blocks_progression": self.reconciliation_decision.blocks_progression,
                "reason": self.reconciliation_decision.reason
            }
        
        return summary
