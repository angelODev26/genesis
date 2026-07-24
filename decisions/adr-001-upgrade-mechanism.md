# ADR-001: Mecanismo futuro de upgrade de agentes (`/upgrade`)

**Estado:** PROPOSED — no implementado; escrito en mármol para discusión y ejecución futura  
**Fecha:** 2026-07-23  
**Contexto:** genesis v1, arquitectura de dos capas, sin mecanismo de evolución post-generación

---

## 1. Problema

genesis es hoy un **scaffold de una sola pasada**: genera agentes especializados y se retira. Esto resuelve el setup inicial, pero deja un agujero estructural a largo plazo.

### 1.1 Obsolescencia por evolución de la plataforma

Claude Code, los modelos subyacentes, y el **formato nativo de subagentes** (`.claude/agents/*.md`) evolucionan constantemente. Ejemplos hipotéticos pero plausibles:

- Claude introduce un nuevo campo de frontmatter obligatorio (ej. `version`, `$schema`, metadata de tool-use avanzado).
- Los alias de modelo nativos cambian o se deprecan.
- Aparece una nueva herramienta nativa que reemplaza un patrón que hoy escribimos manualmente.
- El formato de salida esperado de un agente nativo cambia para soportar nuevas capacidades de rendering.
- Cambios en la CLI de Claude Code sobre cómo se registran comandos o skills.

En cualquiera de estos casos, los proyectos generados por genesis **hoy quedarán con un formato legacy**. No fallarán necesariamente, pero perderán capacidades o requerirán migración manual tediosa por parte del usuario.

### 1.2 ¿Por qué esto no es un “nice to have”?

A diferencia de mejoras subjetivas de agentes (más responsabilidades, mejor naming, refactor de dominio), estos cambios son **impuestos por la plataforma**. Un proyecto no puede decidir “no actualizar” si quiere seguir aprovechando mejoras del ecosistema Claude Code.

Es análogo a que un proyecto Node.js decida no actualizar su `package.json` cuando npm introduce un campo obligatorio: no es una mejora opcional, es un requisito de compatibilidad.

### 1.3 ¿Por qué la capa proyecto no puede resolver esto sola?

Un agente `meta-maintainer` dentro de un proyecto puede auditar sus pares contra una guía de calidad **local**, pero no puede saber que `genesis/core/agent-template.md` cambió el mes pasado. Esa información no existe en el proyecto.

La única fuente de verdad del *formato correcto actual* es `genesis/`.

---

## 2. Diseño propuesto (alto nivel)

**No modifica el flujo actual de `/new-project`.** Es un flujo separado, *opt-in*, invocado explícitamente por el usuario cuando lo desee.

### 2.1 Comando

```
/upgrade <nombre-proyecto>
```

Disponible como comando en `genesis/.claude/commands/upgrade.md` (o directamente invocable desde la capa meta).

### 2.2 Flujo de ejecución

1. **Detección**: El orchestrator verifica que el proyecto exista y que tenga `.claude/agents/` (genesis-origin o no).
2. **Lectura**: Lee todos los agentes `.md` existentes del objetivo.
3. **Comparación**: Los compara contra `core/agent-template.md` y los prompts/estructura de los agentes meta **en su versión actual**.
4. **Reporte**: Genera un diff conceptual con:
   - Cambios estructurales necesarios (ej. “agregar campo `X` en frontmatter”).
   - Cambios de formato (ej. “el formato de salida obligatorio ahora requiere sección `Z`”).
   - Advertencias de deprecación (ej. “alias de modelo `opus-4` ya no existe”).
   - Incompatibilidades detectadas (ej. “este agente usa un campo desconocido”).
5. **Decisión del usuario**: Presenta el reporte y pregunta si aplicar todo, aplicar parcialmente, o descartar.
6. **Aplicación selectiva** (si el usuario acepta):
   - Modifica solo los aspectos estructurales que no rompan la lógica de negocio del agente.
   - **Nunca** toca las responsabilidades específicas de dominio inyectadas durante la generación original.
   - Preserva el `name:` y la `description:` salvo que el template vigente exija un cambio estructural explícito en esos campos.
   - Si el proyecto no es genesis-origin, añade una advertencia previa sobre el riesgo de falsos positivos.
7. **Registro**: Actualiza o crea un archivo de versión del template usado en el proyecto.

### 2.3 Versionado del template

`core/agent-template.md` debe llevar una forma de identificar su versión actual. Opciones a decidir:

| Opción | Pros | Contras |
|--------|------|---------|
| **A. Implícita por fecha de commit** de `agent-template.md` | Cero mantenimiento manual | No es semántica; difícil razonar sobre breaking changes |
| **B. Versionado semántico explícito** (`version: 1.2.0`) en frontmatter o header del template | Claridad absoluta sobre breaking vs. minor changes | Requiere disciplina de mantenimiento cada vez que se edita el template |
| **C. Versionado por hash de contenido** | Automático, preciso | Opaco para humanos |

**Propuesta preliminar:** Opción B (semántico explícito), por ser la única que permite que el upgrade decida automáticamente si una migración es *informativa* o *bloqueante*.

Cada proyecto generado guarda la versión del template en un archivo lightweight, ej. `core/.genesis-template-version`.

### 2.4 Alcance consciente: lo que NO hace

- **No** mejora la lógica de negocio de los agentes (eso sigue siendo trabajo de la capa proyecto).
- **No** cambia las decisiones fundacionales del proyecto (stack, patrones, topología).
- **No** se ejecuta automáticamente ni en segundo plano.
- **No** monitorea los proyectos.
- **No** convierte a genesis en un “orquestador permanente” de los proyectos.

