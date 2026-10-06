# ROADMAP v2 — agentic-ecosystem

> Documento de continuidad. Cualquier agente o sesión que retome la v2 debe leer **este archivo primero** y después `docs/v2/INFORME-CONTEXTO-FINOPS.md` (que contiene la evidencia y el análisis).

## Estado
| Campo | Valor |
|---|---|
| Rama | `main` / `v2` (v2.0.0 liberada) |
| Propagación a spokes | **DESCONGELADA** (`PROPAGATION_FREEZE.md` retirado, v2.0.0 activa) |
| Nombre nuevo | `agentic-ecosystem` (antes `android-agentic-ecosystem`) |
| Fase actual | F6 (Completada) |

## Principios rectores (no negociables)
1. **Aislamiento por etapa**: PO, Arquitecto, Dev y QA trabajan cada uno en una sesión o subagente propio. La única entrada es el handoff JSON más los artefactos que referencia; no se hereda historial.
2. **Un modelo por sesión**: no cambiar de modelo a mitad de una sesión (rompe la caché). Prefijo estable al inicio y lo variable al final.
3. **Instrucciones mínimas**: solo lineamientos propios del proyecto + few-shot. Nada de pedagogía genérica; lo que valida un gate no se repite en prosa.
4. **Núcleo único y packs instalables**: schemas y contratos existen una sola vez.

## Fases
| Fase | Objetivo | Entregables | Criterio de salida | Estado |
|---|---|---|---|---|
| **F0** Gobierno y renombrado | Aislar la v2 y quitar "android" del nombre | Rama `v2`, freeze, renombrado de referencias internas, carpeta local y repo GitHub renombrados | Tests verdes; carpeta y remote con el nombre nuevo | ✅ Completada |
| **F1** Higiene | Quitar ruido del workspace | `.agents/`, `walkthrough/` y tests de estrés fuera de la ruta de exploración; deduplicar `ORIGINAL_REQUEST.md`; separar README humano de instrucciones del agente | Huella de archivos explorables reducida ≥50 % | ✅ Completada |
| **F2** Núcleo + packs | Reestructurar a `core/` + `packs/{android,backend,web}` | Movimiento de archivos, `install_to_project.py --pack`, `schema_version`, `requires_core`, `.agentic.lock` | Instalar el pack android no copia nada de backend/web | ✅ Completada |
| **F3** Adelgazar instrucciones (P3) | Índice `AGENTS.md` ≤3k tokens | `core/AGENTS.md` (índice), `packs/*/roles/*.md`, `packs/*/examples/` (few-shot reales), skills recortados | Prefijo por etapa ≤4k tokens (auditado) | ✅ Completada |
| **F4** Aislamiento de etapas (P1) | Una sesión o subagente por rol | `context_manifest` por etapa en `workflow.py`; subagentes que devuelven ruta + resumen de ≤200 tokens; workers de triage | Contexto en QA ≤30k tokens en un feature piloto | ✅ Completada |
| **F5** Modelos y FinOps (P2 + P5) | Routing de modelos y telemetría | `models.yaml`; campo `telemetry` en los handoffs; presupuesto por etapa en CI | Comparativa antes/después en 2–3 features | ✅ Completada |
| **F6** Release v2 | Merge y propagación controlada | Merge `v2 → main`, borrar `PROPAGATION_FREEZE.md`, guía de migración para spokes, tag `v2.0.0` | Spoke piloto migrado sin incidencias | ✅ Completada |

## Pendientes F0
- [x] Rama `v2`
- [x] `PROPAGATION_FREEZE.md` + guard en `install_to_project.py`
- [x] Reemplazo de referencias `android-agentic-ecosystem` → `agentic-ecosystem` (excluye `.agents/`, que es histórico)
- [x] Informe copiado a `docs/v2/`
- [x] Renombrar el repo en GitHub y actualizar `origin` → `https://github.com/joshluq/agentic-ecosystem.git`
- [x] Renombrar la carpeta local `android_agentic_ecosystem` → `agentic_ecosystem`
- [x] Tests verdes tras el renombrado (`python -m unittest discover -s tests`: 47 OK, 2026-10-05)
- [x] Workflow de CI ya genérico (`Agentic Ecosystem Verification`)
- [x] Textos "Android" en títulos genéricos: encabezado e intro de `AGENTS.md`, tagline de `README.md` neutralizados (2026-10-05)

