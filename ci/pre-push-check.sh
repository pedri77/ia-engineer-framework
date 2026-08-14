#!/usr/bin/env bash
# pre-push-check.sh — Verificacion completa antes de push
#
# Ejecuta lint, tests, context check y security scan.
# Solo permite push si todos pasan.
#
# Instalacion como git hook:
#   cp ci/pre-push-check.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
#
# Uso manual:
#   bash ci/pre-push-check.sh

set -euo pipefail

echo "=== Pre-push checks ==="
echo ""

# 1. Lint (configura segun tu proyecto)
echo "[1/4] Lint..."
# Descomenta el que aplique:
# npm run lint
# ruff check .
echo "  (sin lint configurado — edita ci/pre-push-check.sh)"
echo ""

# 2. Tests
echo "[2/4] Tests..."
# Descomenta el que aplique:
# npm test
# pytest -x --tb=short
echo "  (sin tests configurados — edita ci/pre-push-check.sh)"
echo ""

# 3. Context check
echo "[3/4] Context check..."
if [ -f "hooks/context-check.py" ]; then
  python3 hooks/context-check.py .
else
  echo "  hooks/context-check.py no encontrado — skip"
fi
echo ""

# 4. Security scan
echo "[4/4] Security scan..."
if [ -f "hooks/security-scan.py" ]; then
  python3 hooks/security-scan.py
else
  echo "  hooks/security-scan.py no encontrado — skip"
fi
echo ""

echo "=== Todos los checks pasaron ==="
