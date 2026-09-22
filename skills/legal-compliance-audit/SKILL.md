---
name: legal-compliance-audit
description: Audits mobile and web legal compliance (Terms and Conditions, Privacy Policy, GDPR/RGPD, App Store & Google Play requirements, data retention, account deletion).
---

# Legal & Regulatory Compliance Audit

Skill specialized in regulatory auditing and compliance for **mobile apps and accompanying static web portals** (Terms & Conditions, Privacy Policy, Cookie Policy).

---

## 1. Google Play & App Store Mandatory Compliance Checklist

### 1.1 Privacy Policy (`/privacy` or `/politica-privacidad`)
- [ ] Explicit identity of the Data Controller (company/developer name, official contact email).
- [ ] Explicit enumeration of data collected:
  - Account info: Email, user ID.
  - Vehicle data: Plate numbers, contract start/end dates, mileage limits.
  - Telemetry & Location: Bluetooth sensor data, background location (if enabled for auto-tracking).
- [ ] Legal basis under GDPR (Consent, Contract fulfillment, Legitimate interest).
- [ ] Data retention periods (e.g. data preserved during active subscription + 5 years for legal/tax accounting).
- [ ] Third-party processors list: Supabase (Hosting/DB), Google Play Services (Auth/In-app purchase).

### 1.2 Account & Data Deletion Requirement (Play Store Rule)
- [ ] A dedicated public web URL MUST exist allowing users to request account and data deletion without having to open the app.
- [ ] Clear SLA for deletion (e.g. within 30 days).

### 1.3 Terms and Conditions (`/terms` or `/terminos-y-condiciones`)
- [ ] Limitation of liability regarding vehicle mileage tracking accuracy (app is an informational tool, leasing contract rules supersede).
- [ ] Subscription, pricing, and cancellation policy.
- [ ] Intellectual property rights.
- [ ] Governing law and dispute resolution jurisdiction.

---

## 2. Standard Semantic HTML Structure

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Términos y Condiciones - KiloMenos</title>
  <meta name="description" content="Términos y Condiciones del servicio KiloMenos.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="legal-header">
    <div class="container">
      <h1>KiloMenos</h1>
      <p class="updated-at">Última actualización: 22 de Septiembre de 2026</p>
    </div>
  </header>

  <main class="container legal-content">
    <section>
      <h2>1. Información General y Titularidad</h2>
      <p>El presente documento regula el uso de la aplicación móvil KiloMenos...</p>
    </section>

    <section>
      <h2>2. Política de Supresión de Datos</h2>
      <p>Para solicitar el borrado integral de su cuenta y registros de kilometraje, envíe un correo a <a href="mailto:soporte@kilomenos.es">soporte@kilomenos.es</a> o utilice nuestro formulario web.</p>
    </section>
  </main>

  <footer class="legal-footer">
    <div class="container">
      <p>&copy; 2026 KiloMenos. Todos los derechos reservados.</p>
    </div>
  </footer>
</body>
</html>
```
