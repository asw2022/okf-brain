---
type: playbook
title: Kanban-Management
description: Kanban Board Task Flow — todo → in-progress → review → done
tags: [kanban, workflow, task-management, playbook]
created: 2026-09-22
---

# Kanban Management Playbook

## Board
- Datei: G:/Download/kanban-asw.html
- localStorage-basiert
- Drag&Drop, Tags, JSON/Telegram-Export

## Spalten
1. **todo** — neue Tasks
2. **in-progress** — aktiv bearbeitet
3. **review** — zur Prüfung bereit
4. **done** — abgeschlossen

## Workflow
1. Task erstellen → todo
2. Bearbeitung starten → in-progress
3. Fertig → review (Human check)
4. Genehmigt → done

## Hermes Integration
- `/kanban` für Status
- Agent kann Cards erstellen/aktualisieren
- Telegram Export für unterwegs

## Regeln
- Immer nach G:/Download/ speichern
- Kein C: (nicht doppelt ablegen)
- JSON Backup regelmäßig
