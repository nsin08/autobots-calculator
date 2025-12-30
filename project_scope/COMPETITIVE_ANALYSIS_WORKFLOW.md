# Competitive Analysis Workflow

**Purpose:** Automated process to search GitHub for similar projects and generate competitive analysis report.

**When to use:** 
- Before major releases (to identify competitors)
- Quarterly reviews (to track emerging projects)
- When repositioning the project (to validate uniqueness)

**Duration:** ~15-20 minutes

---

## Prerequisites

- `gh` CLI installed and authenticated
- PowerShell (Windows) or Bash (Linux/Mac)
- Project directory: `project_scope/references/`

---

## Step 1: Prepare References Directory

```powershell
# Create references directory if not exists
New-Item -ItemType Directory -Force -Path "project_scope\references"
```

---

## Step 2: Define Search Queries

Create a list of search terms targeting:
- **Core concept keywords** (your main value proposition)
- **Technology stack** (languages, frameworks)
- **Domain-specific terms** (SDLC, workflow, lifecycle)
- **Competitor keywords** (known similar projects)

**Example queries for Autobots:**
1. "AI agent workflow"
2. "epic story task workflow"
3. "copilot instructions workflow"
4. "github issue template workflow automation"
5. "project management github actions"
6. "sdlc software development lifecycle"
7. "github project workflow automation"
8. "role-based development workflow"
9. "definition of ready definition of done"
10. "multi-agent orchestration github"

---

## Step 3: Execute GitHub Searches

Run each search query and save results to JSON:

```powershell
# Search 1: AI agent workflow
gh search repos "AI agent workflow" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_ai_agent_workflow.json" -Encoding utf8

# Search 2: Epic/Story/Task workflow
gh search repos "epic story task workflow" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_epic_story.json" -Encoding utf8

# Search 3: Copilot workflow
gh search repos "copilot instructions workflow" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_copilot_workflow.json" -Encoding utf8

# Search 4: Issue template automation
gh search repos "github issue template workflow automation" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_issue_templates.json" -Encoding utf8

# Search 5: Project management + GitHub Actions
gh search repos "project management github actions" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_project_mgmt.json" -Encoding utf8

# Search 6: SDLC
gh search repos "sdlc software development lifecycle" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_sdlc.json" -Encoding utf8

# Search 7: GitHub project workflow
gh search repos "github project workflow automation" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_github_workflow.json" -Encoding utf8

# Search 8: Role-based workflow
gh search repos "role-based development workflow" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_role_based.json" -Encoding utf8

# Search 9: DoR/DoD
gh search repos "definition of ready definition of done" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_dor_dod.json" -Encoding utf8

# Search 10: Multi-agent orchestration
gh search repos "multi-agent orchestration github" --limit 30 --sort stars `
  --json name,owner,description,url,stargazersCount,language `
  | Out-File -FilePath "project_scope\references\search_multi_agent.json" -Encoding utf8
```

---

## Step 4: Analyze Results

### 4.1 Read and Parse JSON Files

For each search result file:
1. Read the JSON content
2. Identify projects with >50 stars (significant traction)
3. Identify projects with 0-10 stars (emerging competitors)
4. Identify empty results (gaps in the market)

### 4.2 Categorize Projects

Group found projects into categories:
- **Direct Competitors:** Same problem space + similar approach
- **Adjacent Competitors:** Similar tech, different problem
- **Complementary Projects:** Could integrate with yours
- **Tangential:** Mentioned in search but not relevant

### 4.3 Score Similarity

For each direct/adjacent competitor, rate similarity (1-10):
- **Problem Space:** Are they solving the same problem?
- **Technology Stack:** Do they use similar tech?
- **Target Audience:** Are they targeting the same users?
- **Approach:** Do they use similar methodology?
- **Maturity:** How mature is their solution?

---

## Step 5: Generate Analysis Report

Create `project_scope/references/ANALYSIS.md` with this structure:

