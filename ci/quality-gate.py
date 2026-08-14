#!/usr/bin/env python3
"""
Quality gate: orquesta todos los checks de calidad.

Ejecuta lint, tests, evals, security scan y context check.
Reporta resumen y falla si alguno no pasa.

Uso:
    python3 ci/quality-gate.py
    python3 ci/quality-gate.py --checks lint,tests,security
    python3 ci/quality-gate.py --eval-threshold 0.85
"""

import argparse
import subprocess
import sys
import time

# Checks disponibles y sus comandos
CHECKS = {
    "lint": {
        "name": "Lint",
        "commands": [
            # Descomenta los que apliquen:
            # ["npm", "run", "lint"],
            # ["ruff", "check", "."],
            ["echo", "lint: no configurado"],
        ],
    },
    "tests": {
        "name": "Tests",
        "commands": [
            # Descomenta los que apliquen:
            # ["npm", "test"],
            # ["pytest", "-x", "--tb=short"],
            ["echo", "tests: no configurado"],
        ],
    },
    "security": {
        "name": "Security Scan",
        "commands": [
            ["python3", "hooks/security-scan.py"],
        ],
    },
    "context": {
        "name": "Context Check",
        "commands": [
            ["python3", "hooks/context-check.py", "."],
        ],
    },
    "evals": {
        "name": "Eval CI Gate",
        "commands": [],  # Se configura dinamicamente
    },
}

ALL_CHECKS = list(CHECKS.keys())


def run_check(name: str, commands: list[list[str]]) -> dict:
    """Ejecuta un check y retorna resultado."""
    start = time.time()
    passed = True
    output_lines = []

    for cmd in commands:
        cmd_str = " ".join(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = (result.stdout + result.stderr).strip()
        if output:
            output_lines.append(output[-300:])
        if result.returncode != 0:
            passed = False

    elapsed = round(time.time() - start, 1)
    return {
        "name": name,
        "passed": passed,
        "elapsed_s": elapsed,
        "output": "\n".join(output_lines),
    }


def main():
    parser = argparse.ArgumentParser(description="Quality gate — orquesta checks de calidad")
    parser.add_argument(
        "--checks",
        default=",".join(ALL_CHECKS),
        help=f"Checks a ejecutar, separados por coma. Disponibles: {', '.join(ALL_CHECKS)}",
    )
    parser.add_argument("--eval-threshold", type=float, default=0.8)
    args = parser.parse_args()

    checks_to_run = [c.strip() for c in args.checks.split(",")]

    print("=" * 60)
    print("QUALITY GATE")
    print("=" * 60)
    print(f"Checks: {', '.join(checks_to_run)}")
    print()

    results = []
    for check_name in checks_to_run:
        if check_name not in CHECKS:
            print(f"Check desconocido: {check_name}")
            continue

        check = CHECKS[check_name]
        commands = check["commands"]

        # Skip si no hay comandos (ej. evals sin configurar)
        if not commands and check_name != "evals":
            print(f"[SKIP] {check['name']}: sin comandos configurados")
            continue

        # Para evals, construir comando dinamicamente
        if check_name == "evals":
            import glob
            datasets = glob.glob("eval/datasets/*.jsonl")
            if not datasets:
                print(f"[SKIP] {check['name']}: sin datasets")
                continue
            # Solo verificar si existen resultados previos
            result_files = glob.glob("eval-results/*-results.jsonl")
            if not result_files:
                print(f"[SKIP] {check['name']}: sin resultados previos (ejecuta run-evals.py primero)")
                continue
            commands = [
                ["python3", "eval/runners/ci-gate.py", "--results", rf, "--threshold", str(args.eval_threshold)]
                for rf in result_files
            ]

        print(f"[RUN]  {check['name']}...", end=" ", flush=True)
        result = run_check(check["name"], commands)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} ({result['elapsed_s']}s)")

    # Resumen
    print()
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"{'Check':<25} {'Estado':>8} {'Tiempo':>8}")
    print("-" * 45)

    all_passed = True
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"{r['name']:<25} {status:>8} {r['elapsed_s']:>7.1f}s")
        if not r["passed"]:
            all_passed = False

    print()
    if all_passed:
        print("RESULTADO: PASS — todos los checks pasaron")
        sys.exit(0)
    else:
        failed = [r["name"] for r in results if not r["passed"]]
        print(f"RESULTADO: FAIL — checks fallidos: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
