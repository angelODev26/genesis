# genesis

Sistema meta para generar equipos de agentes especializados en proyectos personales de desarrollo de software.

## ¿Qué es esto?

Este repositorio (`genesis/`) es la **capa meta** de un sistema de dos capas:

1. **Capa meta (`genesis/`)** — aquí. Contiene agentes genéricos cuyo único trabajo es auditar, entrevistar y **escribir** los agentes especializados de un proyecto. No desarrollan código de negocio.
2. **Capa proyecto (`<nombre-proyecto>/`)** — carpeta hermana generada por este sistema. Contiene agentes ya especializados en el lenguaje, stack y dominio reales del proyecto. Son los que desarrollan, revisan y testean.

Una vez generados, los agentes especializados **no dependen de `genesis/`** para su trabajo diario.

---

## Cómo se usa

Desde una sesión de Claude Code u OpenCode abierta en esta carpeta (o en el directorio padre que contenga a `genesis/` y a los proyectos), ejecuta:

```
/new-project <nombre-del-proyecto>
```

Esto dispara el flujo completo coordinado por los agentes de esta capa meta.

También está disponible `/verify <ruta-del-proyecto>` para auditar un proyecto ya generado (ver "Verificación y protección de la capa meta").

---

## Los tres casos del flujo

### Caso 1: proyecto nuevo (greenfield)

1. El usuario ejecuta `/new-project <nombre>`.
2. Los agentes genéricos revisan si existe algo en `intake/` y hacen una breve entrevista de afinación (incluida la **plataforma de agentes**: Claude Code, OpenCode o Ambos).
3. Sugieren stack/dominio con trade-offs explícitos; el usuario confirma o ajusta.
4. Se genera la carpeta hermana `<nombre>/` con los agentes especializados ya instalados.
5. **Fin del trabajo de la capa meta.**
6. El usuario abre una **nueva sesión directamente en la carpeta del proyecto generado** (si la plataforma es OpenCode, esa sesión debe arrancarse tras la generación para que cargue los agentes). Desde ahí, los agentes especializados manejan su propio ciclo de planeación y ejecución.

### Caso 2: proyecto existente ajeno a genesis (brownfield externo)

1. El usuario ejecuta `/new-project <nombre>` apuntando a una carpeta existente sin agentes de genesis.
2. `code-auditor` analiza el código actual primero (usando Repomix si está disponible) para entender stack, convenciones y arquitectura.
3. La entrevista cubre solo lo que el código no revela (incluida la plataforma de agentes).
4. Los agentes especializados se instalan **dentro** del proyecto existente.
5. Como primer paso pendiente, los agentes especializados deben generar un **baseline spec** documentando el comportamiento actual antes de cualquier cambio nuevo.
6. Todo cambio posterior se propone como delta contra ese baseline.

### Caso 3: proyecto ya generado por genesis, agregando capa (brownfield interno)

1. El usuario quiere añadir una capa de stack que el proyecto no tenía (por ejemplo, un frontend para un backend existente) y ejecuta `/new-project` con el nombre del mismo proyecto.
2. `code-auditor` detecta los agentes especializados existentes; la(s) plataforma(s) queda(n) determinada(s) por la(s) carpeta(s) y no se vuelve(n) a preguntar. El análisis de código se enfoca en lo que no está cubierto.
3. La entrevista cubre únicamente la capa faltante.
4. `agent-writer` agrega **solo** los agentes de la nueva capa — sin modificar, duplicar ni sobrescribir los existentes, y verificando colisiones de nombre.
5. Se actualiza el README del proyecto reflejando la capa agregada. **Fin del trabajo de la capa meta.**

---

## Modelo de orquestación en la capa proyecto

Los proyectos generados **no incluyen un agente orquestador**. La orquestación es una propiedad del sistema, no un agente más:

- **La sesión principal** (Claude Code / OpenCode) orquesta el trabajo: lee la petición del usuario y delega al subagente adecuado. Su mecanismo de despacho son las `description:` de los agentes — por eso deben ser diferenciadas y precisas (ver `core/agent-template.md`).
- **OpenSpec** orquesta el proceso de desarrollo (ciclo propose → apply → archive).
- Los agentes especializados **no se invocan entre sí** salvo necesidad explícita; cada uno declara su alcance para evitar solapamientos.

Esta ausencia es una decisión de diseño deliberada: un orquestador intermediario duplicaría al agente principal de la sesión, añadiría un salto con pérdida de contexto y crearía dos capas compitiendo por la misma responsabilidad.

---

## Plataformas soportadas: Claude Code y OpenCode

Cada proyecto generado tiene **una o dos plataformas de agentes**, elegidas por el usuario durante la entrevista (nunca asumidas): Claude Code, OpenCode, o **Ambos**. Si se elige Ambos, `agent-writer` genera el mismo equipo dos veces — una variante estricta por plataforma, con los mismos nombres y descripciones en ambas carpetas. Las dos carpetas no colisionan (cada herramienta solo lee la suya) y pueden cohabitar sin conflicto; el costo real es el mantenimiento doble del proyecto generado en adelante.

