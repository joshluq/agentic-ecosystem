# Architecture Specification: Web SSG (Astro & Tailwind)

## 1. Purpose & Scope
This specification governs the static web portals of KiloMenos (Legal, Privacy Policy, Terms of Service, Account Deletion instructions, and Landing Pages).

## 2. Architectural Principles
1. **Zero Unnecessary JavaScript**: All static informational pages ship 0KB client JavaScript by default.
2. **Accessible by Default (WCAG 2.1 AA)**: All interactive elements, navigation bars, and forms are fully keyboard-navigable and screen-reader accessible.
3. **Store Compliance Assurance**: A public URL `/account-deletion` is permanently maintained to satisfy Google Play Store and Apple App Store user account deletion requirements.
