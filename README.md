# OpenSIN Competitor Tracker

Automated competitor research and tracking for all AI coding agents.

## Competitors Tracked: 50+

See `all-competitors.json` for full list.

## Comprehensive Scanning System

### n8n Workflow (`workflows/competitor-scanner-master.json`)

A comprehensive n8n workflow that monitors 50+ competitors across GitHub and the web:

- **Schedule-based scanning** with priority tiers:
  - CRITICAL: Every 6 hours (Cursor 3, Claude Code, Codex, Antigravity, Copilot, Roo Code)
  - HIGH: Every 12 hours (Windsurf, OpenCode, Aider, Kilo Code, Continue, Replit, Bolt.new, Devin, Augment, Morph, Jules, Cline, OpenHands, MetaGPT, AutoGen, CrewAI, LangGraph, Google A2A)
  - MEDIUM: Daily (Tabnine, Amazon Q, DeepSeek, Cody, Pieces, CodeRabbit, SWE-agent, Devika, GPT Engineer, AutoDev, AutoGPT, ChatDev, CAMEL, Lovable, v0, Junie)
  - LOW: Weekly (Bito, MutableAI, Grit, Sweep, Bloop, Mintlify, Codeium, PearAI)

- **GitHub scanning**: Commits, releases, PRs, issues, stars, contributors
- **Web scanning**: Changelogs, blog posts, Twitter announcements
- **Notifications**: Telegram and Discord
- **Results**: Stored in `competitor-research-results.json`

### Python Scanner (`scanner.py`)

Standalone Python script that can be run independently or via n8n:

```bash
# Install dependencies
pip install requests

# Run scanner
GITHUB_TOKEN=your_token python scanner.py
```

Scans:
- GitHub commits, releases, PRs, issues
- Star milestone tracking (1K, 5K, 10K, 25K, 50K, 100K, 200K, 500K)
- Changelog change detection via content hashing
- Priority-based significance scoring

### Webhook Handler (`webhook-handler.py`)

Flask app for n8n webhook integration:

```bash
# Start webhook server
pip install flask
python webhook-handler.py

# Trigger scan via webhook
curl -X POST http://localhost:8080/scan -H "Content-Type: application/json" -d '{"priority": "CRITICAL"}'

# Get latest report
curl http://localhost:8080/report
```

## Auto-Research

Runs daily at 6AM CET via LaunchAgent `com.sin.competitor-research`.
Script: `auto-research-daily.sh`

## Top Competitors by Stars

| Rank | Competitor | Stars | Language |
|------|-----------|-------|----------|
| 1 | OpenClaw/openclaw | 347,216 | TypeScript |
| 2 | anomalyco/opencode | 136,564 | TypeScript |
| 3 | anthropics/claude-code | 108,029 | Shell |
| 4 | openai/codex | 72,945 | Rust |
| 5 | microsoft/autogen | 56,657 | Python |
| 6 | crewAIInc/crewAI | 47,954 | Python |
| 7 | aider-ai/aider | 42,771 | Python |
| 8 | getcursor/cursor | 32,564 | - |
| 9 | continuedev/continue | 32,273 | TypeScript |
| 10 | langchain-ai/langgraph | 28,353 | Python |

## Files

- `all-competitors.json` — Master competitor list (50+ competitors)
- `competitor-research-results.json` — Latest research results
- `auto-research-daily.sh` — Daily research script
- `scanner.py` — Standalone Python scanner
- `webhook-handler.py` — Flask webhook handler for n8n
- `workflows/competitor-scanner-master.json` — n8n workflow definition

## Competitor Categories

### AI Coding Agents (IDE/CLI)
Cursor 3, Claude Code, Codex, Antigravity, Copilot, Windsurf, OpenCode, Aider, Kilo Code, Continue, Tabnine, Amazon Q Developer, Replit Agent 4, Bolt.new, Devin, Augment Code, Morph, Jules, DeepSeek Coder, Cody, Bito AI, MutableAI, Pieces, CodeRabbit, Grit

### Autonomous Coding Agents
Roo Code, Cline, SWE-agent, OpenHands, Devika, GPT Engineer, AutoDev, Magentic, AutoGPT, BabyAGI

### Multi-Agent Frameworks
MetaGPT, ChatDev, CAMEL, AutoGen, CrewAI, LangGraph, Google A2A

### Pivoted/Adjacent
Sweep, Bloop, Mintlify, Codeium, Lovable, Vercel v0, PearAI, JetBrains Junie

## Mandate

**Team Coder MUST analyze competitors and implement missing features.**
Research runs automatically daily at 6AM CET.
Issues are automatically created in all 8 team coder repos.

> OpenSIN connects to **100+ LLM providers** and **1000+ models** — including OpenAI, Anthropic, Google, Mistral, Groq, Cerebras, TogetherAI, Ollama, local models, and 90+ more. Bring your own API key or use our free tier.
