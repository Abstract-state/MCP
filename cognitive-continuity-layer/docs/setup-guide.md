# Post-Clone Setup Guide

If you have just cloned this repository, follow these steps to initialize the environment and get the Cognitive Continuity Layer running.

## 1. Environment Variables
The repository contains a `.env.example` file. Create a copy named `.env` in the root and in the respective project folders if needed.

```powershell
cp .env.example .env
```

## 2. Python Backend Setup (Memory Engine)
The Python backend manages the vector database and behavioral logic.

```powershell
# Navigate to the backend directory
cd memory-engine-py

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 3. TypeScript Frontend Setup (MCP Server)
The MCP server provides the interface for AI assistants.

```powershell
# Navigate to the MCP server directory
cd ../mcp-server-ts

# Install Node.js dependencies
npm install

# Build the project
npm run build
```

## 4. Initialization & Validation
The project includes a root-level script to automate the verification of the entire stack. This script will run Python tests, start the server, run TypeScript tests, and perform a live end-to-end handshake.

```powershell
# From the root directory
.\validate_all.ps1
```

## 5. MCP Configuration
Once the services are ready, you must register the MCP server in your IDE or Assistant configuration (e.g., `mcp.json`).

**Template Configuration:**
```json
{
  "mcpServers": {
    "cognitive_continuity_mcp": {
      "command": "node",
      "args": [
        "C:/ABSOLUTE/PATH/TO/mcp-server-ts/dist/index.js"
      ],
      "env": {
        "MEMORY_ENGINE_URL": "http://localhost:8001"
      }
    }
  }
}
```
*Note: Ensure the path to `index.js` is an absolute path on your system.*

## 6. Directory Structure Note
- `chroma_data/`: This directory will be created automatically upon the first run of the Memory Engine. It is excluded from Git to keep your local database private.
- `node_modules/` and `venv/`: These are local environment folders and must be recreated via the steps above after every fresh clone.
