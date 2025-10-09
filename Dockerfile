FROM python:3.12-slim

# Install system dependencies (git is needed for git-based dependencies in uv.lock)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files (README.md is required for package build)
COPY pyproject.toml uv.lock README.md ./
COPY docling_mcp ./docling_mcp

# Install dependencies (excluding dev dependencies which contain mlx)
RUN uv sync --frozen --no-dev

# Expose the port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "docling-mcp-server", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]