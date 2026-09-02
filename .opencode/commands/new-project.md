---
description: Arranca el flujo completo de creación o adaptación de un proyecto por parte de la capa meta genesis
agent: orchestrator
subtask: true
---

Evento: `/new-project`
Nombre del proyecto indicado por el usuario: $ARGUMENTS

Ejecuta tu flujo completo de orquestación de la capa meta:

1. Detecta el caso (greenfield, brownfield externo o brownfield interno / ampliación de capa).
2. Si es brownfield, invoca a `code-auditor`.
3. Invoca a `requirements-interviewer` (lee `intake/` si existe; esa carpeta es solo lectura).
4. Invoca a `stack-advisor` para stack/patrones con trade-offs.
5. Invoca a `agent-writer` para generar los agentes especializados según la plataforma elegida.
6. Termina notificando al usuario que abra una nueva sesión en la carpeta del proyecto (si la plataforma es OpenCode, indicarle que reinicie su sesión de opencode para cargar los agentes).

No desarrolles código de negocio. No ejecutes el ciclo OpenSpec de desarrollo — ese vive en la capa proyecto.
