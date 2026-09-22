---
type: concept
title: Prompt-Engineering
description: Prompt techniques for Hermes agents — search-box vs. proactive assistant
tags: [hermes, prompt, technique, ai]
created: 2026-09-22
---

# Prompt Engineering

## Search-Box Mode (default)
- One question → one answer
- No planning, no verification
- Reactive only

## 200 IQ Mode (Joon Ahn technique)
- Goal → Plan → Execute
- Source verification required
- Proactive, iterative

## Rules
1. Always give a goal, not just a question
2. Ask for a plan before execution
3. Require source citations
4. Iterate on results

## Hermes-Specific
- Use OKF Brain as context
- Reference playbooks explicitly
- Ask for confirmation on complex tasks
