# Developer Documentation

This guide provides comprehensive instructions for developers who want to contribute to or extend the Docling MCP project.

## Project History

This repository is a **fork of [docling-mcp](https://github.com/docling-project/docling-mcp)**, extended and customized for our specific use cases and requirements. The original Docling MCP project provides a document processing service using the Model Context Protocol (MCP) for tool integration.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install uv Package Manager](#2-install-uv-package-manager)
  - [3. Set Up Python Environment](#3-set-up-python-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Apple Silicon Development Setup](#5-apple-silicon-development-setup)
- [Running the Development Server](#running-the-development-server)
- [Setting Up MCP Inspector](#setting-up-mcp-inspector)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
  - [Using MCP Inspector](#using-mcp-inspector)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style and Quality](#code-style-and-quality)
- [Testing](#testing)
- [Debugging](#debugging)
- [Building and Publishing](#building-and-publishing)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.10 or higher** (3.10, 3.11, 3.12, or 3.13)
- **uv** package manager (installation instructions below)
- (Optional) **Docker** and **Docker Compose** for containerized development

## Development Setup

### 1. Clone the Repository

First, clone the Docling MCP repository to your local machine:

```bash
git clone git@github.com:docling-project/docling-mcp.git
cd docling-mcp
```


### 2. Install uv Package Manager

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager written in Rust. We use it for managing dependencies and virtual environments.

**Install on macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Install on Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative installation methods:**

```bash
# Using pip
pip install uv

# Using pipx
pipx install uv

# Using Homebrew (macOS)
brew install uv
```

Verify installation:

```bash
uv --version
```

### 3. Set Up Python Environment

uv will automatically create a virtual environment for the project. You can optionally specify a Python version:

**Use the default Python version:**

```bash
uv venv
```

**Or specify a particular Python version:**

```bash
# For Python 3.12
uv venv --python 3.12

# For Python 3.11
uv venv --python 3.11

# For Python 3.10
uv venv --python 3.10
```

The virtual environment will be created in the `env/` directory (or `.venv/` depending on your configuration).

### 4. Install Dependencies

Install all project dependencies, including development tools:

```bash
uv sync --all-extras
```

This command will:
- Create or update the virtual environment
- Install all dependencies from `pyproject.toml`
- Install optional dependencies (llama-index-rag, llama-stack, smolagents, mellea)
- Install development dependencies (pytest, mypy, ruff, pre-commit)
- Install example dependencies (Jupyter notebooks)

**Install only core dependencies:**

```bash
uv sync
```

**Install specific optional dependencies:**

```bash
# For LlamaIndex RAG functionality
uv sync --extra llama-index-rag

# For Llama Stack integration
uv sync --extra llama-stack

# For Smolagents support
uv sync --extra smolagents
```

### 5. Apple Silicon Development Setup

If you're developing on Apple Silicon (M1, M2, M3 chips), you can install additional optimizations using the MLX framework:

```bash
uv sync --group apple-dev
```

This installs:
- `mlx-vlm>=0.3.3` - Apple's MLX framework for vision-language models
- Optimized libraries for Apple Silicon performance

**Why use apple-dev group?**
- **Better Performance**: MLX is optimized for Apple Silicon's unified memory architecture
- **Lower Memory Usage**: More efficient memory management on M-series chips
- **Native Support**: Uses Apple's Metal framework for GPU acceleration
- **Faster Inference**: Optimized for on-device model inference

**Complete setup for Apple Silicon:**

```bash
# Install all dependencies including Apple-specific optimizations
uv sync --all-extras --group apple-dev
```

---

## Running the Development Server

After installing dependencies, you can run the Docling MCP server in development mode:

**Run app without uv:**
```bash
# Run with HTTP transport 
docling-mcp-server --transport streamable-http

# Show all available options
docling-mcp-server --help

# Run with python module
python -m docling_mcp.servers.mcp_server --transport streamable-http
```

**Or using uv run (recommended):**
```bash
# Run with stdio transport (default, for Claude Desktop)
uv run docling-mcp-server
```

**Available tool groups:**
- `conversion` - Document conversion tools (PDF to DoclingDocument)
- `generation` - Document generation tools (create new documents)
- `manipulation` - Document manipulation tools (modify existing documents)
- `llama-index-rag` - RAG with LlamaIndex and Milvus
- `llama-stack-rag` - RAG with Llama Stack
- `llama-stack-ie` - Information extraction with Llama Stack

**Activating the virtual environment manually:**

If you prefer to activate the environment first:

```bash
# On macOS/Linux
source env/bin/activate

# On Windows
.\env\Scripts\activate

# Then run the server
docling-mcp-server
```

---

## Setting Up MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a powerful tool for testing and debugging MCP servers. It provides a web UI to inspect tools, call them, and see responses.

### Local Installation

**Install MCP Inspector globally using npx (Node.js required):**

```bash
# This will download and run the inspector without permanent installation
npx @modelcontextprotocol/inspector
```

**Or install it permanently:**

```bash
npm install -g @modelcontextprotocol/inspector

# Then run it
mcp-inspector
```

### Docker Installation

If you prefer a containerized setup, use Docker Compose:

```bash
# Build and start the inspector
docker-compose up mcp-inspector

# Or run in detached mode
docker-compose up -d mcp-inspector

# View logs to get the authentication token
docker-compose logs mcp-inspector
```

The inspector will be available at:
- **Web UI**: http://localhost:6274
- **Proxy Server**: http://localhost:6277

### Using MCP Inspector

**1. Start your Docling MCP server:**

```bash
# In one terminal, run the server with HTTP transport
uv run docling-mcp-server --transport streamable-http --host localhost --port 8000
```

**2. Start MCP Inspector:**

```bash
# In another terminal
npx @modelcontextprotocol/inspector
```

**3. Connect to your server:**

Open your browser to http://localhost:6274 and configure:

- **Server URL**: `http://localhost:8000/mcp`
- **Transport Type**: `streamable-http`
- **Authentication**: If using Docker, copy the session token from logs

**4. Test your tools:**

Once connected, you can:
- Browse all available tools
- View tool schemas and descriptions
- Call tools with test inputs
- Inspect responses and errors
- Debug tool behavior

**Example workflow:**

1. Select the `convert_document_into_docling_document` tool
2. Provide a `source` parameter (local file path or URL)
3. Click "Call Tool"
4. Inspect the returned `document_key`
5. Use the key with other tools like `export_docling_document_to_markdown`

---

## Working with Files in Docker Container

When developing locally with Docker and using the `convert_document_into_docling_document` tool, you may need to copy files into the running container to process them.

### Adding Files to Docker Container

To copy a file from your local filesystem into the Docker container:

```bash
docker cp "/path/to/your/file.pdf" docling-mcp-server:/app/
```

**Example:**
```bash
docker cp "/Users/username/Documents/sample.pdf" docling-mcp-server:/app/
```

This copies the file to the `/app/` directory inside the container.

### File Paths Inside Docker

Once copied, files are accessible using their absolute path inside the container:

```
/app/filename.ext
```

**Example:**
- Local file: `/Users/username/Documents/sample.pdf`
- After copying: `/app/sample.pdf`
- Use in tool: `convert_document_into_docling_document` with `source="/app/sample.pdf"`

**Note:** This is particularly useful during local development when testing document processing with the `convert_document_into_docling_document` tool, as it requires file paths that exist within the container's filesystem.

---

## Project Structure

Understanding the project structure helps you navigate and contribute effectively:

```
docling-mcp/
├── docling_mcp/           # Main package directory
│   ├── __init__.py
│   ├── docling_cache.py   # Document caching system
│   ├── logger.py          # Logging configuration
│   ├── shared.py          # Shared state and utilities
│   ├── servers/           # MCP server implementation
│   │   ├── mcp_server.py  # Main server entry point
│   │   └── __init__.py
│   ├── settings/          # Configuration modules
│   │   ├── conversion.py  # Conversion settings
│   │   ├── llama_index.py # LlamaIndex settings
│   │   ├── llama_stack.py # Llama Stack settings
│   │   └── __init__.py
│   └── tools/             # MCP tools implementation
│       ├── conversion.py  # Document conversion tools
│       ├── generation.py  # Document generation tools
│       ├── manipulation.py # Document manipulation tools
│       ├── llama_index/   # LlamaIndex RAG tools
│       └── llama_stack/   # Llama Stack tools
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest configuration
│   ├── test_conversion_tools.py
│   ├── test_generation_tools.py
│   └── test_document_manipulation.py
├── examples/              # Usage examples
│   ├── llama-index/       # LlamaIndex examples
│   ├── llama-stack/       # Llama Stack examples
│   └── smolagents/        # Smolagents examples
├── docs/                  # Documentation
│   ├── integrations/      # Integration guides
│   └── applications/      # Application examples
├── pyproject.toml         # Project configuration
├── docker-compose.yml     # Docker services
├── Dockerfile             # Main server image
├── Dockerfile.inspector   # MCP Inspector image
└── README.md              # User documentation
```

**Key files:**

- **`pyproject.toml`**: Defines dependencies, build configuration, and tool settings
- **`docling_mcp/servers/mcp_server.py`**: Server entry point and CLI
- **`docling_mcp/tools/*.py`**: Tool implementations using FastMCP
- **`docling_mcp/shared.py`**: Shared MCP instance and caches
- **`tests/conftest.py`**: Test fixtures and utilities

---

## Development Workflow

### Adding a New Dependency

Use `uv add` to add new dependencies:

```bash
# Add a regular dependency
uv add requests

# Add a development dependency
uv add --dev pytest-mock

# Add an optional dependency
uv add --optional llama-index-core
```

This updates both `pyproject.toml` and `uv.lock`.

### Creating a New Tool

1. **Create a new tool module** (or add to an existing one):

```python
# docling_mcp/tools/my_tools.py
from typing import Annotated
from pydantic import Field
from dataclasses import dataclass
from mcp.types import ToolAnnotations

from docling_mcp.shared import mcp

@dataclass
class MyToolOutput:
    """Output of my_tool."""
    result: Annotated[str, Field(description="The result")]

@mcp.tool(
    title="My Custom Tool",
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
def my_tool(
    input_param: Annotated[str, Field(description="Input parameter")],
) -> MyToolOutput:
    """My custom tool description."""
    # Tool implementation
    return MyToolOutput(result=f"Processed: {input_param}")
```

2. **Register in the server** (`docling_mcp/servers/mcp_server.py`):

```python
# Add to ToolGroups enum
class ToolGroups(str, enum.Enum):
    MY_TOOLS = "my-tools"

# Add to main() function
if ToolGroups.MY_TOOLS in tools:
    logger.info("loading my custom tools...")
    import docling_mcp.tools.my_tools
```

3. **Write tests** (`tests/test_my_tools.py`):

```python
import pytest

@pytest.mark.asyncio
async def test_my_tool(mcp_client):
    response = await mcp_client.call_tool(
        "my_tool",
        {"input_param": "test"}
    )
    assert response.content[0].text == '{"result": "Processed: test"}'
```

---

## Code Style and Quality

We enforce code quality using automated tools:

### Pre-commit Hooks

Install pre-commit hooks to automatically check code before commits:

```bash
uv run pre-commit install
```

This will run checks on every commit. To run manually:

```bash
# Run on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run ruff --all-files
uv run pre-commit run mypy --all-files
```

### Ruff (Linting and Formatting)

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and code formatting:

```bash
# Check for linting issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without modifying
uv run ruff format --check .
```

