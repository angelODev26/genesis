---
description: Verificación determinística (solo lectura) de un proyecto generado por genesis. Uso: /verify <ruta-del-proyecto>
---

Evento: `/verify`
Ruta del proyecto a verificar: $ARGUMENTS

Ejecuta la verificación determinística del proyecto indicado:

1. Desde la raíz de `genesis/`, corre `python3 tools/verify-project.py $ARGUMENTS` (la ruta suele ser relativa como `../nombre-proyecto`).
2. Si el código de salida es **0**, informa al usuario que el proyecto pasa la verificación y muestra las advertencias si las hubiera.
3. Si el código de salida es **1**, presenta cada error agrupado (frontmatter, mezcla de campos entre plataformas, simetría, unicidad) y propón la corrección concreta de cada uno. **No edites el proyecto** sin confirmación explícita del usuario.

Este comando nunca modifica archivos: es solo lectura.
