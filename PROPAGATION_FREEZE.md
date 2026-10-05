# PROPAGATION FREEZE — v2 en curso

- Desde: 2026-10-05 · Rama: `v2`
- No propagar cambios a proyectos satélite (spokes) hasta cerrar la v2.
- `scripts/install_to_project.py` aborta (exit 2) mientras exista este archivo.
- `validate_spokes_sync.py`: el drift con los spokes es **esperado** durante la v2; ignorarlo.
- Levantar el freeze: borrar este archivo en el merge final `v2 → main` (ver `docs/v2/ROADMAP-V2.md`, fase F6).
