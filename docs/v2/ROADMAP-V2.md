# ROADMAP v2 — agentic-ecosystem

> Documento de continuidad. Cualquier agente o sesión que retome la v2 debe leer **este archivo primero** y después `docs/v2/INFORME-CONTEXTO-FINOPS.md` (que contiene la evidencia y el análisis).

## Estado
| Campo | Valor |
|---|---|
| Rama | `v2` (base: `main` @ 2026-10-05) |
| Propagación a spokes | **CONGELADA** (`PROPAGATION_FREEZE.md`) |
| Nombre nuevo | `agentic-ecosystem` (antes `android-agentic-ecosystem`) |
| Fase actual | F1 |

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
| **F2** Núcleo + packs | Reestructurar a `core/` + `packs/{android,backend,web}` | Movimiento de archivos, `install_to_project.py --pack`, `schema_version`, `requires_core`, `.agentic.lock` | Instalar el pack android no copia nada de backend/web | 🟡 Siguiente |
| **F3** Adelgazar instrucciones (P3) | Índice `AGENTS.md` ≤3k tokens | `core/AGENTS.md` (índice), `packs/*/roles/*.md`, `packs/*/examples/` (few-shot reales), skills recortados | Prefijo por etapa ≤4k tokens (auditado) | ⬜ |
| **F4** Aislamiento de etapas (P1) | Una sesión o subagente por rol | `context_manifest` por etapa en `workflow.py`; subagentes que devuelven ruta + resumen de ≤200 tokens; workers de triage | Contexto en QA ≤30k tokens en un feature piloto | ⬜ |
| **F5** Modelos y FinOps (P2 + P5) | Routing de modelos y telemetría | `models.yaml`; campo `telemetry` en los handoffs; presupuesto por etapa en CI | Comparativa antes/después en 2–3 features | ⬜ |
| **F6** Release v2 | Merge y propagación controlada | Merge `v2 → main`, borrar `PROPAGATION_FREEZE.md`, guía de migración para spokes, tag `v2.0.0` | Spoke piloto migrado sin incidencias | ⬜ |

## Pendientes F0
- [x] Rama `v2`
- [x] `PROPAGATION_FREEZE.md` + guard en `install_to_project.py`
- [x] Reemplazo de referencias `android-agentic-ecosystem` → `agentic-ecosystem` (excluye `.agents/`, que es histórico)
- [x] Informe copiado a `docs/v2/`
- [x] Renombrar el repo en GitHub y actualizar `origin` → `https://github.com/joshluq/agentic-ecosystem.git`
- [x] Renombrar la carpeta local `android_agentic_ecosystem` → `agentic_ecosystem`
- [x] Tests verdes tras el renombrado (`python -m unittest discover -s tests`: 47 OK, 2026-10-05)
- [x] Workflow de CI ya genérico (`Agentic Ecosystem Verification`)
- [ ] Textos "Android" en títulos genéricos: encabezado e intro de `AGENTS.md`, tagline de `README.md` (se resuelve en F2/F3)

## Registro de decisiones
| Fecha | Decisión | Referencia |
|---|---|---|
| 2026-10-05 | Adoptar los principios 1–3 (contexto aislado, un modelo por sesión, prompts mínimos) | Informe §1–3 |
| 2026-10-05 | Monorepo con núcleo y packs (opción C); no dividir en tres repos | Informe §6 |
| 2026-10-05 | Nombre `agentic-ecosystem`; congelar la propagación hasta F6 | Informe §7 |
