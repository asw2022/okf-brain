---
type: playbook
title: Hermes-Quant-Trading
description: Autonomer Quant-Market-Engine mit Hermes — Paper Trading first
tags: [quant, trading, hermes, market, autonomous]
created: 2026-09-22
---

# Hermes Quant Trading Playbook

## Setup
```bash
hermes quant setup conservative
hermes quant doctor
```

## Workflow
1. **Scan** — Market scan alle 30 Min
2. **Signal** — ARIA Multi-Analyst generiert Signale
3. **Paper Trade** — Nur Paper Trading initially
4. **Report** — Daily + Weekly auto-report
5. **Review** — Human review before any live

## Commands
| Befehl | Zweck |
|---|---|
| `hermes quant start` | Daemon starten |
| `hermes quant signals -n 20 --follow` | Live-Signale |
| `hermes quant status` | Status check |
| `hermes quant doctor` | Health check |

## Sample Status
```
Daemon: running (uptime 23h 14m)
Letzter Tick: BTC/USDT 1h
Signale: 4 (3 long, 1 flat)
Position: 1 long BTC @ 7% NAV
P&L heute: +$12.34 (paper)
```

## Für unser System
- Ollama 192.168.0.147 als Host
- CPU-only kompatibel
- yfinance für Daten
- **NUR Paper Trading bis验证完成**

## Safety Rules
1. Never go live without 48h paper testing
2. Max position: 7% NAV
3. Conservative profile default
4. Daily P&L check mandatory
5. Stop if loss > X% in one day
