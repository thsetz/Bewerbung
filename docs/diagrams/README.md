# Mermaid Diagrams

This directory contains standalone Mermaid diagrams for the Bewerbung Generator project. Each diagram is available in two formats:

- `.mmd` files: Pure Mermaid syntax for development and testing
- `.html` files: Standalone HTML pages with interactive rendering

## Available Diagrams

### 🔄 [System Workflow](system-workflow.html)
**File:** `system-workflow.mmd` | **View:** [system-workflow.html](system-workflow.html)

Illustrates the complete 7-step application generation process from cache clearing through PDF conversion.

### 🤖 [AI Provider Selection](ai-provider-selection.html)
**File:** `ai-provider-selection.mmd` | **View:** [ai-provider-selection.html](ai-provider-selection.html)

Shows the intelligent multi-provider fallback chain (Llama → Claude → Sample Content).

### 🏗️ [Directory Structure](directory-structure.html)
**File:** `directory-structure.mmd` | **View:** [directory-structure.html](directory-structure.html)

Demonstrates the clean directory-only output organization with AI provider separation.

### 🏗️ [System Architecture](system-architecture.html)
**File:** `system-architecture.mmd` | **View:** [system-architecture.html](system-architecture.html)

High-level component overview showing the modular architecture with CLI, core components, AI providers, and analysis tools.

## Usage

### Viewing Diagrams
- **Interactive HTML:** Open any `.html` file in a web browser for rendered diagrams
- **Raw Mermaid:** View `.mmd` files for the source syntax

### Development
- **Edit:** Modify `.mmd` files to update diagram content
- **Regenerate:** Update corresponding `.html` files after making changes
- **Testing:** Use Mermaid CLI or online editor to validate syntax

### Integration
These diagrams are referenced from:
- `README.md` (root project documentation)
- `docs/index.rst` (Sphinx documentation)
- `docs/development/architecture.rst` (architecture documentation)

## Mermaid Resources

- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/)
- [Online Editor](https://mermaid.live/)
- [Syntax Reference](https://mermaid-js.github.io/mermaid/#/flowchart)