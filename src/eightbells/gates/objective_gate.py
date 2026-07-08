"""
Objective gate implementation using leveled verification.

The objective gate determines whether a change can progress based on
verification results across all levels, with L4 reconciliation applied.
"""

import logging
from typing import Dict, List

from ..verification.leveled_verifier import (
    LeveledVerifier,
    ProbeLevel,
    ProbeResult,
    ProbeOutcome
)


logger = logging.getLogger(__name__)


class ObjectiveGate:
    """
    Gate that controls progression based on leveled verification.
    
    Implements the L4 reconciliation policy:
    - When L4 fails but L0-L2 all pass: log and allow progression
    - When L4 fails and any L0-L2 fail/absent: block progression
    """
    
    def __init__(self):
        self.verifier = LeveledVerifier()
    
    def add_probe_result(self, level: str, result: str, message: str = None) -> None:
        """
        Add a probe result to the gate.
        
        Args:
            level: Level name (e.g., "L0_unit", "L4_usergoal")
            result: Result string ("pass", "fail", "absent")
            message: Optional message describing the result
        """
        # Convert string to enum
        level_enum = ProbeLevel(level)
        result_enum = ProbeResult(result)
        
        outcome = ProbeOutcome(
            level=level_enum,
            result=result_enum,
            message=message
        )
        
        self.verifier.add_probe_outcome(outcome)
    
    def evaluate(self) -> bool:
        """
        Evaluate the gate and determine if progression is allowed.
        
        Returns True if progression should be allowed, False otherwise.
        """
        logger.info("Evaluating objective gate with L4 reconciliation")
        result = self.verifier.verify()
        
        summary = self.verifier.get_verification_summary()
        logger.info(f"Gate evaluation complete: {'PASS' if result else 'BLOCK'}")
        logger.debug(f"Verification summary: {summary}")
        
        return result
    
    def get_reconciliation_info(self) -> Dict:
        """Get information about L4 reconciliation decision."""
        if self.verifier.reconciliation_decision:
            return {
                "applied": self.verifier.reconciliation_decision.reconciliation_applied,
                "reason": self.verifier.reconciliation_decision.reason,
                "l4_failed": self.verifier.reconciliation_decision.l4_failed,
                "l0_l2_all_passed": self.verifier.reconciliation_decision.l0_l2_all_passed
            }
        return {"applied": False}
