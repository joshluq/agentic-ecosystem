# Component Specification (COMP-SPEC)

**Spec Identifier**: `COMP-SPEC-[ID]`  
**Component Name**: `[ComponentName]`  
**Target Route / File**: `src/pages/[route].astro` or `src/components/[Component].astro`  

---

## 1. Component Hierarchy & Semantics
- **Semantic Structure**: `<main>`, `<article>`, `<section>`, `<header>`, `<footer>`.
- **Heading Outline**: Strict `h1` -> `h2` -> `h3` hierarchy without skipping levels.

## 2. Props & Data Contract
```typescript
export interface Props {
  title: string;
  effectiveDate?: string;
  sections: Array<{ id: string; heading: string; body: string }>;
}
```

## 3. Tailwind Styling & Design Tokens
- Typography: `prose prose-slate max-w-none`
- Colors: `bg-slate-50 text-slate-900 dark:bg-slate-900 dark:text-slate-100`
- Minimum touch target for links/buttons: >= 48px height/width.

## 4. Accessibility (a11y) Invariants
- Color contrast ratio >= 4.5:1 for normal text, >= 3:1 for large headings.
- Meaningful `alt` attributes on all content images; `alt=""` on purely decorative icons.
