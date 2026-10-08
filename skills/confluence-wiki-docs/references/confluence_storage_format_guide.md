# Confluence XHTML Storage Format Conversion Guide

This guide describes how Markdown elements are mapped into Confluence Cloud XHTML Storage Representation.

---

## 1. Storage Format Architecture

Confluence Cloud REST API accepts `body.storage.value` with `representation: "storage"` using XHTML syntax.

---

## 2. Element Mappings

### Headers & Paragraphs
- `# Title` $\rightarrow$ `<h1>Title</h1>`
- `## Subtitle` $\rightarrow$ `<h2>Subtitle</h2>`
- Text paragraphs $\rightarrow$ `<p>Paragraph text</p>`

### Code Blocks
Markdown code fences:
```xml
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">kotlin</ac:parameter>
  <ac:plain-text-body><![CDATA[val state = ProfileUiState.Loading]]></ac:plain-text-body>
</ac:structured-macro>
```

### Callout Panels (Info, Warning, Note)
```xml
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p><strong>Note:</strong> Business rules must be verified in Stage 1.</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Tables
Standard HTML `<table>` elements with Confluence styling:
```xml
<table>
  <thead>
    <tr><th>Column 1</th><th>Column 2</th></tr>
  </thead>
  <tbody>
    <tr><td>Value A</td><td>Value B</td></tr>
  </tbody>
</table>
```