```markdown
# Competitive Analysis Report

**Date:** [Current Date]
**Analyst:** [Your Name or "Automated"]
**Search Queries:** [Number] queries executed

---

## Executive Summary

[2-3 sentences on key findings]

---

## Search Results Summary

### Query Results Table
| Query | Results Found | Stars Range | Empty? |
|-------|--------------|-------------|--------|
| AI agent workflow | 30 | 3 - 24,674 | No |
| epic story task | 0 | - | Yes |
| ... | ... | ... | ... |

---

## Close Candidates (Top 10)

### 1. [Project Name] ⭐ [Stars]
- **Description:** [One-line description]
- **Language:** [Primary language]
- **URL:** [GitHub URL]
- **Similarity Score:** [1-10] / 10
- **What they do:** [Key features]
- **Key Difference:** [How we differ]

[Repeat for top 10 projects]

---

## Market Gaps (Empty Search Results)

List all queries that returned 0 results. These represent gaps in the market.

1. ❌ [Query that returned 0 results]
2. ❌ [Another empty query]
...

---

## Unique Value Proposition

Based on this analysis, our project is unique because:

### What Exists Elsewhere
- [Feature/approach found in competitors]
- [Another common feature]

### What Doesn't Exist (Our Differentiators)
- ✅ [Our unique feature 1]
- ✅ [Our unique feature 2]
- ✅ [Our unique feature 3]

---

## Positioning Statement

[Your project] is a [category] that [key benefit].

Unlike [competitor approach], we [your approach].

We target [audience] who [pain point].

---

## Recommendations

1. **Positioning:** [How to position based on findings]
2. **Messaging:** [Key messages to emphasize]
3. **Features:** [Features to prioritize/add]
4. **Audience:** [Target audience refinement]
5. **GitHub Topics:** [Recommended topics to add]

---

## Monitoring Strategy

**Competitors to Watch:**
- [Competitor 1] - [Why watch them]
- [Competitor 2] - [Why watch them]

**Re-run Analysis:** Every [frequency, e.g., 3 months]

**Alert Triggers:** 
- New project with >100 stars in our space
- Existing competitor releases major version
- New GitHub topic trending in our domain

---

## Appendix: Raw Data

All search results saved to:
- `project_scope/references/search_*.json`
```

---

## Step 6: Create Summary for README (Optional)

Extract key differentiators and add to project README:

```markdown
## Why This Project is Unique

Unlike existing solutions:
- ❌ **Visual workflow builders** (sim, n8n) → We're GitHub-native
- ❌ **Generic agents** → We follow SDLC with quality gates
- ❌ **Enterprise tools** (JIRA, ADO) → We're lightweight and agent-ready

Our unique combination:
1. GitHub-native workflow engine
2. Role-based lifecycle (adaptable)
3. Strict quality gates (DoR/DoD)
4. AI agent orchestration ready
5. Working demo with full documentation
```

---

## Step 7: Schedule Next Analysis

Add reminder to re-run this workflow:
- **Quarterly:** Check for new competitors
- **Before major release:** Validate positioning
- **After significant GitHub ecosystem changes:** Reassess landscape

---

## Automation Script (Optional)

Create `project_scope/run_competitive_analysis.ps1`:

```powershell
# Competitive Analysis Automation Script
# Run this script to execute all searches and generate report skeleton

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

# Create references directory
New-Item -ItemType Directory -Force -Path "project_scope\references" | Out-Null

Write-Host "Starting competitive analysis..." -ForegroundColor Green
Write-Host "Running $($searches.Count) GitHub searches..." -ForegroundColor Yellow

$index = 1
foreach ($query in $searches) {
    $filename = $query -replace '\s+', '_' -replace '[^\w-]', ''
    $outputPath = "project_scope\references\search_$filename.json"
    
    Write-Host "[$index/$($searches.Count)] Searching: $query" -ForegroundColor Cyan
    
    gh search repos $query --limit 30 --sort stars `
        --json name,owner,description,url,stargazersCount,language `
        | Out-File -FilePath $outputPath -Encoding utf8
    
    $index++
    Start-Sleep -Milliseconds 500  # Rate limiting
}

Write-Host "✅ Search complete! Results saved to project_scope\references\" -ForegroundColor Green
Write-Host "📝 Next: Analyze results and create ANALYSIS.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run this to view results:"
Write-Host "  Get-ChildItem project_scope\references\search_*.json | ForEach-Object { Write-Host `$_.Name; Get-Content `$_ | ConvertFrom-Json | Measure-Object | Select-Object -ExpandProperty Count }" -ForegroundColor Gray
```

