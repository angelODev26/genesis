# Playbooks de entrevista — áreas de decisión por capa

Este archivo es el checklist de cobertura del `requirements-interviewer`. Para cada capa de stack que tenga el proyecto, estas son las áreas de decisión que **no pueden quedar implícitas**: cada una debe terminar la entrevista en uno de estos estados:

- **resuelta** (intake, auditor o respuesta del usuario ya la cubrieron)
- **preguntada y respondida** en esta entrevista
- **diferida consciente** (se decidió explícitamente posponerla — se registra como tal, nunca queda en blanco)

No hay que especificar el sistema al 100%: el objetivo es que ninguna área crítica para la composición del equipo de agentes quede "olvidadas en silencio". Las respuestas de una línea bastan.

---

## Frontend

| Área | Por qué importa para los agentes | Ejemplos de respuesta buena |
|---|---|---|
| **Estrategia de renderizado** | Define la familia de framework y toolchain (SPA pura vs SSR cambian todo) | "SPA con Vite" / "SSR con Next 15" |
| **Manejo de estado** | Determina si hace falta un agente especializado en estado o alcanza con patrón en el agente de features | "Zustand para estado global; el resto local por componente" |
| **Data fetching y caché** | Es el contrato vivo con el backend: debe haber un criterio único para no tener 5 patrones de fetch | "TanStack Query con cliente generado desde OpenAPI" |
| **Contrato con el backend** | Si hay API existente (Swagger/OpenAPI), los agentes front deben conocerla y no reinventarla | "El backend expone OpenAPI en /v3/api-docs; auth por JWT Bearer" |
| **Estilos** | El agente de UI necesita UN sistema de estilos; mezclar sistemas genera deuda el día 1 | "Tailwind 4 + tokens propios; nada de CSS-in-JS" |
| **Testing** | Decide si entra un agente de calidad/testing o queda dentro de cada agente de feature | "Vitest para unit/component, Playwright para E2E en flujos críticos" |
| **i18n / accesibilidad** | Si aplica y se omite, se convierte en refactor caro a mitad de proyecto | "Solo español MVP" / "WCAG AA obligatorio" |
| **Build y despliegue** | El agente de toolchains/CI debe saber a dónde va el bundle | "Docker multi-stage + Nginx" |

## Backend

| Área | Por qué importa | Ejemplos |
|---|---|---|
| **Framework base y versión** | Determina el conocimiento que cada agente necesita y el formato de sus ejemplos | "Spring Boot 3.x + Java 21" |
| **Persistencia** | ORM, migraciones, y motor DB son decisiones que ningún agente debe decidir a medias | "PostgreSQL 16 + Flyway + Spring Data JPA" |
| **Estructura de módulos** | Define las fronteras de responsabilidad entre agentes de dominio | "Monolito modular, un paquete por dominio" |
| **AuthN / AuthZ** | Afecta a casi todos los endpoints y hay que nombrar un dueño claro | "Spring Security + JWT; permisos por rol EMPLOYEE/ATHLETE" |
| **Testing y cobertura** | Igual que en front: ¿quién vigila la calidad y con qué barra? | "JUnit 5 + Testcontainers; cobertura mínima 70% en dominio" |
| **Observabilidad** | Errores, logs estructurados, métricas — si no se decide, cada agente improvisa | "Logs JSON con correlation-id" |
| **Empaquetado y despliegue** | Docker vs JVM jar cambia el agente de infra | "Docker Compose local; imagen para prod" |

## Móvil

| Área | Por qué importa | Ejemplos |
|---|---|---|
| **Nativo vs cross-platform** | Cambia completamente el equipo y las herramientas | "React Native + Expo" / "Kotlin nativo" |
| **Offline y sincronización** | Es la decisión más cara de revertir tarde | "Offline-first con cola local" |
| **Navegación** | Define el esqueleto de la app | "Expo Router con tabs" |
| **Manejo de estado / fetching** | Mismas razones que en frontend | "Zustand + TanStack Query" |
| **Distribución** | Play Store / App Store / interno — afecta los agentes de CI | "Internal testing en Play Console" |

## Fullstack

No hay áreas distintas: aplica **ambas** playbooks (frontend + backend) y añade una pregunta de cierre: "¿cómo se versiona el contrato entre ambas capas?" (OpenAPI, GraphQL schema, tRPC…).
