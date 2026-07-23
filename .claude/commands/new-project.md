# new-project

Dispara el flujo completo de creación o adaptación de un proyecto por parte de la capa meta.

## Uso

```
/new-project <nombre-del-proyecto>
```

## Comportamiento

Este comando invoca al agente `orchestrator` de la capa meta con los siguientes parámetros implícitos:

- **Nombre del proyecto**: el argumento `<nombre-del-proyecto>` proporcionado por el usuario.
- **Contexto disponible**: `genesis/intake/` se revisa automáticamente antes de la entrevista si contiene archivos.

## Pasos que ejecuta el orchestrator

1. Detecta si el flujo es **nuevo** (greenfield) o **existente** (brownfield) preguntando al usuario si no es evidente por el contexto.
2. Si es brownfield: invoca a `code-auditor` para analizar el proyecto existente.
3. Invoca a `requirements-interviewer` para cubrir lo que falta (lee `intake/` si existe).
4. Invoca a `stack-advisor` para proponer stack/patrones con trade-offs.
5. Invoca a `agent-writer` para generar los agentes especializados y terminar el setup.
6. El orchestrator termina su trabajo y notifica al usuario que debe abrir una nueva sesión en la carpeta del proyecto generado.

## Notas importantes

- Este comando **no** desarrolla código de negocio del proyecto.
- Este comando **no** ejecuta el ciclo OpenSpec de desarrollo — ese vive únicamente dentro de la capa proyecto.
- Si el proyecto ya existe como carpeta hermana (o el usuario indica que es brownfield), el flujo adapta y enriquece el proyecto en lugar de crearlo desde cero.
