# genesis — capa meta

`genesis/` es una **capa meta**, no un proyecto de software. Aquí no se desarrolla código de negocio ni se usa OpenSpec. Tu trabajo en este directorio es ejecutar el flujo de generación de agentes especializados para proyectos que vivirán como **carpetas hermanas**.

## Disparador del flujo

- `/new-project <nombre>` — arranca el flujo completo (detección de caso → auditoría → entrevista → stack → generación). Disponible como comando en `.claude/commands/` y `.opencode/commands/`.

## Los tres casos del flujo

1. **Greenfield**: el proyecto no existe — se crea la carpeta hermana desde cero.
2. **Brownfield externo**: proyecto existente ajeno a genesis — se audita y se le añade la capa meta completa.
3. **Brownfield interno (ampliación de capa)**: proyecto ya generado por genesis (tiene `.claude/agents/` o `.opencode/agents/`) — solo se agregan los agentes de la nueva capa, sin tocar los existentes. La plataforma queda determinada por la carpeta existente.

## Reglas duras de esta carpeta

- **`intake/` es propiedad del usuario: solo lectura.** Nunca crear, editar, mover ni borrar archivos ahí. Los agentes solo la leen como fuente de requerimientos.
- **Los proyectos generados tienen una sola plataforma de agentes**: Claude Code (`.claude/agents/`) u OpenCode (`.opencode/agents/`). Nunca mezclar campos de frontmatter entre variantes (`tools:` ↔ `mode:`/`permission:`). Las variantes estrictas viven en `core/agent-template.md`.
- **Las descripciones son la regla de despacho**: la sesión principal delega leyendo `description:`; deben decir qué hace cada agente y cuándo invocarlo a él y no a otro.
- **No se generan agentes orquestadores** en la capa proyecto (decisión de diseño documentada en README).
- **Los principios universales** (`core/principles.md`) se copian tal cual a cada proyecto generado; los agentes especializados los referencian como pilar base.

## Estructura

```
genesis/
├── .claude/agents/     # capa meta, formato Claude Code
├── .opencode/agents/   # capa meta, formato OpenCode (espejo)
├── core/
│   ├── principles.md        # principios universales
│   └── agent-template.md    # dos variantes estrictas (Claude Code / OpenCode)
├── intake/             # SOLO LECTURA — propiedad del usuario
└── decisions/          # ADRs de la capa meta
```

## Detalles

Lee `README.md` para el flujo completo, la comparativa de plataformas y el estado de desarrollo de la capa meta.
