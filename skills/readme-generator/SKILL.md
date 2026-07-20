---
id: readme-generator
name: readme-generator
title: README Generator
summary: Generate standards-compliant README.md files for data engineering repositories.
description: |
  Generate comprehensive README.md files by scanning directory contents (SQL models,
  YAML configs, Python scripts, dbt projects) and producing documentation that covers
  purpose, structure, data flows, and onboarding instructions. Use when a user wants to
  create a README, document a directory, generate getting-started docs, or needs
  repository documentation. Triggers include generate readme, create readme, document
  this repo, add readme, missing readme, documentation gap, getting-started guide,
  onboarding docs, repository documentation. Do not use for API documentation generation,
  code-level docstrings, or changelog generation.
authors: Seayar
status: draft
categories:
  - documentation
  - data-engineering
  - devops
tools:
  - Read
  - Grep
  - Bash
  - Write
prompt: Generate a README for this repository.
language: en
---

# README Generator for Data Engineering Repositories

## Overview

Generate comprehensive, standards-compliant README.md files by scanning directory contents (SQL models, YAML configs, Python scripts, dbt projects) and producing documentation that covers purpose, structure, data flows, and onboarding instructions.

This skill addresses the common DevOps standard: "All repositories must have a README.md with getting-started instructions."

## When To Use

- A directory or repository lacks a README.md
- Existing README is stale or incomplete
- User needs onboarding documentation for a data project
- Documentation gap analysis identified missing READMEs
- User wants to comply with DevOps documentation standards

## When Not To Use

- Generating API-level documentation or code docstrings
- Creating changelogs or release notes
- Writing documentation for non-technical audiences (marketing, product pages)
- When a more specific skill already covers the task (e.g., a dbt docs skill)

## Workflow

### Step 1: Identify Target Directory

**Goal:** Determine which directory needs a README.

**Actions:**

1. **Ask** the user which directory to document:
   - If user already specified a path, use it
   - If ambiguous, ask for clarification
   - Default to current working directory if user says "this directory"

2. **Verify** the directory exists and list its contents

**Output:** Confirmed target path

### Step 2: Scan and Analyze Contents

**Goal:** Understand what the directory contains and its purpose.

**Actions:**

1. **List** all files in the target directory (recursive, 2 levels deep max for initial scan)

2. **Classify** the project type based on file patterns:
   - `.sql` files -> dbt models / SQL transformations
   - `.yml` / `.yaml` files -> dbt schema, ingestion metadata, or config
   - `.py` files -> Python scripts or packages
   - `dbt_project.yml` -> dbt project root
   - `pyproject.toml` / `requirements.txt` -> Python project
   - `Dockerfile` / `docker-compose.yml` -> containerized service
   - Mixed -> hybrid project

3. **Read** key files to understand domain context:
   - Up to 5 representative source files (first 50 lines each)
   - Any existing documentation fragments
   - Config files (dbt_project.yml, pyproject.toml, etc.)

4. **Identify** domain-specific patterns:
   - Table/model names that reveal business domain
   - Column names indicating data subjects (PII, financial, operational)
   - References to external systems or data sources
   - Layer patterns (staging, intermediate, marts, consumption)

**Output:** Project classification and domain context summary

### Step 3: Determine README Sections

**Goal:** Select appropriate sections based on project type.

**Actions:**

Choose sections from this menu based on project type:

| Section | When to Include |
|---------|----------------|
| Title + Description | Always |
| Overview / Purpose | Always |
| Architecture / Data Flow | Multi-layer projects, pipelines |
| Directory Structure | 5+ files or nested directories |
| Prerequisites | External dependencies exist |
| Getting Started | Always (DevOps standard requirement) |
| Configuration | Config files present |
| Models / Components | dbt projects, modular code |
| Data Sources | Ingestion or ETL projects |
| Key Business Rules | SQL with domain logic |
| Domain Glossary | Abbreviations or domain terms found |
| Testing | Test files or test configs present |
| Deployment | CI/CD configs present |
| Contributing | If CONTRIBUTING.md doesn't exist separately |
| Contact / Ownership | Always recommended |

**Present** proposed outline to user for approval.

**MANDATORY STOPPING POINT**: Get user confirmation on the outline before writing.

### Step 4: Generate README Content

**Goal:** Write the README.md content.

**Actions:**

1. **Write** each section following these principles:
   - Lead with **what** and **why** before **how**
   - Use concrete examples from the actual codebase
   - Explain abbreviations and domain terms on first use
   - Include actual file names and paths
   - Keep language accessible to a new team member

2. **Format** using standard markdown:
   - H1 for the project title only
   - H2 for major sections
   - H3 for subsections within
   - Fenced code blocks with language tags
   - Tables for structured comparisons
   - Bullet lists for enumerations

3. **Include** a "Last Updated" date at the bottom

**Quality checks before presenting:**
- No placeholder text (e.g., "[TODO]", "INSERT HERE")
- All referenced files actually exist in the directory
- Getting-started instructions are actionable (specific commands)
- No sensitive information (passwords, tokens, internal URLs without user approval)

**Output:** Complete README.md draft

### Step 5: Review and Finalize

**Goal:** Get user approval and write the file.

**Actions:**

1. **Present** the full README to the user

2. **MANDATORY STOPPING POINT**: Ask for approval or requested changes

3. **If approved:** Write the file to `<target_directory>/README.md`

4. **If changes requested:** Apply edits and re-present

**Output:** Written README.md file

## README Templates by Project Type

### dbt Project README Structure
```markdown
# [Project Name]

## Overview
[What this project does, what data domain it covers]

## Data Flow
[Source] -> [Staging] -> [Intermediate] -> [Marts/Consumption]

## Models
| Model | Layer | Description |
|-------|-------|-------------|
| model_name | staging | Brief purpose |

## Prerequisites
- dbt CLI installed (version X+)
- Access to [warehouse/database]
- Profiles configured in `~/.dbt/profiles.yml`

## Getting Started
1. Clone the repository
2. Install dependencies: `dbt deps`
3. Test connection: `dbt debug`
4. Run models: `dbt run --select [selector]`

## Domain Glossary
| Abbreviation | Meaning |
|---|---|
| ABBR | Full Term |
```

### Ingestion / ETL README Structure
```markdown
# [Pipeline Name]

## Overview
[What data sources, what destination, what frequency]

## Data Sources
| Source | Format | Frequency | Description |
|--------|--------|-----------|-------------|

## Configuration
[How YAML/config files control behavior]

## Getting Started
1. [Environment setup]
2. [Configuration steps]
3. [How to run locally]

## Monitoring
[How to check pipeline health]
```

### Python Package README Structure
```markdown
# [Package Name]

## Overview
[Purpose and capabilities]

## Installation
pip install [package]

## Usage
[Quick example]

## API Reference
[Key functions/classes]

## Development
1. Clone and install: `pip install -e ".[dev]"`
2. Run tests: `pytest`
```

## Stopping Points

- After Step 3 (outline approval)
- After Step 4 (content review before writing)
- If sensitive information detected (PII references, credentials)

## Common Mistakes

- Generating a README without reading the actual source files first
- Including placeholder text that was never filled in
- Referencing files or paths that don't exist in the directory
- Omitting Getting Started instructions (violates DevOps standard)
- Including sensitive information like connection strings or internal URLs
- Making the README too generic without domain-specific context

## Output

A complete `README.md` file written to the target directory.
