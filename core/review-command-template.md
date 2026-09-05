# Template del comando `/review` — proyectos generados

`agent-writer` copia este comando al proyecto generado cuando incluye el agente de calidad/review (comportamiento por defecto, salvo descarte explícito en la entrevista). Hay **dos variantes estrictas**, una por plataforma — misma regla que `agent-template.md`: nunca mezclar expresiones entre plataformas.

## Placeholders a resolver

- `[AGENTE-REVIEW]`: el `name:`/archivo del agente de calidad generado para ese proyecto (ej. `quality-guardian`, `code-reviewer`). Debe coincidir exactamente con el agente real generado.
- `[ARCHIVOS-CONVENCIONES]`: los documentos de convenciones del proyecto que el revisor debe cargar antes de juzgar (ej. `core/principles.md`, `AGENTS.md`, guías de estilo propias).

No dejar ningún placeholder sin resolver antes de terminar la generación.

---

## Variante A — Claude Code (`.claude/commands/review.md`)

```markdown
---
description: Revisión de código post-tarea — invoca a [AGENTE-REVIEW] sobre los archivos tocados. Uso: /review [rutas opcionales]
---

Revisión de código solicitada vía `/review`.

**Alcance:** $ARGUMENTS

Protocolo fijo:

1. **Determina el alcance**:
   - Si `$ARGUMENTS` trae rutas o módulos, revisa solo eso.
   - Si está vacío, revisa el trabajo reciente: cambios sin commitear (`git status --short` + `git diff`); si el working tree está limpio, usa los archivos del último commit (`git diff HEAD~1 --name-only`). Informa qué alcance elegiste y por qué, en una línea.

2. **Carga el contexto de calidad** antes de juzgar nada:
   - `core/principles.md` (pilar base)
   - [ARCHIVOS-CONVENCIONES]

3. **Invoca al subagente `[AGENTE-REVIEW]`** (via herramienta Agent) pasándole: la lista concreta de archivos a revisar, el contexto convencional cargado, y la instrucción de revisar únicamente ese alcance. Pídele evidencia concreta (`archivo:línea` + snippet) por hallazgo, priorizado: seguridad > integridad de datos > mantenibilidad > estilo.

4. **Presenta su reporte** al usuario sin reescribir conclusiones, y cierra con:
   - Veredicto: `OK para avanzar` / `Corregir antes de continuar` / `Hay decisiones que requieren tu input`
   - Si hay hallazgos, propón el siguiente paso recomendado (corregir, posponer como deuda documentada, o descartar con justificación).

**Restricciones:** ni tú ni `[AGENTE-REVIEW]` modifican código en esta revisión. Este comando solo audita y reporta.
```

## Variante B — OpenCode (`.opencode/commands/review.md`)

Idéntica a la variante A salvo en el paso 3, que dice:

    3. **Invoca al subagente `[AGENTE-REVIEW]`** pasándole: […mismo texto…]

(es decir, sin la mención "via herramienta Agent", que es específica de Claude Code).

---

## Notas de generación

- Si el proyecto es **Ambos**, genera las dos variantes con el mismo contenido semántico.
- El agente de review referenciado debe ser de **solo lectura de código** (sin `edit:`/`write:` en sus permisos de modificación de código, o con ellos denegados) — el comando audita, no arregla.
- Si en modo ampliación de capa el proyecto ya tiene un comando `/review`, no lo sobrescribas: verifica que apunte al agente de calidad vigente y reporta su estado.
