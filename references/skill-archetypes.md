# Skill Archetypes

Choose the lightest pattern that fits the task.

## Tool Wrapper

Wraps an external tool or API into a skill.

- Trigger: user asks to use a specific tool
- Structure: SKILL.md with CLI commands, references for flags/options
- Examples: yt-dlp-downloader, music-downloader

## Generator

Produces files or content from inputs.

- Trigger: user asks to create something
- Structure: SKILL.md with output format specs, templates in assets/
- Examples: pptx-generator, drawio-diagram

## Reviewer

Analyzes existing content and provides feedback.

- Trigger: user asks to review, audit, or check something
- Structure: SKILL.md with checklists, references for criteria
- Examples: code review, document analysis

## Pipeline

Chains multiple steps into a workflow.

- Trigger: user describes a multi-step process
- Structure: SKILL.md with step sequence, scripts for each step
- Examples: CI/CD setup, data processing

## Inversion

Transforms one format into another.

- Trigger: user asks to convert or transform
- Structure: SKILL.md with mapping rules, scripts for conversion
- Examples: convertx, markdown-to-X

## How to Choose

1. Is it about a specific tool? → Tool Wrapper
2. Creating something new? → Generator
3. Analyzing existing content? → Reviewer
4. Multiple steps in sequence? → Pipeline
5. Converting formats? → Inversion

When unsure, start with Generator — it's the most flexible.
