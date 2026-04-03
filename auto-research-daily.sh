#!/bin/bash
# ============================================================
# OpenSIN Auto-Research System
# Runs DAILY at 6:00 AM CET
# Searches GitHub for ALL competitors
# Creates issues in ALL team coder repos
# NEVER lets agents be idle
# ============================================================

RESEARCH_DATE=$(date +%Y-%m-%d)
ORG="OpenSIN-AI"
LOG_FILE="/tmp/auto-research-$RESEARCH_DATE.log"

echo "=== AUTO-RESEARCH START: $RESEARCH_DATE ===" | tee -a "$LOG_FILE"

# COMPETITOR LIST - from marketing strategy + GitHub research
COMPETITORS=(
  "OpenClaw/openclaw"
  "anomalyco/opencode"
  "anthropics/claude-code"
  "openai/codex"
  "getcursor/cursor"
  "continuedev/continue"
  "aider-ai/aider"
  "windsurf-ai/windsurf"
  "kilocode/kilo-code"
  "Qodo/qodo"
  "devin-ai/devin"
  "manus-ai/manus"
  "github/copilot"
  "amazon-q/amazon-q-developer"
  "tabnine/tabnine-vscode"
  "Exafunction/codeium"
  "sourcegraph/cody"
  "rooveterinaryinc/roo-cline"
  "stackblitz/bolt.new"
  "lovable-dev/lovable"
  "replit/replit-agent"
  "vercel/v0"
  "pearai/pearai"
  "jetbrains/junie"
  "sweep-ai/sweep"
  "microsoft/autogen"
  "crewAIInc/crewAI"
  "langchain-ai/langgraph"
  "google/a2a"
)

# TEAM CODER REPOS - ALL must have issues to work on
TEAM_CODER_REPOS=(
  "OpenSIN-Coding-CEO"
  "OpenSIN-Agent-Frontend"
  "OpenSIN-Agent-Backend"
  "OpenSIN-Designer"
  "OpenSIN-Repo-Sync"
  "OpenSIN-Issues"
  "OpenSIN-Tester"
  "OpenSIN-Opal"
)

echo "" | tee -a "$LOG_FILE"
echo "=== COMPETITOR ANALYSIS ===" | tee -a "$LOG_FILE"

# Research each competitor
TOP_COMPETITORS=""
for repo in "${COMPETITORS[@]}"; do
  info=$(gh api repos/$ORG/$repo 2>/dev/null || gh api repos/$repo 2>/dev/null)
  if [ -n "$info" ]; then
    stars=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stargazers_count',0))" 2>/dev/null)
    updated=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('updated_at','?')[:10])" 2>/dev/null)
    desc=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print((d.get('description') or '')[:100])" 2>/dev/null)
    lang=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('language') or '?')" 2>/dev/null)
    echo "  ⭐ $repo: $stars⭐ $lang $updated - $desc" | tee -a "$LOG_FILE"
    if [ -n "$stars" ] && [ "$stars" -gt 0 ] 2>/dev/null; then
      TOP_COMPETITORS="$TOP_COMPETITORS\n| $repo | $stars⭐ | $lang | $updated | $desc |"
    fi
  else
    echo "  ❌ $repo: NOT FOUND" | tee -a "$LOG_FILE"
  fi
done

echo "" | tee -a "$LOG_FILE"
echo "=== CREATING ISSUES FOR TEAM CODER ===" | tee -a "$LOG_FILE"

# Create issues in ALL team coder repos
for repo in "${TEAM_CODER_REPOS[@]}"; do
  echo "  Creating issue in $repo..." | tee -a "$LOG_FILE"
  
  # Check if repo has issues enabled
  has_issues=$(gh api repos/$ORG/$repo --jq '.has_issues' 2>/dev/null)
  if [ "$has_issues" != "true" ]; then
    echo "    Enabling issues..." | tee -a "$LOG_FILE"
    gh api -X PATCH repos/$ORG/$repo -f has_issues=true 2>/dev/null
  fi
  
  # Create the issue
  gh issue create --repo "$ORG/$repo" \
    --title "🔍 Auto-Research: Implement competitor features - $RESEARCH_DATE" \
    --body "## 🔍 Auto-Research: Competitor Feature Implementation

**GENERATED AUTOMATICALLY** by OpenSIN Auto-Research System.
**MANDATE: Work on this IMMEDIATELY. No idle agents allowed. 24/7.**

### Competitors to Analyze (Top 10 by Stars)

| Competitor | Stars | Language | Updated |
|-----------|-------|----------|---------|
$TOP_COMPETITORS

### Action Items
- [ ] Research top 5 competitors in detail
- [ ] Identify feature gaps vs our implementation
- [ ] Implement missing features from competitors
- [ ] Update documentation with our advantages
- [ ] Create blog posts about competitive advantages

### Sources
- Marketing Strategy: $ORG/OpenSIN-Marketing-Release-Strategie (58 blog posts)
- Competitor Tracker: $ORG/OpenSIN-Competitor-Tracker
- Auto-Research runs daily at 6AM CET

### MANDATE
**This issue MUST be worked on immediately.**
If completed, find the next competitor and implement their features.
NEVER be idle. ALWAYS be improving OpenSIN." 2>&1 | tee -a "$LOG_FILE"
  
  sleep 2
done

echo "" | tee -a "$LOG_FILE"
echo "=== AUTO-RESEARCH COMPLETE ===" | tee -a "$LOG_FILE"
echo "Issues created in ${#TEAM_CODER_REPOS[@]} repos" | tee -a "$LOG_FILE"
echo "Next run: Tomorrow at 6:00 AM CET" | tee -a "$LOG_FILE"