---

## Usage Example

**Quick run (PowerShell):**
```powershell
# Option 1: Run automation script
.\project_scope\run_competitive_analysis.ps1

# Option 2: Manual execution
# Follow Step 3 above
```

**Analyze results:**
```powershell
# Count results per search
Get-ChildItem project_scope\references\search_*.json | ForEach-Object {
    $results = Get-Content $_ | ConvertFrom-Json
    Write-Host "$($_.Name): $($results.Count) results"
}

# View top result from each search
Get-ChildItem project_scope\references\search_*.json | ForEach-Object {
    $results = Get-Content $_ | ConvertFrom-Json
    if ($results.Count -gt 0) {
        $top = $results | Sort-Object -Property stargazersCount -Descending | Select-Object -First 1
        Write-Host "`n$($_.Name):"
        Write-Host "  Top: $($top.name) ($($top.stargazersCount) stars)"
        Write-Host "  URL: $($top.url)"
    }
}
```

---

## Tips for Better Analysis

1. **Vary search terms:** Try synonyms, related concepts, and adjacent problems
2. **Check language-specific:** Add `language:Python`, `language:TypeScript` filters
3. **Time-based searches:** Use `created:>2024-01-01` to find recent projects
4. **Topic searches:** Use `topic:ai-agents`, `topic:workflow-automation`
5. **Explore forks/stars:** High-star projects may have interesting forks
6. **Check GitHub trending:** Visit https://github.com/trending regularly
7. **Monitor discussions:** Check GitHub Discussions in competitor repos

---

## Step 8: Head-to-Head Comparison (Optional)

After identifying close candidates (>50 stars or conceptually similar), perform detailed 1-1 comparisons.

### Comparison Framework

For each close candidate, create a structured comparison with:

**1. Project Profile** - Name, Stars, Last Activity, Tech Stack, URL  
**2. Feature Comparison Matrix** - Compare across 15-20 key dimensions  
**3. Detailed Analysis** - Architecture, workflow, integration approaches  
**4. Strengths & Weaknesses** - 5 each for your project and competitor  
**5. Use Case Decision Matrix** - When to choose each project  
**6. Differentiation Summary** - What makes your project unique  
**7. Learning Opportunities** - What to learn/avoid, collaboration potential  
**8. Verdict** - Direct competitor? Recommended action? Confidence level?

### Execution

```powershell
# Clone competitor for deep analysis (optional)
cd project_scope/references/competitors
gh repo clone <owner>/<repo>

# Review their documentation
Get-ChildItem -Recurse -Filter "*.md" | Select-String "workflow|agent|role"

# Check their issue templates
Get-ChildItem .github/ISSUE_TEMPLATE/

# Review their GitHub Actions
Get-ChildItem .github/workflows/

# Create comparison document
# Edit: project_scope/references/HEAD_TO_HEAD_COMPARISONS.md
```

**Output:** `project_scope/references/HEAD_TO_HEAD_COMPARISONS.md` with section per competitor

See HEAD_TO_HEAD_COMPARISONS.md for full comparison template and examples.

---

## Usage Example

From the root of your project:

```powershell
# Run the automation script
.\project_scope\run_competitive_analysis.ps1

# Output will be in: project_scope/results/YYYY-MM-DD_HHmmss/
# - search_*.json files (raw data)
# - ANALYSIS_SUMMARY.md (auto-generated)

# Or run searches manually
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
New-Item -ItemType Directory -Force -Path "project_scope\results\$timestamp"
cd "project_scope\results\$timestamp"
gh search repos "AI agent workflow" --limit 30 --sort stars --json name,owner,description,url,stargazersCount,language | Out-File -FilePath search_ai_agent_workflow.json -Encoding utf8

# Review results and create ANALYSIS.md in the timestamped directory
# Identify top 5 candidates and create HEAD_TO_HEAD_COMPARISONS.md
```

---

## Maintenance

Update this workflow when:
- Project pivot or new features added
- New competitors emerge (quarterly review)
- GitHub search API changes
- Team needs different analysis format
- Before major releases (v0.3.0, v1.0.0, etc.)

**Last Updated:** December 30, 2025  
**Version:** 1.1