> **Caso pendiente no implementado aún** — para evitar inyectar complejidad sin necesidad: "agregar plataforma" a un proyecto brownfield interno de una sola plataforma (por ejemplo, proyecto nacido en Claude Code al que luego se le quiere añadir `.opencode/agents/`). Si aparece, `agent-writer`/`orchestrator` lo reportan como pendiente en lugar de improvisar.

La elección determina dónde y con qué formato estricto `agent-writer` escribe los agentes:

| | Claude Code | OpenCode |
|---|---|---|
| Ubicación | `.claude/agents/<nombre>.md` | `.opencode/agents/<nombre>.md` |
| Nombre del agente | campo `name:` (kebab-case, único) | nombre del archivo |
| Frontmatter clave | `name`, `description`, `tools` (allowlist), `model` (alias: `haiku`/`sonnet`/`opus`) | `description`, `mode: subagent`, `permission` (allow/ask/deny), `model` (`proveedor/modelo`) |
| Incompatibilidades | No tiene `mode`/`permission` | **No tiene `tools:`** — campos desconocidos se ignoran silenciosamente |
| Activación | inmediata | requiere reiniciar la sesión de opencode |

Las dos variantes estrictas viven en `core/agent-template.md`. **Nunca se mezclan campos entre plataformas.**

En proyectos ya generados (brownfield interno), la(s) plataforma(s) quedan determinadas por la(s) carpeta(s) de agentes existente(s) y no se vuelven a preguntar.

---

## `intake/` — requerimientos opcionales

La carpeta `genesis/intake/` es **propiedad del usuario**: aquí colocas tus archivos `.md` con requerimientos funcionales o no funcionales **antes** de iniciar el flujo.

- Los agentes de genesis **solo leen** esta carpeta — nunca escriben, crean ni mueven archivos en ella.
- Si existe contenido, los agentes genéricos lo usan como fuente de verdad y acortan la entrevista a solo lo ambiguo.
- Si no existe, la entrevista parte de cero.
- Aplica igual para proyectos nuevos y existentes.

---

## Estructura de este repositorio

```
genesis/
├── AGENTS.md                # contexto auto-cargado (OpenCode lee este archivo al arrancar)
├── .claude/
│   ├── agents/              # agentes genéricos de la capa meta (formato Claude Code)
│   │   ├── orchestrator.md
│   │   ├── code-auditor.md
│   │   ├── requirements-interviewer.md
│   │   ├── stack-advisor.md
│   │   └── agent-writer.md
│   └── commands/
│       ├── new-project.md   # /new-project (Claude Code)
│       └── verify.md        # /verify (Claude Code)
├── .opencode/
│   ├── agents/              # los mismos agentes meta (formato OpenCode, espejos regenerables)
│   └── commands/
│       ├── new-project.md   # /new-project (OpenCode)
│       └── verify.md        # /verify (OpenCode)
├── core/
│   ├── principles.md        # buenas prácticas universales
│   ├── agent-template.md    # plantilla base (dos variantes: Claude Code / OpenCode)
│   └── interview-playbooks.md # áreas de decisión obligatorias por capa (front/back/móvil)
├── tools/
│   ├── verify-project.py        # verificación determinística de proyectos generados (solo lectura)
│   ├── sync-opencode-mirrors.py # regenera/valida los espejos .opencode/ desde .claude/
│   └── hooks/
│       └── pre-commit       # resincroniza espejos automáticamente (copiar a .git/hooks/)
├── intake/                  # SOLO LECTURA — propiedad del usuario (ignorado por git)
├── decisions/               # ADRs de la capa meta
└── README.md                # este archivo
```

---

## Verificación y protección de la capa meta

- **`/verify <ruta-del-proyecto>`** — verificación determinística y de solo lectura sobre cualquier proyecto generado: frontmatter estricto por plataforma, unicidad de nombres, prohibición de mezcla de campos, simetría en proyectos "Ambos", presencia de `core/principles.md` y de `openspec/`. Nada de esto depende de un LLM: es `tools/verify-project.py`, y `agent-writer` lo ejecuta como paso obligatorio post-generación.
- **Protección de espejos**: los fuentes de verdad son `.claude/agents/*.md`; los `.opencode/agents/*.md` se regeneran con `tools/sync-opencode-mirrors.py`. El hook `tools/hooks/pre-commit` (instalar copiándolo a `.git/hooks/pre-commit`) lo corre en cada commit y resincroniza automáticamente si hay drift.

---

## ¿Y después?

Una vez el proyecto especializado está generado:

1. **Cierra o abandona la sesión actual de `genesis/`**.
2. **Abre una nueva sesión (Claude Code u OpenCode, según la plataforma elegida) en la carpeta del proyecto generado** (`../<nombre-proyecto>/`).
3. Invoca los comandos de ese proyecto (por ejemplo, su propio ciclo OpenSpec) para empezar a trabajar.

Los agentes especializados ya saben tu stack, tu dominio y tus convenciones. La capa meta no vuelve a entrar en juego salvo que decidas regenerar completamente el equipo de agentes desde cero.
