---
name: JEPA World Model
type: architecture
status: draft
author: ASW Labs
based_on: Yann LeCun NYU Talk 2026-09-30
---

# JEPA World Model Architecture

## Core Idea
Statt nächsten Token vorherzusagen (LLM), vorhersagen wir in
Repräsentationsraum, was als Nächstes im physikalischen Zustand passiert.

## Komponenten

| Modul | Aufgabe |
|-------|---------|
| PerceptionModule | Beobachtung → Repräsentation |
| JEPA Core | Vorhersage in Repräsentationsraum (nicht Pixel) |
| EnergyFunction | Bewusstsein/Kompatibilität als Skalarfeld |
| GuardrailObjective | Sicherheit als optimierbare Constraint |
| HierarchicalPlanner | Goal → Sub-goal → Action Hierarchie |

## Inferenz
Kein Autoregressives Token-Generieren. Stattdessen:
1. Wahrnehmung → aktueller Zustand `s`
2. Candidate-Aktionen generieren
3. Weltmodell sagt `s'` für jede Kandidaten-Aktion voraus
4. Energy `E(s', goal)` minimieren → beste Aktion
5. Guardrails prüfen → ausführen

## Safety
Guardrails sind Teil der Energy-Funktion, kein nachträglicher Filter.
System kann nicht gegen Constraints optimieren, weil Constraints die
Energy direkt definieren.

## Status
- Referenz-Implementierung: `systems/jepa_world_model.py`
- Demo: `systems/jepa_demo.py`
- Tests: `systems/test_jepa.py`
