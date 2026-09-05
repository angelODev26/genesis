# genesis — capa meta

`genesis/` es una **capa meta**, no un proyecto de software. Aquí no se desarrolla código de negocio ni se usa OpenSpec. Tu trabajo en este directorio es ejecutar el flujo de generación de agentes especializados para proyectos que vivirán como **carpetas hermanas**.

## Disparador del flujo

- `/new-project <nombre>` — arranca el flujo completo (detección de caso → auditoría → entrevista → stack → generación → verificación). Disponible como comando en `.claude/commands/` y `.opencode/commands/`.
- `/verify <ruta-del-proyecto>` — verificación determinística y de solo lectura sobre un proyecto ya generado (`tools/verify-project.py`; `agent-writer` también lo corre como paso obligatorio post-generación).

## Los tres casos del flujo

1. **Greenfield**: el proyecto no existe — se crea la carpeta hermana desde cero.
2. **Brownfield externo**: proyecto existente ajeno a genesis — se audita y se le añade la capa meta completa.
3. **Brownfield interno (ampliación de capa)**: proyecto ya generado por genesis (tiene `.claude/agents/` o `.opencode/agents/`) — solo se agregan los agentes de la nueva capa, sin tocar los existentes. La plataforma queda determinada por la carpeta existente.

## Reglas duras de esta carpeta

- **`intake/` es propiedad del usuario: solo lectura.** Nunca crear, editar, mover ni borrar archivos ahí. Los agentes solo la leen como fuente de requerimientos.
- **Los proyectos generados tienen una o dos plataformas de agentes**: Claude Code (`.claude/agents/`), OpenCode (`.opencode/agents/`), o Ambos (el mismo equipo duplicado en las dos variantes, mismo nombre y descripción). Nunca mezclar campos de frontmatter entre variantes (`tools:` ↔ `mode:`/`permission:`). Si un proyecto generado con una sola plataforma quiere después la otra, es el caso pendiente "agregar plataforma" (documentado en README, no implementado — reportarlo, no improvisar). Las variantes estrictas viven en `core/agent-template.md`.
- **Las descripciones son la regla de despacho**: la sesión principal delega leyendo `description:`; deben decir qué hace cada agente y cuándo invocarlo a él y no a otro.
- **Los espejos `.opencode/agents/` son artefactos derivados**: la fuente de verdad es `.claude/agents/`. Tras editar cualquier agente meta, resincroniza con `python3 tools/sync-opencode-mirrors.py` (el hook `tools/hooks/pre-commit` lo hace solo si está instalado en `.git/hooks/`).
- **No se generan agentes orquestadores** en la capa proyecto (decisión de diseño documentada en README).
- **Los principios universales** (`core/principles.md`) se copian tal cual a cada proyecto generado; los agentes especializados los referencian como pilar base.

## Estructura

```
genesis/
├── .claude/agents/     # capa meta, formato Claude Code (fuente de verdad)
├── .opencode/agents/   # capa meta, formato OpenCode (espejo derivado)
├── core/
│   ├── principles.md        # principios universales
│   ├── agent-template.md    # dos variantes estrictas (Claude Code / OpenCode)
│   ├── interview-playbooks.md # checklist de cobertura de la entrevista por capa
│   ├── capability-classes.md  # clasificación de capacidades (agente/comando/skill/script)
│   └── review-command-template.md # plantilla estricta del /review generado por proyecto
├── tools/              # verify-project.py, sync-opencode-mirrors.py, hooks/
├── intake/             # SOLO LECTURA — propiedad del usuario
└── decisions/          # ADRs de la capa meta
```

## Detalles

Lee `README.md` para el flujo completo, la comparativa de plataformas y el estado de desarrollo de la capa meta.
