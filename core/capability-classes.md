# Clases de capacidades — qué herramienta usa cada una

`agent-writer` consulta este archivo antes de materializar cualquier capacidad pedida en la entrevista. La regla: **la forma de la herramienta se decide por la naturaleza del trabajo, no por costumbre**. Un equipo de solo subagentes es síntoma de no haberse hecho esta pregunta.

## La tabla de decisión

| Si la capacidad es... | Materializa como... | Por qué |
|---|---|---|
| Trabajo con **juicio y criterio** sobre código o dominio, delegable en segundo plano | **Subagente** (`.claude/agents/` / `.opencode/agents/`) | El LLM decide bien cuando el contexto es delimitado y las instrucciones son especializadas |
| Un **punto de entrada explícito** del usuario que dispara un flujo o invoca a un agente | **Comando** (`.claude/commands/` / `.opencode/commands/`) | El usuario quiere controlar *cuándo* pasa; el comando es el gatillo, el agente es el cerebro |
| **Conocimiento procedural compartido** que solo se necesita a veces (workflow de OpenSpec, convenciones de API, cómo se hace un release) | **Skill** (`.claude/skills/` / `.opencode/skills/`) | Carga progresiva: no infla todos los prompts; existe una sola fuente del procedimiento |
| **Chequeo o repetición determinística** sin juicio (tests, formato, lint, validar migraciones, comparar frontmatters) | **Script o hook**, nunca un subagente | El LLM es caro e inconsistente para esto; un script es exacto y gratis |

## Señales de clasificación errónea

- Un subagente cuyo trabajo cabe en un script → estás pagando tokens por determinismo gratuito.
- Un procedimiento copiado en el prompt de tres agentes → debería ser una skill.
- Una capacidad que el usuario "olvida invocar" → probablemente necesita comando (gatillo visible) o hook (gatillo automático), no mejor descripción.

## Capacidad de calidad/review: presencia por defecto

Todo proyecto generado incluye, salvo que la entrevista lo haya descartado explícitamente:

1. **Un subagente de calidad/review** (solo lectura de código, sin implementación), y
2. **El comando `/review`** que lo dispara con protocolo fijo: archivos tocados en la tarea + principios aplicables (`core/principles.md` + convenciones del proyecto) + formato de reporte.

La razón: un revisor que depende de que el humano recuerde llamarlo tiende a no llamarse nunca. El comando convierte el buen hábito en ruta visible.

## Regla de simetría multiplataforma

La decisión es **semántica** ("este proyecto tiene comando de review"); la **expresión es por plataforma** (comando en sintaxis Claude Code y/o OpenCode según aplique). Nunca mezcles sintaxis entre variantes — misma regla dura que con los agentes.
