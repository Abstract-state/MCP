# MCP Configuration Guide

This guide details how to install and configure the Cognitive Continuity Layer MCP Server alongside your existing MCP infrastructure (like HEX MCP servers) on Windows, suitable for IDEs like IntelliJ or tools like Copilot.

## Requirements
- Node.js (v18+)
- Python (3.12+)
- The Cognitive Continuity MVP repository

## 1. Startup Steps
Before the MCP server can process requests, the Python Memory Engine must be running in the background.

1. **Start the Python Memory Engine**:
   Open a PowerShell terminal and run:
   ```powershell
   cd <path_to_repo>\memory-engine-py
   .\venv\Scripts\Activate.ps1
   uvicorn app.main:app --port 8001
   ```

2. **Build the TypeScript MCP Server**:
   Ensure the TypeScript project is built:
   ```powershell
   cd <path_to_repo>\mcp-server-ts
   npm install
   npm run build
   ```

## 2. Configuration Entry
To add this MCP server to your Copilot, Cursor, or IntelliJ configuration, append the following entry to your `mcp.json` or equivalent configuration file. 

**Important:** This configuration safely runs alongside existing integrations. **Do not overwrite** any existing configurations like `hex_mcp_docs`, `hex_mcp_memory`, or `hex_mcp_task_state`.

```json
{
  "mcpServers": {
    "cognitive_continuity_mcp": {
      "command": "node",
      "args": [
        "C:/absolute/path/to/repo/mcp-server-ts/dist/index.js"
      ],
      "env": {
        "TRANSPORT": "stdio",
        "MEMORY_ENGINE_URL": "http://localhost:8001",
        "DEFAULT_USER_ID": "demo_user",
        "DEFAULT_WORKSPACE_ID": "corp_ws"
      }
    }
  }
}
```

*Note: Be sure to replace `C:/absolute/path/to/repo/` with the actual absolute path to your `cognitive-continuity-layer` checkout on your Windows filesystem.*

## 3. Tool Verification
Once configured and running, the MCP server will expose the following tools to the LLM automatically:

### Continuity & Context
- `memory.save`: Persist reusable context snippets.
- `memory.search`: Query existing memories semantically.
- `memory.suggest_related`: Retrieve relevant history for current prompt.
- `memory.apply_context_bundle`: Apply approved instructions.

### Behavioral Learning
- `episode.capture`: Log interaction turns to build episodic memory.
- `episode.analyze`: Calculate friction and distill knowledge from episodes.

### Prompt Intelligence
- `prompt.refine_preview`: Generate context-aware prompt enhancements.
- `prompt.refine_confirm`: Human-in-the-loop approval of refinements.

### Patterns & Profile
- `communication.learn`: Explicitly define phrase meanings.
- `communication.search`: Query communication style meanings.
- `profile.get`: Retrieve user-specific continuity profile.

