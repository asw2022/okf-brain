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

## Märkte (10 aktiv)
| Markt | PLZ-Range | Status |
|---|---|---|
| Rewe | 10000-14999 | ✅ aktiv |
| EDEKA | 15000-19999, 40000-44999 | ✅ aktiv |
| Kaufland | 20000-24999 | ✅ aktiv |
| Aldi | 25000-29999, 60000-64999 | ✅ aktiv |
| Lidl | 30000-34999 | ✅ aktiv |
| Penny | 35000-39999 | ✅ aktiv |
| Netto | 45000-49999, 70000-74999 | ✅ aktiv |
| DM | 50000-54999, 80000-84999 | ✅ aktiv |
| Rossmann | 55000-59999, 90000-94999 | ✅ aktiv |
| Fressnapf | 65000-69999, 75000-79999, 85000-89999, 95000-99999 | ✅ aktiv |

## Fahrer (Round-Robin)
| ID | Name | PLZ-Gebiet | Max Pakete | Status |
|---|---|---|---|---|
| F001 | Alex | 10-16 | 15 | aktiv |
| F002 | Maria | 20-29 | 15 | aktiv |
| F003 | Samir | 30-39 | 15 | aktiv |

## Aktuelle Aufträge (Sample)
| ID | PLZ | Markt | Priorität |
|---|---|---|---|
| A-001 | 10115 | Rewe | dringend |
| A-002 | 12000 | Rewe | normal |
| A-003 | 14500 | Rewe | spät |
| A-004 | 16000 | EDEKA | dringend |
| A-005 | 18300 | EDEKA | normal |

## Workflow
1. Märkte konfigurieren (10 aktiv, PLZ-Range)
2. Fahrer zuweisen (Round-Robin: Alex 10-16, Maria 20-29, Samir 30-39)
3. Aufträge zuweisen (PLZ → Markt → Fahrer)
4. Status check via Hermes
5. Telegram Export für Fahrer
6. Probleme → localStorage reset + hard reload

## Dateien
- `lieferapp-data.json` — Master data (409 Zeilen)
- `maerkte.py` — Market config + PLZ lookup
- `fahrer.py` — Driver management
- `kanban_router.py` — Task routing
- `telegram_bot.py` — Telegram integration
- `dashboard.html` — Dashboard
- `lieferapp-pwa.html` — PWA

## Hermes Integration
- Status: `hermes chat -q "LieferApp Status"`
- Export: JSON für Backup, Telegram für Fahrer
