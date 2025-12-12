# playwright-scriptforge

laywright ScriptForge is a round-trip automation tool for Playwright that bridges the gap between raw recorded code and human-editable browser automation workflows. It ingests Playwright codegen Python output, converts it into a human-readable, YAML-based script with fully parameterized inputs, and compiles that script back into deterministic, executable Playwright Python code for replay.

The goal of ScriptForge is to enable a record once, edit safely, replay many workflow—allowing selectors and interaction flow to remain stable while user-provided inputs such as form values, credentials, and test data can be modified without touching Playwright code directly.

Key Features

Ingests Playwright codegen Python recordings

Converts recorded actions into a human-readable YAML DSL

Automatically parameterizes user inputs

Compiles YAML scripts back into executable Playwright Python code

Supports headless and headed browser execution

Fully CLI-driven and non-interactive

Runs entirely inside a Docker container

Designed for extensibility and future language targets

How It Works

Record
Use Playwright’s codegen to record browser interactions.

Normalize
ScriptForge parses the generated Python code into a structured internal model.

Script
The model is exported as a human-readable YAML script with variable placeholders.

Edit
Users modify inputs and parameters directly in YAML or via environment variables.

Regenerate & Run
ScriptForge compiles the YAML back into Playwright Python code and executes it.

Project Goals

Make Playwright recordings editable without writing code

Preserve selector fidelity and action ordering

Enable repeatable automation with different input sets

Keep execution deterministic and transparent

Remain lightweight, scriptable, and container-friendly

Non-Goals

No graphical UI

No cloud or SaaS dependencies

No test assertion or reporting framework

No automatic healing or AI-based selector changes

Requirements

Python 3.10+

Docker (recommended)

Playwright (installed in container)

Docker Usage

ScriptForge is designed to run entirely in Docker with Playwright and browser dependencies preinstalled.

docker build -t playwright-scriptforge .
docker run --rm -v $(pwd):/work playwright-scriptforge run script.yaml


Environment variables may be injected at runtime to supply parameter values.

CLI Overview

Planned CLI commands include:

record – ingest Playwright codegen output

to-script – convert Playwright code to YAML

to-playwright – compile YAML to Playwright Python

run – execute a script with resolved parameters

All commands are non-interactive and suitable for CI/CD usage.

Architecture Overview

ScriptForge is composed of clearly separated layers:

Parser – ingests Playwright Python code

DSL Model – language-agnostic representation of actions

Generator – emits YAML and Playwright code

Runner – executes generated scripts

This separation allows future support for additional Playwright language targets.

Status

This project is under active development. APIs, DSL schema, and CLI interfaces may change prior to a stable release.

License

MIT License
