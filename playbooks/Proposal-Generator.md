---
type: playbook
title: Proposal-Generator
description: Kundenproposal erstellen aus OKF Brain-Daten
tags: [proposal, kunden, sales, playbook]
created: 2026-09-22
updated: 2026-09-22
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

## Template (befüllt)
```markdown
# Proposal: [Kunde]

## Projekt
- Konzept: [aus concepts/]
- Scope: [beschreiben]

## Anforderungen
- [Aus OKF Brain entnommen]
- Playbook Referenz: [ref]

## Lösung
- [Beschreibung basierend auf Brain-Daten]

## Timeline
- Phase 1: [Dauer]
- Phase 2: [Dauer]
- Phase 3: [Dauer]

## Preis
- [Kalkulation basierend auf Scope]

## Status
- Draft → Review → Final
```

## Beispiel-Filling (OKF Brain Setup)
- Kunde: ASW
- Konzept: OKF Brain G:/Download/OKF-Brain/
- Anforderungen: Ingest+Query Skills, GitHub Backup, Daily Cron
- Lösung: 16 Dateien, 6 Playbooks, automatischer Backup
- Timeline: 1 Woche Setup + laufend
- Preis: Kostenlos (lokal)
