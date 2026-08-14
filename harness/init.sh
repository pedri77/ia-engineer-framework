#!/usr/bin/env bash
# init.sh — Inicializacion del entorno de desarrollo
# Ejecuta esto al inicio de cada sesion para verificar que todo funciona.

set -euo pipefail

# ============================================================
# CONFIGURA ESTOS 3 VALORES PARA TU PROYECTO
# ============================================================
INSTALL_CMD="npm install"          # o "pip install -r requirements.txt"
VERIFY_CMD="npm test"              # o "pytest"
START_CMD="npm run dev"            # o "uvicorn main:app --reload"
# ============================================================

echo "=== Directorio actual ==="
pwd

echo ""
echo "=== Instalando dependencias ==="
$INSTALL_CMD

echo ""
echo "=== Verificacion ==="
if $VERIFY_CMD; then
  echo ""
  echo "VERIFICACION OK"
else
  echo ""
  echo "VERIFICACION FALLIDA — corrige antes de continuar"
  exit 1
fi

echo ""
echo "=== Comando de inicio ==="
if [ "${RUN_START_COMMAND:-0}" = "1" ]; then
  echo "Ejecutando: $START_CMD"
  $START_CMD
else
  echo "Para arrancar el servidor: $START_CMD"
  echo "(Establece RUN_START_COMMAND=1 para ejecutar automaticamente)"
fi
