# Competitive Analysis Automation Script
$searches = @(
    "AI agent workflow",
    "epic story task workflow",
    "copilot instructions workflow",
    "github issue template workflow automation",
    "project management github actions",
    "sdlc software development lifecycle",
    "github project workflow automation",
    "role-based development workflow",
    "definition of ready definition of done",
    "multi-agent orchestration github"
)
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$analysisDir = "project_scope\results\$timestamp"
New-Item -ItemType Directory -Force -Path $analysisDir | Out-Null
Write-Host "`nCompetitive Analysis - Running $($searches.Count) searches..." -ForegroundColor Cyan
Write-Host "Results: $analysisDir`n" -ForegroundColor Yellow
$index = 1; $totalResults = 0
foreach ($query in $searches) {
    $filename = $query -replace '\s+', '_' -replace '[^\w-]', ''
    $outputPath = "$analysisDir\search_$filename.json"
    Write-Host "[$index/$($searches.Count)] $query" -ForegroundColor White
    try {
        gh search repos $query --limit 30 --sort stars --json name,owner,description,url,stargazersCount,language | Out-File -FilePath $outputPath -Encoding utf8
        $content = Get-Content $outputPath | ConvertFrom-Json
        $count = $content.Count; $totalResults += $count
        if ($count -eq 0) { Write-Host "  No results" -ForegroundColor Yellow }
        else { Write-Host "  Found $count results" -ForegroundColor Green }
    } catch { Write-Host "  Error: $_" -ForegroundColor Red }
    $index++; Start-Sleep -Milliseconds 500
}
Write-Host "`nComplete! Total: $totalResults projects" -ForegroundColor Green
Write-Host "Open folder: explorer $analysisDir" -ForegroundColor Cyan
