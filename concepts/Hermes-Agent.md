---
type: concept
title: Hermes-Agent
description: Hermes Agent Fähigkeiten, Architektur und Konfiguration
tags: [hermes, agent, ai, assistant]
created: 2026-09-28
updated: 2026-09-28
source: 
---

# Hermes-Agent

## Überblick
Hermes ist ein persönlicher AI-Agent mit CLI, Desktop-App, Gateway (Telegram/Discord/Slack) und TUI. Kern: schmales Model-Tool-Interface, Fähigkeiten leben in Plugins/Skills.

## Architektur
- Core: run_agent.py (AIAgent-Klasse), model_tools.py, toolsets.py
- CLI: cli.py + hermes_cli/ (Subcommands, Skin-Engine)
- Gateway: gateway/run.py + gateway/platforms/ (Adapter)
- Plugins: plugins/ (memory, model-providers, kanban, observability)
- Skills: skills/ + optional-skills/

## Toolsets
- Core-Tools: terminal, read_file, web_search, browser_navigate, execute_code
- Plugins fügen Toolsets hinzu ohne Core zu berühren
- Footprint-Ladder: Core nur wenn nicht möglich über CLI/Plugin/MCP

## Konfiguration
- ~/.hermes/config.yaml — Einstellungen
- ~/.hermes/.env — Secrets only
- Profile: ~/.hermes/profiles/<name>/

## Entwicklung
- Python 3.14, uv für Dependency-Management
- Tests: scripts/run_tests.sh (CI-parität)
- TUI: Ink (React) + JSON-RPC stdio
- Desktop: Electron + React + nanostore

## Key Patterns
- Per-conversation prompt caching ist sacred
- Neue Tools nur über Footprint-Ladder
- Plugins ≠ Core-Änderungen
- Profile-sicheres Code: get_hermes_home() nicht hardcoded
