#!/usr/bin/env python
"""
Demonstration of L4 reconciliation behavior.

This script shows how the L4 reconciliation logic works in practice.
"""

import logging
from eightbells.gates.objective_gate import ObjectiveGate

# Configure logging to see reconciliation messages
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

print("=" * 70)
print("L4 Reconciliation Demonstration")
print("=" * 70)

# Scenario 1: L4 fails but L0-L2 pass → Reconciliation applied
print("\n--- Scenario 1: L4 Reconciliation Applied ---")
print("L0: PASS, L1: PASS, L2: PASS, L4: FAIL")
print()

gate1 = ObjectiveGate()
gate1.add_probe_result("L0_unit", "pass", "All unit tests passed")
gate1.add_probe_result("L1_integration", "pass", "All integration tests passed")
gate1.add_probe_result("L2_e2e", "pass", "All E2E tests passed")
gate1.add_probe_result("L4_usergoal", "fail", "User goal 'intuitive workflow' not fully met")

result1 = gate1.evaluate()
reconciliation1 = gate1.get_reconciliation_info()

print(f"Result: {'ALLOW PROGRESSION' if result1 else 'BLOCK PROGRESSION'}")
print(f"Reconciliation applied: {reconciliation1['applied']}")
print(f"Reason: {reconciliation1['reason']}")

# Scenario 2: L4 fails and L1 fails → No reconciliation, blocking
print("\n--- Scenario 2: L4 Reconciliation NOT Applied (Blocking) ---")
print("L0: PASS, L1: FAIL, L2: PASS, L4: FAIL")
print()

gate2 = ObjectiveGate()
gate2.add_probe_result("L0_unit", "pass", "All unit tests passed")
gate2.add_probe_result("L1_integration", "fail", "Integration test timeout")
gate2.add_probe_result("L2_e2e", "pass", "All E2E tests passed")
gate2.add_probe_result("L4_usergoal", "fail", "User goal not met")

result2 = gate2.evaluate()
reconciliation2 = gate2.get_reconciliation_info()

print(f"Result: {'ALLOW PROGRESSION' if result2 else 'BLOCK PROGRESSION'}")
print(f"Reconciliation applied: {reconciliation2['applied']}")
print(f"Reason: {reconciliation2['reason']}")

# Scenario 3: All pass → No reconciliation needed
print("\n--- Scenario 3: All Tests Pass (Normal Case) ---")
print("L0: PASS, L1: PASS, L2: PASS, L4: PASS")
print()

gate3 = ObjectiveGate()
gate3.add_probe_result("L0_unit", "pass", "All unit tests passed")
gate3.add_probe_result("L1_integration", "pass", "All integration tests passed")
gate3.add_probe_result("L2_e2e", "pass", "All E2E tests passed")
gate3.add_probe_result("L4_usergoal", "pass", "User goal met")

result3 = gate3.evaluate()
reconciliation3 = gate3.get_reconciliation_info()

print(f"Result: {'ALLOW PROGRESSION' if result3 else 'BLOCK PROGRESSION'}")
print(f"Reconciliation applied: {reconciliation3['applied']}")
print(f"Reason: {reconciliation3['reason']}")

print("\n" + "=" * 70)
print("Summary:")
print("- Scenario 1: L4 failure overridden by empirical evidence (L0-L2)")
print("- Scenario 2: L4 failure blocks when empirical tests also fail")
print("- Scenario 3: No reconciliation needed when all tests pass")
print("=" * 70)
