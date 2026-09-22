---
type: playbook
title: OKF-Ingest
description: Neues Material aufnehmen, strukturieren und in den OKF Brain integrieren
tags: [okf, ingest, workflow, agent]
created: 2026-09-22
---

# OKF Ingest Playbook

## Eingabe
- URL, Text, Datei oder Transkript

## Schritt 1: Analyse
Lies das Material und identifiziere:
1. Welche Konzepte entstehen?
2. Welche Entitäten sind betroffen?
3. Passt es zu einem bestehenden Playbook?
4. Soll es eine neue Reference werden?

## Schritt 2: Struktur vorschlagen
Erstelle einen Vorschlag im Markdown-Format mit YAML Frontmatter.

## Schritt 3: Human Approval
Zeige den Vorschlag dem User zur Genehmigung.
- ✅ Genehmigt → speichern
- ✏️ Edit → anpassen, dann speichern
- ❌ Reject → verwerfen, Log-Eintrag

## Schritt 4: Speichern
- Datei im richtigen Ordner ablegen
- index.md aktualisieren
- Log-Eintrag schreiben

## Schritt 5: Verknüpfen
Tags prüfen, Cross-References zu existierenden Dateren hinzufügen.
