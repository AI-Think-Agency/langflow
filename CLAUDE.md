# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Langflow is a visual workflow builder for AI-powered agents. It has a Python/FastAPI backend, React/TypeScript frontend, and a lightweight executor CLI (lfx).

## Prerequisites

- Python 3.10-3.13, uv >=0.4
- Node.js >=20.19.0 (v22.12 LTS recommended), npm v10.9+
- `make` for build coordination

## Common Commands

### Development Setup
```bash
make init              # Install all dependencies + pre-commit hooks
make run_cli           # Build and run Langflow (http://localhost:7860)
make run_clic          # Clean build and run (use when frontend issues occur)
```

### Development Mode (Hot Reload)
```bash
make backend           # FastAPI on port 7860
make frontend          # Vite dev server on port 3000
```

For component development with dynamic loading:
```bash
LFX_DEV=1 make backend                    # Load all components dynamically
LFX_DEV=mistral,openai make backend       # Load only specific modules
```

### Code Quality
```bash
make format_backend    # Format Python (ruff) — run FIRST before lint
make format_frontend   # Format TypeScript (biome)
make lint              # mypy type checking
```

### Testing
```bash
make unit_tests                                    # Backend unit tests (pytest, parallel)
make unit_tests async=false                        # Sequential
uv run pytest path/to/test.py                      # Single test file
uv run pytest path/to/test.py::test_name           # Single test

make test_frontend                                 # Jest unit tests
make tests_frontend                                # Playwright e2e tests
```

Always use `uv run` when running Python commands directly.

### Database Migrations
```bash
make alembic-revision message="Description"  # Create migration
make alembic-upgrade                         # Apply migrations
make alembic-downgrade                       # Rollback one version
```

## Architecture

### Monorepo Structure
```
src/
├── backend/
│   ├── base/langflow/     # Core backend package (langflow-base)
│   │   ├── api/           # FastAPI routes (v1/, v2/)
│   │   ├── components/    # Built-in Langflow components
│   │   ├── services/      # Service layer (auth, database, cache, etc.)
│   │   ├── graph/         # Flow graph execution engine
│   │   └── custom/        # Custom component framework
│   └── tests/             # Backend tests
├── frontend/              # React/TypeScript UI
│   └── src/
│       ├── components/    # UI components
│       ├── stores/        # Zustand state management
│       └── icons/         # Component icons
└── lfx/                   # Lightweight executor CLI
```

### Key Packages
- **langflow**: Main package with all integrations
- **langflow-base**: Core framework (api, services, graph engine)
- **lfx**: Standalone CLI for running flows (`lfx serve`, `lfx run`)

### Frontend Stack
React 19 + TypeScript + Vite, Zustand for state, `@xyflow/react` for graph visualization, Tailwind CSS for styling.

## Component Development

Components live in `src/backend/base/langflow/components/`. To add a new component:

1. Create component class inheriting from `Component`
2. Define `display_name`, `description`, `icon`, `inputs`, `outputs`
3. Add to `__init__.py` (alphabetical order)
4. Run with `LFX_DEV=1 make backend` for hot reload

**IMPORTANT:** Never rename a component's class name — it is used as an identifier in saved flows. Renaming breaks existing flows.

```python
from langflow.custom import Component
from langflow.io import MessageTextInput, Output

class MyComponent(Component):
    display_name = "My Component"
    description = "What it does"
    icon = "component-icon"  # Lucide icon name or custom

    inputs = [MessageTextInput(name="input_value", display_name="Input")]
    outputs = [Output(display_name="Output", name="output", method="process")]

    def process(self) -> Message:
        return Message(text=self.input_value)
```

Component tests go in `src/backend/tests/unit/components/` using:
- `ComponentTestBaseWithClient` — components needing API access
- `ComponentTestBaseWithoutClient` — pure logic components

Required fixtures: `component_class`, `default_kwargs`, `file_names_mapping`

## Custom Icons

1. Create SVG component in `src/frontend/src/icons/YourIcon/`
2. Export with `forwardRef` and `isDark` prop support
3. Add to `lazyIconImports.ts`
4. Set `icon = "YourIcon"` in the Python component

## Testing Notes

- `@pytest.mark.api_key_required` — tests requiring external API keys
- `@pytest.mark.no_blockbuster` — skip blockbuster plugin
- Database tests may fail in batch but pass individually
- Pre-commit hooks require `uv run git commit`
- Avoid mocking when possible; prefer real integrations

### Graph Testing Pattern

1. Build graph with connected components
2. Connect them via `.set()` calls
3. Call `async_start` and iterate over results
4. Validate results

## Pre-commit Workflow

1. `make format_backend` (run first)
2. `make format_frontend`
3. `make lint`
4. `make unit_tests`
5. `uv run git commit` (if pre-commit hooks are enabled)

## Version Management

```bash
make patch v=1.5.0  # Update version across pyproject.toml files and package.json
```

## Documentation

```bash
cd docs && yarn install && yarn start  # Dev server on port 3000
```
