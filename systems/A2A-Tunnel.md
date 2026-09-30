---
type: system
title: A2A-Tunnel
description: Windows→Linux SSH A2A-Tunnel 9901→9900, bearer asw-local-a2a-2026, peer 127.0.0.1:9901
tags: [a2a, tunnel, ssh, windows, linux]
created: 2026-09-28
updated: 2026-09-28
source: 
---

# A2A-Tunnel

## Overview
A2A (Agent-to-Agent) Tunnel von Windows nach Linux über SSH.

## Config
- Windows: Peer 127.0.0.1:9901
- Linux: Port 9900 (lokal)
- SSH: Port 22
- Bearer: asw-local-a2a-2026

## Status
- ✅ FIXED (2026-09-28)
- Bearer nur in default-Profil (ollama-local hatte Duplikat)

## Related
- [[Linux-Server]] — 192.168.0.147
- [[Hermes-Desktop]] — Windows Host
