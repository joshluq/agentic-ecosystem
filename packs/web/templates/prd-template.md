# Product Requirements Document (PRD)

**Feature Identifier**: `PRD-[ID]`  
**Feature Title**: [Feature / Portal Name]  
**Target Platform**: Web (Astro SSG / Tailwind)  
**Creation Date**: [YYYY-MM-DD]  
**Status**: DRAFT | IN_REVIEW | APPROVED  

---

## 1. Problem Statement & User Value
- **Problem**: [Clear description of user friction, legal compliance requirement, or content gap]
- **Target Audience**: [Public Users, Premium Subscribers, Regulators, Auditors]
- **Value Hypothesis**: [Expected outcome: e.g. compliance with Play Store deletion policy, < 1.0s page load]

## 2. User Stories
- **US-01**: As a [visitor], I want to [view privacy policy], so that [I understand how my data is stored].
- **US-02**: As an [app user], I want to [request account deletion], so that [my data is expunged per GDPR].

## 3. Acceptance Criteria (Given / When / Then)
- **AC-01**: [Criteria Title]
  - **Given** [a visitor navigating to the portal URL]
  - **When** [the page loads]
  - **Then** [the complete text renders with semantic typography and zero layout shift]

### 3.1 Reglas de Negocio con Consecuencia Explícita si Fallan (BR-xx)
Toda regla de negocio web debe definir inequívocamente su condición de activación y la consecuencia observable en caso de incumplimiento:

| ID Regla | Enunciado de Regla | Condición de Fallo / Violación | Consecuencia en Sistema / Feedback Visual / HTTP |
|---|---|---|---|
| **BR-01** | [Regla de contenido o formulario] | [Fallo de validación o campo mandatorio ausente] | [Mensaje de error accesible, foco en campo erróneo] |
| **BR-02** | [Regla de enlace / redirección] | [Recurso inexistente o ruta rota] | [Página 404 estática optimizada con retorno a Home] |

## 4. Non-Functional Requirements (Web Standards)
- **Lighthouse Performance Targets**:
  - Performance: >= 95
  - Accessibility: 100 (WCAG 2.1 AA)
  - Best Practices: 100
  - SEO: 100
- **Responsive Viewport Support**: 320px (mobile) to 2560px (ultra-wide desktop).
- **Zero Client-Side JS Bloat**: Pure static HTML output for informational and legal content.
- **GDPR & Store Compliance**: Clear account deletion instructions and request submission form.

## 5. Dudas Abiertas Bloqueantes (HITL Halt Gate)
> [!IMPORTANT]
> **GATE BLOQUEANTE**: Si existen dudas de producto, legales, de negocio o dependencias técnicas no resueltas en esta tabla, **QUEDA ESTRICTAMENTE PROHIBIDO AVANZAR A DISEÑO TÉCNICO O ESCRITURA DE CÓDIGO**. El Product Owner y los Stakeholders deben resolverlas antes de desbloquear la fase de Arquitectura e Implementación.

| ID Duda | Pregunta / Ambigüedad Detectada | Impacto si no se resuelve | Propietario / Stakeholder | Estado (BLOQUEANTE / RESUELTA) | Decisión Final Acordada |
|---|---|---|---|---|---|
| D-01 | [Ej: ¿Texto legal exacto aprobado por compliance?] | Crítico: riesgo regulatorio | Legal / Product Owner | RESUELTA | [Aprobado texto v1.2] |

## 6. Out of Scope
- [Explicit list of capabilities, platforms, or variations deliberately excluded from this release]
