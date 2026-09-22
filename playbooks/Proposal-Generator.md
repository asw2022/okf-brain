---
type: playbook
title: Proposal-Generator
description: Kundenproposal erstellen aus OKF Brain-Daten
tags: [proposal, kunden, sales, playbook]
created: 2026-09-22
---

# Proposal Generator Playbook

## Eingabe
- Kunde (Entity)
- Projekt (Concept)
- Anforderungen (Tags)

## Workflow
1. Kunde aus entities/ laden
2. Relevante Konzepte aus concepts/ suchen
3. Playbooks als Referenz nutzen
4. Draft generieren
5. Human review
6. Finalisieren

## Hermes Integration
- `hermes chat -q "Erstelle Proposal für [Kunde]"`
- OKF Brain als Wissensquelle
- Output: G:/Download/proposals/

## Template
```
# Proposal: [Kunde]
## Projekt
## Anforderungen
## Lösung
## Timeline
## Preis
```
