"""
Integration tests for L4 reconciliation behavior.

Tests the complete flow of L4 reconciliation through the gate system.
"""

import pytest
from src.eightbells.gates.objective_gate import ObjectiveGate


class TestL4Reconciliation:
    """Test L4 reconciliation in the objective gate."""
    
    def test_l4_fail_with_l0_l2_pass_allows_progression(self):
        """
        Test that L4 failure with all L0-L2 passing allows progression.
        
        This is the core reconciliation case: empirical evidence (L0-L2)
        overrides aspirational L4 probe failure.
        """
        gate = ObjectiveGate()
        
        # All empirical tests pass
        gate.add_probe_result("L0_unit", "pass", "Unit tests passed")
        gate.add_probe_result("L1_integration", "pass", "Integration tests passed")
        gate.add_probe_result("L2_e2e", "pass", "E2E tests passed")
        
        # L4 UserGoal probe fails
        gate.add_probe_result("L4_usergoal", "fail", "User goal not fully met")
        
        # Should allow progression due to reconciliation
        result = gate.evaluate()
        assert result is True, "Should allow progression when L4 fails but L0-L2 pass"
        
        # Check reconciliation was applied
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is True
        assert reconciliation["l4_failed"] is True
        assert reconciliation["l0_l2_all_passed"] is True
    
    def test_l4_fail_with_l0_fail_blocks_progression(self):
        """
        Test that L4 failure with L0 failure blocks progression.
        
        When empirical tests fail, L4 failure should block.
        """
        gate = ObjectiveGate()
        
        # L0 fails
        gate.add_probe_result("L0_unit", "fail", "Unit tests failed")
        gate.add_probe_result("L1_integration", "pass", "Integration tests passed")
        gate.add_probe_result("L2_e2e", "pass", "E2E tests passed")
        
        # L4 also fails
        gate.add_probe_result("L4_usergoal", "fail", "User goal not met")
        
        # Should block progression
        result = gate.evaluate()
        assert result is False, "Should block when L4 fails and L0 fails"
        
        # Check reconciliation was not applied
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is False
        assert reconciliation["l4_failed"] is True
        assert reconciliation["l0_l2_all_passed"] is False
    
    def test_l4_fail_with_l1_absent_blocks_progression(self):
        """
        Test that L4 failure with L1 absent blocks progression.
        
        Missing empirical tests should not allow reconciliation.
        """
        gate = ObjectiveGate()
        
        # L1 is absent
        gate.add_probe_result("L0_unit", "pass", "Unit tests passed")
        gate.add_probe_result("L2_e2e", "pass", "E2E tests passed")
        
        # L4 fails
        gate.add_probe_result("L4_usergoal", "fail", "User goal not met")
        
        # Should block progression
        result = gate.evaluate()
        assert result is False, "Should block when L4 fails and L1 is absent"
        
        # Check reconciliation was not applied
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is False
    
    def test_l4_pass_allows_progression(self):
        """
        Test that L4 passing allows progression (normal case).
        
        No reconciliation needed when L4 passes.
        """
        gate = ObjectiveGate()
        
        gate.add_probe_result("L0_unit", "pass", "Unit tests passed")
        gate.add_probe_result("L1_integration", "pass", "Integration tests passed")
        gate.add_probe_result("L2_e2e", "pass", "E2E tests passed")
        gate.add_probe_result("L4_usergoal", "pass", "User goal met")
        
        result = gate.evaluate()
        assert result is True, "Should allow progression when all tests pass"
        
        # Check no reconciliation needed
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is False
    
    def test_l4_fail_with_l2_fail_blocks_progression(self):
        """
        Test that L4 failure with L2 failure blocks progression.
        """
        gate = ObjectiveGate()
        
        gate.add_probe_result("L0_unit", "pass", "Unit tests passed")
        gate.add_probe_result("L1_integration", "pass", "Integration tests passed")
        gate.add_probe_result("L2_e2e", "fail", "E2E tests failed")
        gate.add_probe_result("L4_usergoal", "fail", "User goal not met")
        
        result = gate.evaluate()
        assert result is False, "Should block when L4 fails and L2 fails"
        
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is False
    
    def test_all_empirical_pass_l4_absent_allows_progression(self):
        """
        Test that missing L4 with passing empirical tests allows progression.
        """
        gate = ObjectiveGate()
        
        gate.add_probe_result("L0_unit", "pass", "Unit tests passed")
        gate.add_probe_result("L1_integration", "pass", "Integration tests passed")
        gate.add_probe_result("L2_e2e", "pass", "E2E tests passed")
        
        result = gate.evaluate()
        assert result is True, "Should allow progression when L4 absent and L0-L2 pass"
        
        reconciliation = gate.get_reconciliation_info()
        assert reconciliation["applied"] is False
