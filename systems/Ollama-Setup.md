---
type: system
title: Ollama-Setup
description: Ollama auf Linux 192.168.0.147 — 3 lokale Modelle, Hermes verbunden
tags: [ollama, linux, hermes, local-ai]
created: 2026-09-22
---

# Ollama Setup

## Server
- Host: 192.168.0.147
- Port: 11434
- Status: aktiv, enabled on boot

## Modelle
| Modell | Größe | Use Case |
|---|---|---|
| llama3.2:3b | 2.0GB | Standard (Hermes default) |
| phi3:mini | 2.2GB | Schnelle Antworten |
| gemma2:2b | 1.6GB | Einfache Tasks |

## Hermes Integration
- Provider: ollama
- Base URL: http://192.168.0.147:11434/v1
- Default: llama3.2:3b
- Context: 8192

## Zugriff
- Localhost: `ollama run llama3.2:3b`
- Remote: `curl http://192.168.0.147:11434/api/tags`
- Win11: LM Studio → Remote: http://192.168.0.147:11434
