#!/usr/bin/env python3
"""Regenera los espejos .opencode/agents/ de la capa meta desde .claude/agents/.

Las fuentes de verdad son los archivos .claude/agents/*.md. Los .opencode/agents/*.md
son artefactos derivados: se regeneran tomando el cuerpo íntegro y reescribiendo
solo el frontmatter a la variante OpenCode (description + mode + permission).

Uso:
    python3 tools/sync-opencode-mirrors.py           # regenera los espejos
    python3 tools/sync-opencode-mirrors.py --check   # solo valida (exit 1 si hay drift)

Si se agrega un nuevo agente meta, hay que añadirlo a PERMISSIONS abajo.
"""

import re
import sys
from pathlib import Path

CLAUDE_DIR = Path(".claude/agents")
OPENCODE_DIR = Path(".opencode/agents")

# Permisos por agente meta (formato OpenCode: allow / ask / deny).
PERMISSIONS = {
    "orchestrator":             {"edit": "deny",  "bash": "ask",   "webfetch": "deny"},
    "code-auditor":             {"edit": "deny",  "bash": "allow", "webfetch": "deny"},
    "requirements-interviewer": {"edit": "deny",  "bash": "deny",  "webfetch": "deny"},
    "stack-advisor":            {"edit": "deny",  "bash": "deny",  "webfetch": "allow"},
    "agent-writer":             {"edit": "allow", "bash": "allow", "webfetch": "deny"},
}


def render_opencode(name, claude_text):
    _, _, body = claude_text.split("---\n", 2)
    fm = claude_text.split("---\n", 2)[1]
    m = re.search(r"description: \|\n((?: {2}.*\n)+)", fm)
    if not m:
        raise ValueError(f"{name}: no se pudo extraer 'description: |' del frontmatter")
    perms = PERMISSIONS[name]
    new_fm = (
        f"description: |\n{m.group(1)}mode: subagent\n"
        f"permission:\n"
        f"  edit: {perms['edit']}\n"
        f"  bash: {perms['bash']}\n"
        f"  webfetch: {perms['webfetch']}\n"
    )
    return f"---\n{new_fm}---\n{body}"


def main():
    check_only = "--check" in sys.argv
    drifted, ok = [], []

    for src in sorted(CLAUDE_DIR.glob("*.md")):
        name = src.stem
        if name not in PERMISSIONS:
            print(f"  ⚠ {name}: sin entrada en PERMISSIONS — agregarla antes de sincronizar")
            drifted.append(name)
            continue
        expected = render_opencode(name, src.read_text(encoding="utf-8"))
        dst = OPENCODE_DIR / f"{name}.md"
        actual = dst.read_text(encoding="utf-8") if dst.exists() else None
        if actual == expected:
            ok.append(name)
        else:
            drifted.append(name)
            if not check_only:
                dst.write_text(expected, encoding="utf-8")

    # Detectar espejos huérfanos (agente borrado de .claude pero presente en .opencode)
    for dst in sorted(OPENCODE_DIR.glob("*.md")):
        if not (CLAUDE_DIR / dst.name).exists():
            drifted.append(dst.stem)
            if not check_only:
                dst.unlink()
                print(f"  🗑 eliminado espejo huérfano: {dst}")

    if drifted:
        verbo = "desincronizados" if check_only else "resincronizados"
        print(f"{verbo}: {', '.join(sorted(drifted))}")
        if check_only:
            print("Ejecuta `python3 tools/sync-opencode-mirrors.py` para regenerar los espejos.")
            sys.exit(1)
    print(f"OK ({len(ok)} sin cambios, {len(drifted)} {'drift detectado' if check_only else 'actualizados'})")


if __name__ == "__main__":
    main()
