#!/usr/bin/env python3
"""Verificación determinística (solo lectura) de proyectos generados por genesis.

Valida, sin depender de ningún LLM:
- Presencia de carpeta(s) de agentes (.claude/agents/ y/o .opencode/agents/).
- Frontmatter estricto por plataforma (sin mezcla de campos entre variantes).
- Unicidad de nombres y descripciones no vacías.
- Reglas de `model:` por plataforma (alias vs. proveedor/modelo).
- Simetría de nombres cuando el proyecto usa Ambos.
- Presencia de core/principles.md y del directorio openspec/.

Uso:
    python3 tools/verify-project.py <ruta-del-proyecto>

Exit code: 0 = sin errores (las advertencias no fallan), 1 = hay errores.
Nota: parseo de frontmatter minimalista a propósito (solo claves de nivel 0);
los valores en bloque (description: |) se tratan como "presente y no vacío".
"""

import re
import sys
from pathlib import Path

CLAUDE_DIR = ".claude/agents"
OPENCODE_DIR = ".opencode/agents"

FORBIDDEN_IN_CLAUDE = {"mode", "permission"}
FORBIDDEN_IN_OPENCODE = {"tools"}

KNOWN_CLAUDE_MODELS = {"haiku", "sonnet", "opus", "inherit"}
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(path, errors):
    """Devuelve dict de claves de nivel 0 del frontmatter, o None si es inválido."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: el frontmatter debe abrir con '---' en la primera línea")
        return None
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        errors.append(f"{path}: frontmatter sin línea de cierre '---'")
        return None
    meta = {}
    for line in lines[1:end]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue  # valor anidado (permission:, lista, bloque escalar): ignorar
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta


def check_claude_agents(root, errors, warnings):
    names = []
    for path in sorted(root.glob("*.md")):
        meta = parse_frontmatter(path, errors)
        if meta is None:
            continue
        name = meta.get("name", "")
        if not name:
            errors.append(f"{path}: falta 'name' (obligatorio en Claude Code)")
        elif not KEBAB_RE.match(name):
            errors.append(f"{path}: 'name' '{name}' no es kebab-case")
        else:
            names.append(name)
        if "description" not in meta:
            errors.append(f"{path}: falta 'description' (regla de despacho)")
        mixed = FORBIDDEN_IN_CLAUDE & set(meta)
        if mixed:
            errors.append(f"{path}: campos de OpenCode en variante Claude Code: {sorted(mixed)}")
        model = meta.get("model", "")
        if model and model not in KNOWN_CLAUDE_MODELS:
            warnings.append(f"{path}: 'model' '{model}' no es un alias conocido (haiku/sonnet/opus)")
    dups = {n for n in names if names.count(n) > 1}
    if dups:
        errors.append(f"Nombres duplicados en {CLAUDE_DIR}: {sorted(dups)}")
    return names


def check_opencode_agents(root, errors, warnings):
    names = []
    for path in sorted(root.glob("*.md")):
        meta = parse_frontmatter(path, errors)
        if meta is None:
            continue
        names.append(path.stem)  # en OpenCode el nombre ES el archivo
        if "description" not in meta:
            errors.append(f"{path}: falta 'description' (regla de despacho)")
        mixed = FORBIDDEN_IN_OPENCODE & set(meta)
        if mixed:
            errors.append(f"{path}: campos de Claude Code en variante OpenCode: {sorted(mixed)}")
        mode = meta.get("mode", "")
        if mode != "subagent":
            warnings.append(f"{path}: 'mode' es '{mode or '(ausente)'}', se espera 'subagent'")
        model = meta.get("model", "")
        if model and "/" not in model:
            errors.append(f"{path}: 'model' '{model}' sin prefijo de proveedor (ej. 'anthropic/...')")
    return names


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 tools/verify-project.py <ruta-del-proyecto>", file=sys.stderr)
        sys.exit(2)

    project = Path(sys.argv[1]).resolve()
    errors, warnings = [], []

    if not project.is_dir():
        print(f"ERROR: '{project}' no existe o no es un directorio", file=sys.stderr)
        sys.exit(1)

    claude_root = project / CLAUDE_DIR
    opencode_root = project / OPENCODE_DIR
    has_claude = claude_root.is_dir()
    has_opencode = opencode_root.is_dir()

    if not has_claude and not has_opencode:
        print(f"ERROR: '{project}' no tiene {CLAUDE_DIR}/ ni {OPENCODE_DIR}/ — no es genesis-origin", file=sys.stderr)
        sys.exit(1)

    claude_names, opencode_names = [], []
    if has_claude:
        claude_names = check_claude_agents(claude_root, errors, warnings)
    if has_opencode:
        opencode_names = check_opencode_agents(opencode_root, errors, warnings)

    ambiguous = "Ambos" if (has_claude and has_opencode) else ("Claude Code" if has_claude else "OpenCode")
    if has_claude and has_opencode:
        only_c = sorted(set(claude_names) - set(opencode_names))
        only_o = sorted(set(opencode_names) - set(claude_names))
        if only_c or only_o:
            errors.append(f"Asimetría en proyecto 'Ambos': solo en Claude Code: {only_c or '—'}; solo en OpenCode: {only_o or '—'}")

    if not (project / "core" / "principles.md").is_file():
        warnings.append("No se encontró core/principles.md en el proyecto")
    if not (project / "openspec").is_dir():
        warnings.append("No se encontró el directorio openspec/ (¿se ejecutó 'openspec init'?)")

    print(f"Verificación de: {project}")
    print(f"Plataforma(s): {ambiguous}")
    print(f"Agentes: Claude Code={len(claude_names)} OpenCode={len(opencode_names)}")
    for w in warnings:
        print(f"  ⚠ {w}")
    for e in errors:
        print(f"  ✗ {e}")
    if errors:
        print(f"\nRESULTADO: ❌ {len(errors)} error(es), {len(warnings)} advertencia(s)")
        sys.exit(1)
    print(f"\nRESULTADO: ✅ OK ({len(warnings)} advertencia(s))")
    sys.exit(0)


if __name__ == "__main__":
    main()
