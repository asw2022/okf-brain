---
type: playbook
title: OKF-Query
description: Wissen aus dem OKF Brain abfragen und zusammenfassen
tags: [okf, query, search, agent]
created: 2026-09-22
---

# OKF Query Playbook

## Eingabe
- Natürliche Sprachfrage oder Suchbegriff

## Schritt 1: Index lesen
Lade `index.md` und identifiziere relevante Dateien nach:
- Tags matching
- Type matching
- Titel/Description matching

## Schritt 2: Dateien selektieren
Lese nur die relevanten Dateien (nicht den ganzen Brain!).

## Schritt 3: Zusammenfassen
Generiere eine präzise Antwort basierend auf den gefundenen Dateien.

## Schritt 4: Quellen angeben
Liste die verwendeten Dateien mit Pfad auf.

## Beispiel
```
Frage: "Wie ist das Ollama-Setup?"
→ index.md → systems/Ollama-Setup.md
→ Antwort mit Details + Quelle
```
