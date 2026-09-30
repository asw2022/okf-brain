---
type: reference
title: AI Agents 2026 — Subagent-Orchestrierung
description: Boss-Agent-Pattern, Retry Logic und Agent City für Hermes Multi-Agent Setup
tags: [newsletter, hermes, agents, 2026-09]
created: 2026-09-28
updated: 2026-09-28
source: https://nevercodealone.de/de/glossare/ki-tools-2026/hermes-agent-anwendungsfaelle
issue_number: 2
topic: Subagent-Orchestrierung
summary: So koordinieren Coordinator, Researcher, Writer und Reviewer als Team — Boss-Agent wählt den Spezialisten, Retry Logic bei Fehlern, Agent City zeigt den Status.
---

# AI Agents 2026 — Subagent-Orchestrierung

## TL;DR
Hermes Agenten arbeiten nicht isoliert — der Coordinator agiert als Boss-Agent, weist Aufgaben zu und überwacht den Fortschritt. Bei Fehlern greift Retry Logic mit exponentieller Backoff. Die Agent City zeigt auf einen Blick, wer arbeitet und wer bereit ist.

## 1. Boss-Agent Pattern
Der Coordinator ist der Boss-Agent. Er analysiert eine Aufgabe, wählt den besten Spezialisten und delegiert:

- **Coordinator** (strong) — Orchestrierung, Team-Auswahl
- **Researcher** (medium) — Recherche, Web-Queries
- **Writer** (medium) — Content-Erstellung
- **Reviewer** (strong) — Validierung, Faktencheck

Der Boss entscheidet anhand des Aufgabentyps: Research → Researcher, Content → Writer, Review → Reviewer.

## 2. Retry Logic
Fehlgeschlagene Missionen werden mit exponentiellem Backoff neu gestartet:

- Retry 1: 2s Wartezeit
- Retry 2: 4s Wartezeit
- Retry 3: 8s Wartezeit → dann als failed markiert

Jede Rolle hat eigene Retry-Limits (Researcher/Writer: 2, Reviewer: 3).

## 3. Agent City Heatmap
Die TUI-Ansicht zeigt alle Agenten als Status-Übersicht:

- 🔵 working — aktive Mission
- 🟢 available — bereit für neue Aufgabe

\`\`\`
  coordinator     🟢 available     [strong]
  researcher      🔵 working       [medium]
  writer          🟢 available     [medium]
  reviewer        🟢 available     [strong]
\`\`\`

## 4. NEXORA vs. unser Setup
Das NEXORA Dashboard (Komputer Mechanic, Sept 2026) bietet 3D-Visualisierung und Hand-Steuerung. Wir setzen auf schlankes TUI — weniger Overhead, gleiche Funktion: Boss-Agent + Retry + Status-Übersicht.

## 5. Nächste Ausgabe
Content-Pipeline Skill ist aktiv. Newsletter #2 folgt mit Deploy-Log.

## Cross-Refs
- [[Hermes-Agent]] — Agent-Architektur
- [[Lokale-KI-Modelle-2026]] — Modell-Runner
- [[OKF-Format]] — Style-Vorlage

---

Quellen: 27 (24 OKF Brain + 3 Web) | Erstellt: 2026-09-28 | Issue #2
(c) ASW Labs