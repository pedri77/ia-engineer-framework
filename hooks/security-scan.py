#!/usr/bin/env python3
"""
Scan de seguridad pre-commit.

Escanea archivos staged en busca de secretos, credenciales y patrones vulnerables.

Instalacion en .claude/settings.json:
{
  "hooks": {
    "PreCommit": [
      {
        "command": "python3 hooks/security-scan.py",
        "description": "Security scan before commit"
      }
    ]
  }
}
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Patrones de secretos (regex, descripcion, severidad)
SECRET_PATTERNS: list[tuple[str, str, str]] = [
    # API keys
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}', "API key detectada", "HIGH"),
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API key", "HIGH"),
    (r'sk-ant-[a-zA-Z0-9\-]{20,}', "Anthropic API key", "HIGH"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token", "HIGH"),
    (r'glpat-[a-zA-Z0-9\-]{20,}', "GitLab Personal Access Token", "HIGH"),

    # Passwords
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{8,}', "Password hardcoded", "HIGH"),
    (r'(?i)(secret|token)\s*[=:]\s*["\'][^"\']{8,}', "Secret/token hardcoded", "HIGH"),

    # AWS
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key", "HIGH"),
    (r'(?i)aws_secret_access_key\s*[=:]\s*[a-zA-Z0-9/+=]{40}', "AWS Secret Key", "HIGH"),

    # Connection strings
    (r'(?i)(postgres|mysql|mongodb)://[^\s"\']+:[^\s"\']+@', "Connection string con credenciales", "HIGH"),

    # Private keys
    (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private key", "HIGH"),

    # Patrones de codigo vulnerable
    (r'eval\s*\(', "eval() detectado", "MEDIUM"),
    (r'exec\s*\(', "exec() detectado", "MEDIUM"),
    (r'(?i)cursor\.execute\s*\(\s*f["\']', "SQL injection potencial (f-string)", "HIGH"),
    (r'(?i)cursor\.execute\s*\(\s*["\'].*%s', "SQL injection potencial (%s)", "MEDIUM"),
    (r'innerHTML\s*=', "innerHTML asignacion directa (XSS potencial)", "MEDIUM"),
]

# Archivos que nunca deberian commitearse
FORBIDDEN_FILES: list[tuple[str, str]] = [
    (".env", "Archivo de variables de entorno"),
    (".env.local", "Archivo de variables de entorno local"),
    (".env.production", "Archivo de variables de entorno produccion"),
    ("credentials.json", "Credenciales JSON"),
    ("service-account.json", "Service account Google"),
    ("id_rsa", "Clave privada SSH"),
    ("id_ed25519", "Clave privada SSH"),
]

# Extensiones que nunca deberian commitearse
FORBIDDEN_EXTENSIONS = {".pem", ".key", ".p12", ".pfx", ".jks"}

# Extensiones a escanear
SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte",
    ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini",
    ".sh", ".bash", ".zsh", ".env", ".md",
}


def get_staged_files() -> list[str]:
    """Obtiene archivos staged para commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
    )
    return [f for f in result.stdout.strip().split("\n") if f]


def scan_file(filepath: str) -> list[dict]:
    """Escanea un archivo en busca de patrones de seguridad."""
    findings = []
    path = Path(filepath)

    # Verificar nombre de archivo prohibido
    for forbidden_name, desc in FORBIDDEN_FILES:
        if path.name == forbidden_name:
            findings.append({
                "file": filepath,
                "line": 0,
                "severity": "HIGH",
                "message": f"Archivo prohibido: {desc}",
                "pattern": forbidden_name,
            })

    # Verificar extension prohibida
    if path.suffix in FORBIDDEN_EXTENSIONS:
        findings.append({
            "file": filepath,
            "line": 0,
            "severity": "HIGH",
            "message": f"Extension prohibida: {path.suffix}",
            "pattern": path.suffix,
        })

    # Escanear contenido
    if path.suffix not in SCAN_EXTENSIONS:
        return findings

    try:
        with open(filepath, "r", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                for pattern, desc, severity in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        # Evitar falsos positivos en comentarios de ejemplo
                        stripped = line.strip()
                        if stripped.startswith("#") and ("ejemplo" in stripped.lower() or "example" in stripped.lower()):
                            continue
                        if "placeholder" in stripped.lower() or "xxx" in stripped.lower():
                            continue

                        findings.append({
                            "file": filepath,
                            "line": line_num,
                            "severity": severity,
                            "message": desc,
                            "content": line.strip()[:100],
                        })
    except (OSError, PermissionError):
        pass

    return findings


def main() -> None:
    staged_files = get_staged_files()
    if not staged_files:
        print("Sin archivos staged.")
        sys.exit(0)

    all_findings: list[dict] = []
    for filepath in staged_files:
        if os.path.exists(filepath):
            all_findings.extend(scan_file(filepath))

    if not all_findings:
        print(f"OK: {len(staged_files)} archivos escaneados. Sin hallazgos de seguridad.")
        sys.exit(0)

    # Mostrar hallazgos
    high_count = sum(1 for f in all_findings if f["severity"] == "HIGH")
    medium_count = sum(1 for f in all_findings if f["severity"] == "MEDIUM")

    print(f"HALLAZGOS DE SEGURIDAD: {len(all_findings)} ({high_count} HIGH, {medium_count} MEDIUM)")
    print()

    for f in sorted(all_findings, key=lambda x: (x["severity"] != "HIGH", x["file"], x["line"])):
        location = f"{f['file']}:{f['line']}" if f["line"] > 0 else f["file"]
        print(f"  [{f['severity']}] {location}: {f['message']}")
        if f.get("content"):
            print(f"         {f['content']}")

    if high_count > 0:
        print(f"\nBLOQUEADO: {high_count} hallazgos HIGH. Corrige antes de commit.")
        sys.exit(1)
    else:
        print(f"\nAVISO: {medium_count} hallazgos MEDIUM. Revisa antes de commit.")
        sys.exit(0)


if __name__ == "__main__":
    main()
