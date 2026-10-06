# Guía de Migración a v2 — `agentic-ecosystem`

> **Destinatarios**: Repositorios satélite (spokes) como `KmSafe`, `kilomenos-backend`, `kilomenos-web`, o proyectos que utilizaban la v1 de `android-agentic-ecosystem`.

---

## 1. Resumen de Cambios Principales en v2

La versión 2.0.0 de `agentic-ecosystem` resuelve los problemas de token bloat, contexto cruzado y degradación de caché identificados en la v1:

1. **Arquitectura Monorepo `core/` + `packs/`**:
   - `core/`: Schemas universales Draft-07, contratos unificados, ciclo de vida OpenSpec, Atlassian Bridge, y enrutamiento FinOps.
   - `packs/{android, backend, web}`: Skills, roles (`packs/<pack>/roles/*.md`), plantillas y ejemplos canónicos aislados estrictamente por plataforma.
2. **Eliminación de Polución Cruzada**:
   - Al instalar un pack (ej. `android`), **solo** se copian los skills y templates de esa plataforma. Ya no se instalan skills de Backend (Supabase) o Web en proyectos Android ni viceversa.
3. **Instrucciones Lean e Índice Compacto**:
   - `AGENTS.md` reducido a un índice de despacho de ~860 palabras (~1.6k tokens).
   - Los roles específicos residen en `packs/<pack>/roles/` y se inyectan únicamente cuando el rol participa en la fase correspondiente.
4. **Aislamiento de Etapas (Stage Isolation)**:
   - Se introduce `get_stage_context_manifest` y `generate_subagent_dispatch_prompt` en `workflow.py`. Cada rol (PO, Arquitecto, Dev, QA) opera en una sesión o subagente aislado con whitelist estricta de archivos y skills.
   - Directiva de salida zero-chatter: ruta del artefacto + resumen $\le 200$ tokens.
5. **Model Routing & FinOps**:
   - Matriz `core/models.yaml` con tarifas por millón de tokens, 4 tiers (`frontier_reasoning`, `frontier_coding`, `mid_reasoning`, `lightweight_flash`) y modelos recomendados.
   - Telemetría en todos los handoffs (`telemetry`: model, input_tokens, output_tokens, cached_tokens, duration_seconds, estimated_cost_usd).
6. **Mecanismo de Lock `.agentic.lock`**:
   - El spoke ahora registra la versión instalada del core y del pack, permitiendo verificar la sincronización de manera determinista.

---

## 2. Procedimiento de Migración Paso a Paso

### Paso 1: Levantar el Freeze de Propagación
En el hub `agentic-ecosystem`, la versión v2 ha sido estabilizada y el archivo `PROPAGATION_FREEZE.md` se ha retirado en la release oficial.

### Paso 2: Instalación del Pack Específico en el Spoke
Ejecutar el script de despliegue desde la raíz de `agentic-ecosystem` apuntando al repositorio destino con la opción `--pack`:

#### Para proyectos Android (`KmSafe`, `kilomenos` Android):
```bash
python scripts/install_to_project.py --target ../KmSafe --pack android --mode both --update-agents
```

#### Para proyectos Backend (`kilomenos-backend`):
```bash
python scripts/install_to_project.py --target ../kilomenos-backend --pack backend --mode both --update-agents
```

#### Para proyectos Web (`kilomenos-web`):
```bash
python scripts/install_to_project.py --target ../kilomenos-web --pack web --mode both --update-agents
```

> **Nota**: El flag `--profile <nombre>` sigue estando soportado como alias de `--pack` por compatibilidad retrospectiva.

---

## 3. Verificación Post-Migración en el Spoke

Una vez ejecutado el instalador en el repositorio spoke:

1. **Verificar el archivo `.agentic.lock`**:
   Comprobar que en la raíz del proyecto existe el archivo `.agentic.lock` con formato:
   ```json
   {
     "core_version": "2.0.0",
     "pack": "android",
     "pack_version": "2.0.0",
     "installed_at": "...",
     "mode": "both"
   }
   ```

2. **Verificar Aislamiento de Skills**:
   Inspeccionar `.gemini/antigravity/skills/` (o `.agents/skills/`).
   - Para Android: deben existir únicamente los skills de Android y Core (sin `supabase-db-triage`, `web-lighthouse-seo`, etc.).
   - La huella de tokens de contexto se reduce en más del 50%.

3. **Verificar Schemas y Contratos**:
   Los esquemas en `schemas/` en el spoke ahora soportan el bloque opcional `telemetry` y validan bajo Draft-07.

4. **Ejecutar Flujo Piloto**:
   ```bash
   python scripts/workflow.py manifest <TICKET-ID> --stage po --prompt
   ```
   Comprobar que el prompt de despacho emite las restricciones de contexto aisladas y el enrutamiento de modelo sugerido.

---

## 4. Resolución de Dudas y Compatibilidad Retrospectiva

- **¿Qué pasa con los handoffs existentes?**
  El bloque `telemetry` en los schemas es opcional. Todos los handoffs generados previamente en v1 siguen siendo 100% compatibles y válidos.
- **¿Qué pasa con los living specs en `openspec/specs/`?**
  La estructura de especificaciones vivas en OpenSpec se preserva íntegramente. No requiere ninguna migración manual de contenido.
