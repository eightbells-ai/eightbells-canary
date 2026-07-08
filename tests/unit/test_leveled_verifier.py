"""
Unit tests for the LeveledVerifier with L4 reconciliation logic.
"""

import pytest
from src.eightbells.verification.leveled_verifier import (
    LeveledVerifier,
    ProbeLevel,
    ProbeResult,
    ProbeOutcome,
    ReconciliationDecision
)


class TestLeveledVerifierReconciliation:
    """Unit tests for L4 reconciliation logic in LeveledVerifier."""
    
    def test_reconciliation_l4_fail_l0_l2_pass(self):
        """
        Test reconciliation when L4 fails but L0-L2 all pass.
        
        Expected: reconciliation applied, progression allowed.
        """
        verifier = LeveledVerifier()
        
        # Add passing empirical tests
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS,
            message="Unit tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS,
            message="Integration tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        
        # Add failing L4
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L4,
            result=ProbeResult.FAIL,
            message="User goal not met"
        ))
        
        # Verify
        result = verifier.verify()
        
        # Should allow progression
        assert result is True
        
        # Check reconciliation decision
        assert verifier.reconciliation_decision is not None
        assert verifier.reconciliation_decision.l4_failed is True
        assert verifier.reconciliation_decision.l0_l2_all_passed is True
        assert verifier.reconciliation_decision.reconciliation_applied is True
        assert verifier.reconciliation_decision.blocks_progression is False
    
    def test_reconciliation_l4_fail_l0_fail(self):
        """
        Test reconciliation when L4 fails and L0 fails.
        
        Expected: reconciliation not applied, progression blocked.
        """
        verifier = LeveledVerifier()
        
        # L0 fails
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.FAIL,
            message="Unit tests fail"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS,
            message="Integration tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        
        # L4 fails
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L4,
            result=ProbeResult.FAIL,
            message="User goal not met"
        ))
        
        # Verify
        result = verifier.verify()
        
        # Should block progression
        assert result is False
        
        # Check reconciliation decision
        assert verifier.reconciliation_decision is not None
        assert verifier.reconciliation_decision.l4_failed is True
        assert verifier.reconciliation_decision.l0_l2_all_passed is False
        assert verifier.reconciliation_decision.reconciliation_applied is False
        assert verifier.reconciliation_decision.blocks_progression is True
    
    def test_reconciliation_l4_fail_l1_absent(self):
        """
        Test reconciliation when L4 fails and L1 is absent.
        
        Expected: reconciliation not applied, progression blocked.
        """
        verifier = LeveledVerifier()
        
        # L1 is absent
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS,
            message="Unit tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        
        # L4 fails
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L4,
            result=ProbeResult.FAIL,
            message="User goal not met"
        ))
        
        # Verify
        result = verifier.verify()
        
        # Should block progression
        assert result is False
        
        # Check reconciliation decision
        assert verifier.reconciliation_decision is not None
        assert verifier.reconciliation_decision.l4_failed is True
        assert verifier.reconciliation_decision.l0_l2_all_passed is False
        assert verifier.reconciliation_decision.reconciliation_applied is False
        assert verifier.reconciliation_decision.blocks_progression is True
    
    def test_reconciliation_l4_pass_no_reconciliation_needed(self):
        """
        Test that no reconciliation is applied when L4 passes.
        """
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS,
            message="Unit tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS,
            message="Integration tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L4,
            result=ProbeResult.PASS,
            message="User goal met"
        ))
        
        # Verify
        result = verifier.verify()
        
        # Should allow progression
        assert result is True
        
        # Check reconciliation decision
        assert verifier.reconciliation_decision is not None
        assert verifier.reconciliation_decision.l4_failed is False
        assert verifier.reconciliation_decision.reconciliation_applied is False
        assert verifier.reconciliation_decision.blocks_progression is False
    
    def test_reconciliation_l4_absent_no_reconciliation_needed(self):
        """
        Test that no reconciliation is applied when L4 is absent.
        """
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS,
            message="Unit tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS,
            message="Integration tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        
        # Verify
        result = verifier.verify()
        
        # Should allow progression
        assert result is True
        
        # Check reconciliation decision
        assert verifier.reconciliation_decision is not None
        assert verifier.reconciliation_decision.l4_failed is False
        assert verifier.reconciliation_decision.reconciliation_applied is False
        assert verifier.reconciliation_decision.blocks_progression is False
    
    def test_check_empirical_levels_pass_all_present_and_pass(self):
        """Test _check_empirical_levels_pass when all L0-L2 pass."""
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS
        ))
        
        assert verifier._check_empirical_levels_pass() is True
    
    def test_check_empirical_levels_pass_one_fails(self):
        """Test _check_empirical_levels_pass when one level fails."""
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.FAIL
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS
        ))
        
        assert verifier._check_empirical_levels_pass() is False
    
    def test_check_empirical_levels_pass_one_absent(self):
        """Test _check_empirical_levels_pass when one level is absent."""
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS
        ))
        
        assert verifier._check_empirical_levels_pass() is False
    
    def test_get_verification_summary_includes_reconciliation(self):
        """Test that verification summary includes reconciliation info."""
        verifier = LeveledVerifier()
        
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L0,
            result=ProbeResult.PASS,
            message="Unit tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L1,
            result=ProbeResult.PASS,
            message="Integration tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L2,
            result=ProbeResult.PASS,
            message="E2E tests pass"
        ))
        verifier.add_probe_outcome(ProbeOutcome(
            level=ProbeLevel.L4,
            result=ProbeResult.FAIL,
            message="User goal not met"
        ))
        
        verifier.verify()
        
        summary = verifier.get_verification_summary()
        
        assert "outcomes" in summary
        assert len(summary["outcomes"]) == 4
        assert "reconciliation" in summary
        assert summary["reconciliation"]["reconciliation_applied"] is True
