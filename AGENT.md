# Agent Instructions

This repository contains a collection of modular AI Agent Skills focused on project modernization and maintenance.

## Navigation

- Each subdirectory (e.g., `flutter-updater/`, `go-updater/`) is a self-contained skill or a component of one.
- The `SKILL.md` file within each directory provides specific instructions and context for that skill.
- The `java-updater.skill` file is a standalone skill definition.
- `TODO.md` tracks the progress of updating specific projects and packages.

## Guidelines for Usage

1. **Activate Relevant Skills**: Before performing any modernization tasks, identify the most appropriate skill (based on the project's language or framework) and activate it.
2. **Context-Specific Instructions**: Follow the guidance provided in the `SKILL.md` file of the activated skill.
3. **Project Independence**: These skills are designed to operate on projects *external* to this repository. Do not modify the projects themselves within this repository unless they are being used for testing or template purposes.
4. **Submodules**: Some projects may be linked as submodules to provide context or testing grounds for the skills.

## Structure

- `*-updater/`: Skill definitions, prompts, and resources.
- `issue-triage/`: Skill for triaging and responding to GitHub issues.
- `package-updater/assets/`: Shared GitHub Action workflows and templates.
- `java-updater.skill`: Standalone skill definition for Java.
