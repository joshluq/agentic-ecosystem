---
name: android-staff-engineer-compose
description: Architects, reviews, and implements production-grade Jetpack Compose UI following Staff Android Engineer standards and KiloMenos guidelines in AGENTS.md. Enforces MVI, CanvasKit tokens, 4-Layer UI, Navigation 3 scoping, and recomposition optimization.
---
# Android Staff Engineer - Jetpack Compose & Clean Architecture

Staff-level standards for **Jetpack Compose** aligned with **KiloMenos (KmSafe) Architecture (`AGENTS.md`)**.

---

## 1. Architectural Pillars

- **The "Being" (Domain Models & UI State)**: Pure data structures with immutable domain rules. MVI UI states are strictly `@Immutable` snapshots.
- **The "Doing" (UseCases & ViewModels)**: Presentation logic mediated via UseCases (`UseCase First`). ViewModels never contain arithmetic formulas or business aggregations.
- **Module Boundaries**: Feature modules (`:feature:*`) depend only on `:core:domain`, `:core:ui` (CanvasKit), and `:core:navigation`. Never inject repositories into ViewModels.

---

## 2. Compose Presentation Architecture (Coordinator / Route Pattern)

Every screen decouples navigation coordination from stateless UI:
- **`FeatureRoute.kt` (Coordinator)**: Resolves scoped ViewModel with `hiltViewModel(key = ...)`, collects state via `collectAsStateWithLifecycle()`, observes effects via `LaunchedEffect(Unit)`, and delegates lambdas down.
- **`FeatureScreen.kt` (Pure UI)**: Stateless composable accepting state and intent lambdas. Zero ViewModel references, contains `@Preview` fixtures, and enforces >= 48dp touch targets and `contentDescription`.
- **MVI Contracts (`ScreenViewModel<State, Event, Effect>`)**:
  ```kotlin
  @Immutable data class FeatureState(...) : UiState
  sealed interface FeatureEvent : UiEvent
  sealed interface FeatureEffect : UiEffect
  ```

---

## 3. The 4-Layer Visual Architecture

1. **Layer 1: The Pulse (Glanceable Metric, < 2s)**: High-contrast KPI using `CanvasKitTheme.typography.headingLarge` and status colors (Safe/Risk/Excess).
2. **Layer 2: Contextual Decision Radar**: Horizontal actionable cards with delta badges (e.g. allowance remaining).
3. **Layer 3: Zero-Friction Action (< 5s)**: 1-Tap preset chips (`[30 €]`, `[Full Tank]`), odometer auto-fill.
4. **Layer 4: Intelligent Diagnostic Feed**: Operational clusters (trips, refueling cycles) instead of raw table dumps.

---

## 4. Navigation 3 & ViewModelStore Scoping

Enforce deterministic ViewModel lifecycle scoping under Navigation 3:
1. **Parametrized Entities**: Provide entity key: `hiltViewModel(key = "record_$recordId")`.
2. **Ephemeral Wizards / Paywalls**: Provide random session key: `val sessionId = rememberSaveable { UUID.randomUUID().toString() }; hiltViewModel(key = sessionId)`.
3. **Session Purge**: On sign-out/account deletion, clear `viewModelStoreOwner?.viewModelStore?.clear()`.
4. **Navigation Triad**: Atomically update `Destination.kt` (`:core:navigation`), `[Feature]Route.kt`, and `AppNavigation.kt` (`:app`).

---

## 5. Design System & Recomposition Optimization

- **CanvasKit Tokens**: Exclusively use `CanvasKitTheme.typography.*`, `CanvasKitTheme.spacing.*`, and `CanvasKitTheme.colors.*`. Zero raw hex colors or arbitrary dp.
- **Stability & Immutability**: Use `@Immutable` data classes and persistent collections (`ImmutableList`).
- **Deferred State Reads**: Defer high-frequency updates using lambda modifiers (`Modifier.offset { ... }`).
- **Stable Keys**: Always key `LazyColumn` / `LazyRow` items (`key = { it.id }`).
- **Verification Gate**: Must assemble cleanly via `./gradlew :app:assembleDevDebug`.

