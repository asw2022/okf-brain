---
type: entity
title: Linux-Server
description: ASW Linux Rechner 192.168.0.147 — SSH, BrainMemory, Ollama, A2A-Tunnel
tags: [linux, server, asw, ssh, brainmemory, ollama]
created: 2026-09-28
updated: 2026-09-28
source: 
---

# Linux-Server

## Hardware
- IP: 192.168.0.147
- RAM: 3.6 GB
- SSH: Port 22 (von Windows aus)
- A2A-Tunnel: 9901→9900, bearer asw-local-a2a-2026

## Services
- BrainMemory: python3 app.py auf Port 8011 (0.0.0.0)
- Ollama: 3 Modelle, Port 11434
- UFW Firewall: Port 8011 offen

## Cron Jobs
- Status alle 30min
- Security alle 2h
- Voice um 07:00
- OSCam alle 3h

## Notes
- Linux 192.168.0.147: 3.6GB RAM, schwach
- Cloud bevorzugt über Local GPU
- A2A-Tunnel Win→Linux SSH 9901→9900 FIXED

## Related
- [[Hermes-Desktop]] — Windows Host
- [[A2A-Tunnel]] — Tunnel-Konfiguration
- [[Brain-Dashboard]] — Visualisierung
