---
type: concept
title: OKF-Format
description: Open Knowledge Format — standardisierte Markdown-Struktur für Agenten-lesbares Wissen
tags: [okf, format, standard, google]
created: 2026-09-22
source: https://www.mariehaynes.com/okf/
---

# OKF-Format

## Was ist OKF?
Google's Open Knowledge Format — standardisierte Markdown-Struktur mit YAML Frontmatter, damit jeder Agent (Claude, Codex, Antigravity, Hermes) darauf zugreifen kann.

## Struktur
```
brain/
├── index.md          # Inhaltsverzeichnis
├── concepts/         # Wissensbausteine
├── entities/         # Verlinkte Objekte
├── playbooks/        # Abläufe/Schritte
├── references/       # Dokumente & Quellen
└── systems/          # Technische Specs
```

## YAML Frontmatter (Pflicht)
```yaml
---
type: concept|entity|playbook|reference|system
title: ...
description: ...
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: URL
---
```

## OKF vs RAG
| RAG | OKF |
|---|---|
| Alles in Context Window | Index-basiert, selektiv |
| Token-expensive | Token-efficient |
| Kein Discovery | Index + Tags + Graph |
| Einmalig | Wiederverwendbar |

## Key Insight
> „OKF ist kein RAG-Ersatz, sondern ein Index davor. Der Agent liest den Index, findet die relevanten Dateien, und ragt nur die Brauchbrauch."
