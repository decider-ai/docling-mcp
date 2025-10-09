# Docker Compose Setup

This directory contains Docker Compose configuration for running the Docling MCP server along with the MCP Inspector.

## Quick Reference

**Start Services:**
```bash
docker-compose up -d
```

**Access Points:**
- Docling MCP Server: http://localhost:8000
- MCP Inspector UI: http://localhost:6274

**Connect Inspector to Server:**
- URL: `http://docling-mcp:8000/mcp`
- Transport: `streamable-http`
- **Authentication**: Use the proxy session token displayed in the `mcp-inspector` container logs

---

## Services

### 1. docling-mcp
The main Docling MCP server that provides document processing capabilities.
- **Port**: 8000
- **Endpoint**: http://localhost:8000

### 2. mcp-inspector
The Model Context Protocol Inspector for testing and debugging MCP servers.
- **Port**: 6274 (Web UI), 6277 (Proxy Server)
- **UI**: http://localhost:6274

## Quick Start

### Start all services
```bash
docker-compose up
```

### Start in detached mode (background)
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f docling-mcp
docker-compose logs -f mcp-inspector
```

### Stop all services
```bash
docker-compose down
```

### Rebuild and start
```bash
docker-compose up --build
```

### Stop and remove all containers, networks, and volumes
```bash
docker-compose down -v
```

## Usage

1. **Start the services**:
   ```bash
   docker-compose up -d
   ```

2. **Access the MCP Inspector**:
   - Open your browser and navigate to http://localhost:6274
   - Or use the pre-filled URL from the logs: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>`
   
3. **Connect to the Docling MCP Server**:
   - In the MCP Inspector UI, configure the connection:
     - **Server URL**: `http://docling-mcp:8000/mcp` (from within Docker network)
     - **OR from host**: `http://host.docker.internal:8000/mcp` (if the above doesn't work)
     - **Transport Type**: `streamable-http`
   - The session token is displayed in the mcp-inspector logs

4. **Access the Docling MCP server directly**:
   - The server is available at http://localhost:8000

## Network
Both services are connected via a Docker bridge network called `mcp-network`, allowing them to communicate with each other using service names as hostnames.
