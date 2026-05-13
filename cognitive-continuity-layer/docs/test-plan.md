# Test Plan & Validation

## 1. Testing Strategy
The Cognitive Continuity Layer uses a multi-layered testing strategy to ensure reliability across the Python/TypeScript bridge.

### Unit Testing
- **Python (`pytest`)**: Validates internal logic for friction calculation, signal extraction, and hybrid ranking.
- **TypeScript (`vitest`)**: Validates MCP tool schema parsing and backend communication.

### Integration Testing
- **E2E Validation (`validate_all.ps1`)**: A unified script that builds the TS project, starts the Python server, runs all tests, and performs a live API handshake.

---

## 2. Test Commands

### Python Tests
```powershell
cd memory-engine-py
.\venv\Scripts\Activate.ps1
pytest
```

### TypeScript Tests
```powershell
cd mcp-server-ts
npm test
```

### Build Check
```powershell
cd mcp-server-ts
npm run build
```

---

## 3. Expected Results

| Component | Target | Expected Result |
| :--- | :--- | :--- |
| `memory-engine-py` | `pytest` | All 32+ tests pass (Health, Schemas, Logic, Behavioral) |
| `mcp-server-ts` | `vitest` | All tests pass (Mocked fetch, Schema validation) |
| `mcp-server-ts` | `tsc` | Successful compilation to `dist/` |
| `Integration` | `validate_all.ps1` | Exit code 0, server starts, E2E ping succeeds |

---

## 4. Final Validation Results (Current State)
- **Python Tests**: PASSED (32 tests)
- **TypeScript Tests**: PASSED
- **TypeScript Build**: SUCCESSFUL
- **E2E Handshake**: SUCCESSFUL

---

## 5. Known Limitations
- **Offline Mode**: BM25 library was not installed due to connection limits; internal keyword-frequency fallback is active.
- **Auth**: User/Workspace IDs are trusted strings in this POC phase.
- **Chroma Hosting**: Uses local persistence; cloud-hosted Chroma required for production scaling.
