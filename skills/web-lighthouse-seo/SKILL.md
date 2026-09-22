---
name: web-lighthouse-seo
description: Optimizes static web portals for 100/100 Google Lighthouse scores (Performance, Accessibility, Best Practices, SEO), WCAG AA compliance, and guides migration from raw HTML/CSS to Astro + Tailwind.
---

# Web Performance, SEO & Astro Modernization

Skill focused on **high-performance static web pages** (Landing & Legal portals), zero-bloat CSS, accessibility compliance, and progressive migration to modern SSG frameworks (**Astro**).

---

## 1. Core Web Vitals Targets

- **Performance**: Score $\ge 98/100$
  - Largest Contentful Paint (LCP) $\le 1.2s$
  - First Input Delay (FID) / INP $\le 100ms$
  - Cumulative Layout Shift (CLS) $\le 0.05$
- **Accessibility**: Score $100/100$ (WCAG 2.1 AA)
  - Color contrast ratio $\ge 4.5:1$ for normal text, $\ge 3:1$ for large text.
  - Proper heading hierarchy (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`).
  - All interactive elements have descriptive focus states and labels.
- **Best Practices & SEO**: Score $100/100$
  - Proper canonical URLs, OpenGraph/Twitter card tags.
  - Semantic HTML tags (`<main>`, `<header>`, `<nav>`, `<article>`, `<footer>`).

---

## 2. Astro Modernization Blueprint

When migrating from raw HTML/CSS to Astro for an ultra-fast, professional legal & marketing site:

### 2.1 Why Astro for KiloMenos Web?
- **Zero JavaScript Runtime**: Generates 100% static HTML by default.
- **Markdown / MDX Support**: Write terms, privacy policies, and changelogs in Markdown files (`src/content/legal/terminos.md`).
- **Tailwind CSS Integration**: Scoped, consistent design tokens matching Android CanvasKit color palettes.

### 2.2 Project Structure
```text
kilomenos-web/
├── astro.config.mjs
├── package.json
├── tailwind.config.cjs
└── src/
    ├── layouts/
    │   └── LegalLayout.astro
    ├── components/
    │   ├── Header.astro
    │   └── Footer.astro
    ├── content/
    │   └── legal/
    │       ├── terminos-y-condiciones.md
    │       └── politica-de-privacidad.md
    └── pages/
        ├── index.astro
        ├── legal/
        │   └── [...slug].astro
        └── eliminar-cuenta.astro
```
