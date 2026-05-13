$ErrorActionPreference = "Stop"

Write-Host "--- Running Python Tests ---"
cd d:\MCP\cognitive-continuity-layer\memory-engine-py
.\venv\Scripts\Activate.ps1
pytest
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python tests failed!"
    exit 1
}

Write-Host "--- Starting Python Server for E2E ---"
$serverProcess = Start-Process -NoNewWindow -FilePath ".\venv\Scripts\uvicorn.exe" -ArgumentList "app.main:app", "--port", "8001" -PassThru
Start-Sleep -Seconds 3

Write-Host "--- Running TypeScript Build and Tests ---"
cd d:\MCP\cognitive-continuity-layer\mcp-server-ts
npm run build
if ($LASTEXITCODE -ne 0) {
    Stop-Process -Id $serverProcess.Id
    Write-Host "TypeScript build failed!"
    exit 1
}

npm run test
if ($LASTEXITCODE -ne 0) {
    Stop-Process -Id $serverProcess.Id
    Write-Host "TypeScript tests failed!"
    exit 1
}

Write-Host "--- Validating E2E Communication ---"
# We can use curl/Invoke-RestMethod to do a quick sanity check that the server is alive
$health = Invoke-RestMethod -Uri "http://localhost:8001/health"
if ($health.status -ne "ok") {
    Stop-Process -Id $serverProcess.Id
    Write-Host "Server health check failed!"
    exit 1
}

# Run the typescript e2e test script
node -e "
const { MemoryEngineClient } = require('./dist/client.js');
const client = new MemoryEngineClient();

async function runE2E() {
    console.log('Sending save memory request via TS client...');
    const saveRes = await client.saveMemory({
        user_id: 'e2e_user',
        workspace_id: 'e2e_ws',
        type: 'task_context',
        title: 'E2E Validation',
        summary: 'Testing E2E',
        content: 'E2E works!',
        scope: 'private',
        status: 'approved'
    });
    console.log('Save response:', saveRes);
    
    if (saveRes.status !== 'saved') throw new Error('Save failed');
    console.log('E2E validation successful!');
}

runE2E().catch(err => {
    console.error(err);
    process.exit(1);
});
"
$e2eResult = $LASTEXITCODE

Write-Host "--- Stopping Python Server ---"
Stop-Process -Id $serverProcess.Id

if ($e2eResult -ne 0) {
    Write-Host "E2E validation failed!"
    exit 1
}

Write-Host "All validations passed successfully!"
