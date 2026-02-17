import unittest
import os
import sys
from junit_xml import TestSuite, TestCase as JUnitTestCase


def run_all_tests():

    # ── Charger tous les tests ────────────────────────────────────────────────
    loader = unittest.TestLoader()
    suite  = loader.discover(start_dir="tests", pattern="test_*.py")

    # ── Lancer les tests ──────────────────────────────────────────────────────
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # ── Construire les cas JUnit XML ──────────────────────────────────────────
    junit_cases = []

    # Tests échoués
    for test, traceback in result.failures:
        tc = JUnitTestCase(
            name=test._testMethodName,
            classname=test.__class__.__name__,
            elapsed_sec=0
        )
        tc.add_failure_info(message="FAILURE", output=traceback)
        junit_cases.append(tc)

    # Tests en erreur
    for test, traceback in result.errors:
        tc = JUnitTestCase(
            name=test._testMethodName,
            classname=test.__class__.__name__,
            elapsed_sec=0
        )
        tc.add_error_info(message="ERROR", output=traceback)
        junit_cases.append(tc)

    # Tests réussis
    total_failed = len(result.failures) + len(result.errors)
    total_passed = result.testsRun - total_failed

    for i in range(total_passed):
        tc = JUnitTestCase(
            name=f"passed_test_{i+1}",
            classname="PassedTests",
            elapsed_sec=0
        )
        junit_cases.append(tc)

    # ── Générer le fichier XML ─────────────────────────────────────────────────
    os.makedirs("reports", exist_ok=True)

    ts = TestSuite("ParaBank Login Tests", junit_cases)
    with open("reports/results.xml", "w", encoding="utf-8") as f:
        TestSuite.to_file(f, [ts], prettyprint=True)

    # ── Résumé console ────────────────────────────────────────────────────────
    print("\n" + "="*50)
    print(f"  Tests exécutés : {result.testsRun}")
    print(f"  ✅ Réussis     : {total_passed}")
    print(f"  ❌ Échoués     : {len(result.failures)}")
    print(f"  💥 Erreurs     : {len(result.errors)}")
    print(f"  📄 XML         : reports/results.xml")
    print("="*50)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_all_tests()