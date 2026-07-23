# genesis

Sistema meta para generar equipos de agentes especializados en proyectos personales de desarrollo de software.

## ¿Qué es esto?

Este repositorio (`genesis/`) es la **capa meta** de un sistema de dos capas:

1. **Capa meta (`genesis/`)** — aquí. Contiene agentes genéricos cuyo único trabajo es auditar, entrevistar y **escribir** los agentes especializados de un proyecto. No desarrollan código de negocio.
2. **Capa proyecto (`<nombre-proyecto>/`)** — carpeta hermana generada por este sistema. Contiene agentes ya especializados en el lenguaje, stack y dominio reales del proyecto. Son los que desarrollan, revisan y testean.

Una vez generados, los agentes especializados **no dependen de `genesis/`** para su trabajo diario.

---

## Cómo se usa

Desde una sesión de Claude Code abierta en esta carpeta (o en el directorio padre que contenga a `genesis/` y a los proyectos), ejecuta:

```
/new-project <nombre-del-proyecto>
```

Esto dispara el flujo completo coordinado por los agentes de esta capa meta.

---

## Flujo nuevo vs. flujo existente

### Proyecto nuevo (greenfield)

1. El usuario ejecuta `/new-project <nombre>`.
2. Los agentes genéricos revisan si existe algo en `intake/` y hacen una breve entrevista de afinación.
3. Sugieren stack/dominio con trade-offs explícitos; el usuario confirma o ajusta.
4. Se genera la carpeta hermana `<nombre>/` con los agentes especializados ya instalados.
5. **Fin del trabajo de la capa meta.**
6. El usuario abre una **nueva sesión de Claude Code directamente en la carpeta del proyecto generado**. Desde ahí, los agentes especializados manejan su propio ciclo de planeación y ejecución.

### Proyecto existente (brownfield)

1. El usuario ejecuta `/new-project <nombre>` apuntando a una carpeta existente.
2. `code-auditor` analiza el código actual primero (usando Repomix si está disponible) para entender stack, convenciones y arquitectura.
3. La entrevista cubre solo lo que el código no revela.
4. Los agentes especializados se instalan **dentro** del proyecto existente.
5. Como primer paso pendiente, los agentes especializados deben generar un **baseline spec** documentando el comportamiento actual antes de cualquier cambio nuevo.
6. Todo cambio posterior se propone como delta contra ese baseline.

---

## `intake/` — requerimientos opcionales

La carpeta `genesis/intake/` está diseñada para que el usuario coloque un archivo `.md` con requerimientos funcionales o no funcionales **antes** de iniciar el flujo.

- Si existe, los agentes genéricos lo usan como fuente de verdad y acortan la entrevista a solo lo ambiguo.
- Si no existe, la entrevista parte de cero.
- Aplica igual para proyectos nuevos y existentes.

---

## Estructura de este repositorio

```
genesis/
├── .claude/
│   ├── agents/              # agentes genéricos de la capa meta
│   │   ├── orchestrator.md
│   │   ├── code-auditor.md
│   │   ├── requirements-interviewer.md
│   │   ├── stack-advisor.md
│   │   └── agent-writer.md
│   └── commands/
│       └── new-project.md   # /new-project
├── core/
│   ├── principles.md        # buenas prácticas universales
│   └── agent-template.md    # plantilla base para agentes especializados
├── intake/
│   └── .gitkeep             # coloca aquí tu .md de requerimientos
└── README.md                # este archivo
```

---

## ¿Y después?

Una vez el proyecto especializado está generado:

1. **Cierra o abandona la sesión actual de `genesis/`**.
2. **Abre una nueva sesión de Claude Code en la carpeta del proyecto generado** (`../<nombre-proyecto>/`).
3. Invoca los comandos de ese proyecto (por ejemplo, su propio ciclo OpenSpec) para empezar a trabajar.

Los agentes especializados ya saben tu stack, tu dominio y tus convenciones. La capa meta no vuelve a entrar en juego salvo que decidas regenerar completamente el equipo de agentes desde cero.
