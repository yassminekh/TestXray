import unittest
import os
import sys


def run_all_tests():

    # ── Charger et lancer les tests ───────────────────────────────────────────
    loader = unittest.TestLoader()
    suite  = loader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # ── Compter les résultats ─────────────────────────────────────────────────
    total_failed = len(result.failures) + len(result.errors)
    total_passed = result.testsRun - total_failed

    # ── Collecter les noms des tests échoués ──────────────────────────────────
    failed_tests = {}
    for test, traceback in result.failures:
        failed_tests[test._testMethodName] = traceback
    for test, traceback in result.errors:
        failed_tests[test._testMethodName] = traceback

    # ── Collecter tous les tests ──────────────────────────────────────────────
    all_tests = []

    def collect_tests(s):
        for item in s:
            try:
                collect_tests(item)
            except TypeError:
                all_tests.append(item)

    collect_tests(suite)

    # ── Générer le XML manuellement ───────────────────────────────────────────
    xml_lines = []
    xml_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_lines.append(
        f'<testsuites name="ParaBank Login Tests" tests="{result.testsRun}" '
        f'failures="{len(result.failures)}" errors="{len(result.errors)}" skipped="0">'
    )
    xml_lines.append(
        f'  <testsuite name="ParaBank Login Tests" tests="{result.testsRun}" '
        f'failures="{len(result.failures)}" errors="{len(result.errors)}" skipped="0">'
    )

    for test in all_tests:
        method_name = test._testMethodName
        class_name  = test.__class__.__name__

        if method_name in failed_tests:
            xml_lines.append(
                f'    <testcase name="{method_name}" classname="{class_name}" time="1">'
            )
            # Échapper les caractères spéciaux dans le message
            error_msg = failed_tests[method_name] \
                .replace("&", "&amp;") \
                .replace("<", "&lt;") \
                .replace(">", "&gt;") \
                .replace('"', "&quot;")
            xml_lines.append(f'      <failure message="Test Failed">{error_msg}</failure>')
            xml_lines.append('    </testcase>')
        else:
            xml_lines.append(
                f'    <testcase name="{method_name}" classname="{class_name}" time="1"/>'
            )

    xml_lines.append('  </testsuite>')
    xml_lines.append('</testsuites>')

    xml_content = "\n".join(xml_lines)

    # ── Écrire le fichier XML ─────────────────────────────────────────────────
    os.makedirs("reports", exist_ok=True)
    with open("reports/results.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    # ── Afficher le XML généré ────────────────────────────────────────────────
    print("\n====== XML généré ======")
    print(xml_content)

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
