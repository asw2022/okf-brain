---
type: playbook
title: LieferApp-Management
description: LieferApp — Märkte, PLZ-Round-Robin, Fahrer-Ansicht, Drag&Drop, JSON/Telegram
tags: [lieferapp, delivery, management, playbook]
created: 2026-09-22
---

# LieferApp Management Playbook

## System
- Pfad: G:/Download/lieferapp/
- localStorage reset + hard reload bei Problemen
- Never `||1` for vehicle fallback → `||0` verwenden

## Märkte
- PLZ-Round-Robin Zuweisung
- Fahrer-Ansicht mit Drag&Drop
- JSON + Telegram Export

## Workflow
1. Märkte konfigurieren (PLZ-Range)
2. Fahrer zuweisen (Round-Robin)
3. Status check via Hermes
4. Probleme → localStorage reset + hard reload

## Hermes Integration
- Status: `hermes chat -q "LieferApp Status"`
- Export: JSON für Backup, Telegram für Fahrer