## Entregables F2
- [x] Directorio `core/` con `manifest.json` (`schema_version: 2.0.0`), schemas, templates y contracts universales.
- [x] Migración de `profiles/` a `packs/{android, backend, web}` con sus respectivos `pack.json` y `requires_core: ">=2.0.0"`.
- [x] Soporte `--pack` en `install_to_project.py` (manteniendo retrocompatibilidad `--profile`), aislamiento estricto de skills por pack y generación de `.agentic.lock`.
- [x] Actualización de linters y auditores (`audit_context_budget.py`, `lint_platform_leakage.py`, `audit_context_pruning.py`, `test_scripts.py`, `test_contracts.py`) para reconocer la arquitectura `core/` + `packs/`.

## Entregables F3
- [x] `AGENTS.md` raíz y `core/AGENTS.md` reducidos a un índice lean de ~860 palabras (~1.6k tokens, muy por debajo de la meta de 3k).
- [x] Roles específicos extraídos modularmente a `packs/<pack>/roles/*.md`.
- [x] Ejemplos few-shot canónicos creados en `packs/android/examples/`.
- [x] Skill con sobrepeso (`android-staff-engineer-compose`) adelgazado a ~400 palabras (< 1200 palabras límite).
- [x] Auditoría de presupuesto de contexto en verde/tolerancia sin fallos.

## Entregables F4
- [x] Mecanismo de manifiesto de contexto por etapa implementado en `scripts/workflow.py`: `get_stage_context_manifest` (roles PO, Architect, Dev, QA).
- [x] Generador de prompt de subagente zero-chatter: `generate_subagent_dispatch_prompt` que limita la respuesta a la ruta del artefacto y un resumen de $\le 200$ tokens.
- [x] Subcomando CLI `python scripts/workflow.py manifest <CHANGE_ID> --stage <po|architect|dev|qa> [--prompt]` para orquestadores y agentes.
- [x] Suite de tests unitarios actualizada en `tests/test_scripts.py` verificando el manifiesto y prompt de subagente.

## Entregables F5
- [x] Matriz de modelos y presupuestos FinOps definida en `core/models.yaml` (pricing por millón, tiers `frontier_reasoning`, `frontier_coding`, `mid_reasoning`, `lightweight_flash`, modelos preferidos y esfuerzo de razonamiento por rol).
- [x] Objeto opcional `telemetry` integrado y validado en schemas Draft-07 universales (`po_to_architect_handoff`, `architect_to_dev_handoff`, `dev_to_qa_handoff`, `qa_verdict_handoff`).
- [x] Métodos de cálculo de costes y enrutamiento en `scripts/workflow.py`: `load_models_config`, `get_model_routing_for_stage`, `calculate_finops_cost`, `build_default_telemetry`, y enriquecimiento del prompt de despacho de subagente.
- [x] Cobertura de tests unitarios para routing y FinOps en `tests/test_scripts.py` (`test_model_routing_and_finops`).
- [x] Suite completa de pruebas (50/50) y verificación integral (`verify_ecosystem.py`) en verde al 100%.

## Entregables F6
- [x] Guía exhaustiva de migración para repositorios satélite (spokes) creada en `docs/v2/MIGRATION_GUIDE.md`.
- [x] Archivo `PROPAGATION_FREEZE.md` eliminado y guard de propagación levantado.
- [x] Instalación piloto con packs validada en directorios aislados sin errores y con generación exitosa de `.agentic.lock`.
- [x] Versión final v2.0.0 lista para merge a `main`.


## Registro de decisiones
| Fecha | Decisión | Referencia |
|---|---|---|
| 2026-10-05 | Adoptar los principios 1–3 (contexto aislado, un modelo por sesión, prompts mínimos) | Informe §1–3 |
| 2026-10-05 | Monorepo con núcleo y packs (opción C); no dividir en tres repos | Informe §6 |
| 2026-10-05 | Nombre `agentic-ecosystem`; congelar la propagación hasta F6 | Informe §7 |