Solo se encarga de la **capa de infraestructura declarativa de los agentes** (formato, campos obligatorios, herramientas nativas nuevas, reglas estructurales).

---

## 3. Temas a abordar antes de implementar

### 3.1 Distinguir “estructura del template” de “contenido inyectado”

El template tiene secciones fijas (frontmatter, reglas de salida, formato obligatorio) y secciones inyectadas (dominio, stack, responsabilidades específicas). El upgrade debe saber cuál es cuál para no borrar la personalización.

**Posibles estrategias:**

- **Marcadores de sección** en el Markdown generado:
  ```markdown
  <!-- genesis:template-section name="tools" -->
  tools:
    - Read
    - Edit
  <!-- /genesis:template-section -->
  ```
- **Modelo de fusión basado en AST/estructura**: parsear frontmatter por un lado y cuerpo por otro, comparando solo las claves estructurales.
- **Agente diferenciador**: un subagente en genesis que reciba [template original + agente actual] y decida qué cambiar.

### 3.2 Backwards compatibility y migraciones acumulativas

Si un proyecto fue generado con genesis v1, y ahora genesis está en v3, ¿`/upgrade` aplica v3 directamente, o v1→v2→v3?

**Propuesta:** `/upgrade` siempre lleva a la última versión, pero si detecta un salto de `major` version, exige confirmación humana paso a paso. Para saltos `minor` o `patch`, puede aplicar directamente con confirmación única.

### 3.3 Proyectos brownfield ajenos (no genesis-origin)

Si el proyecto no fue generado por genesis, `/upgrade` igual puede auditar sus agentes contra `core/agent-template.md` y sugerir alineación. El riesgo de falsos positivos es mayor.

**Propuesta:** `/upgrade` es universal, pero si el proyecto no tiene `core/.genesis-template-version`, añade una advertencia explícita:
> “Este proyecto no fue generado por genesis. Las sugerencias se basan únicamente en nuestro template; verifica que tengan sentido antes de aplicarlas.”

### 3.4 Interacción con OpenRouter y decisiones de proyecto

Si el usuario cambió de opinión sobre OpenRouter desde la generación original, ¿debería `/upgrade` detectar inconsistencias y ofrecer ajustar? Probablemente **no**: el template puede evolucionar, pero la decisión de routing de modelos es del proyecto, no de genesis. Sin embargo, si el template añade un nuevo campo `model:` por defecto, sí debería reflejarse.

### 3.5 Dónde guardar la versión del template en cada proyecto

Opciones:
- `core/.genesis-template-version` (oculto, simple)
- `core/template-version.txt` (visible)
- Frontmatter del README del proyecto (visible pero mezcla concerns)

Ninguna es perfecta. La decisión afecta la legibilidad y la facilidad de recordar que existe un upgrade pendiente.

### 3.6 ¿Es necesario un `meta-maintainer.md` en la capa proyecto?

Un agente *dentro* del proyecto que audite agentes locales contra la guía de calidad del proyecto puede ser complementario: detecta problemas subjetivos (duplicación, descripción poco clara) que `/upgrade` no cubriría (porque no son estructurales). Pero eso es **otra feature**, que puede convivir con `/upgrade` o no.

---

## 4. Relación con la arquitectura de dos capas

Este mecanismo **no rompe el handoff de una sola vía** si se diseña como flujo explícito y separado:

| Handoff normal | Upgrade posterior |
|----------------|-------------------|
| genesis genera → se retira → la capa proyecto es autónoma | El usuario **re-invoca explícitamente** genesis (`/upgrade`) como quien corre `npm update` o `terraform upgrade` |

El proyecto no depende de genesis en su día a día. genesis no “monitorea” ni “controla”. Solo presta un servicio bajo demanda, comparable a un CLI que vuelves a correr cuando la plataforma cambia.

---

## 5. Decisiones pendientes (bloqueantes para la implementación)

1. **¿Versionado semántico explícito para `agent-template.md`, o implícito?**
2. **¿Nombre final del comando?** `/upgrade`, `/sync-agents`, `/update-template`, `/migrate-agents`…
3. **¿Incluimos `meta-maintainer.md` en la generación actual como agente complementario?**
4. **¿Dónde y cómo se guarda la versión del template en cada proyecto?**
5. **¿Se añaden marcadores de sección en los agentes generados ya desde hoy**, para que futuros upgrades sean más fáciles, o se posterga eso hasta que `/upgrade` exista?

---

## 6. Nota sobre el “poderes mentales” de Claude

El ejemplo del usuario de que Claude Code de mañana requiera un archivo `poderesMentales.md` estructurado es humorístico en el detalle, pero **riguroso en la estructura**: la plataforma añadirá capacidades que requerirán cambios en cómo declaramos los agentes.

Tener un mecanismo de upgrade estructural no es paranoia: es **proyección razonable** sobre un ecosistema (Claude Code → Anthropic → LLM tooling) que cambia en ciclos trimestrales. Los proyectos que duren más de 6–12 meses se beneficiarán de no quedar congelados en la versión del template con la que nacieron.

---

## Referencias

- `../core/agent-template.md` — source of truth del formato actual.
- `../orchestrator.md` — donde el flujo de `/upgrade` eventualmente sería orquestado.
- Contexto original: discusión entre usuario y Claude sobre obsolescencia de agentes en proyectos genesis (2026-07-23).
