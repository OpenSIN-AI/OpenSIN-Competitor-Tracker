# OpenSIN Competitor Tracker

Automated competitor research and tracking for all AI coding agents.

## Competitors Tracked: 50+

See `all-competitors.json` for full list.

## Comprehensive Scanning System

### n8n Workflow

Import `workflows/competitor-scanner-master.json` into your n8n instance. The workflow provides:

- **4 Schedule Triggers** based on priority:
  - CRITICAL: every 6 hours (Cursor 3, Claude Code, Codex, Antigravity, Copilot, Roo Code)
  - HIGH: every 12 hours (Windsurf, OpenCode, Aider, Kilo Code, Continue, Devin, Augment, Morph, Jules, Replit, Bolt.new, MetaGPT, AutoGen, CrewAI, LangGraph, Google A2A)
  - MEDIUM: daily at 6AM (Tabnine, Amazon Q, DeepSeek, Cody, Pieces, CodeRabbit, SWE-agent, OpenHands, Devika, GPT Engineer, AutoDev, ChatDev, CAMEL, AutoGPT, Lovable, v0, Junie)
  - LOW: weekly on Monday (Bito, MutableAI, Grit, Sweep, Bloop, Mintlify, Codeium, PearAI)

- **GitHub API Scanning**: commits, releases, PRs, issues, star counts
- **Web Scraping**: changelogs, blogs, announcement pages
- **Change Detection**: compares with previous scan results
- **Notifications**: Telegram and Discord with formatted messages
- **Manual Trigger**: POST to `/webhook/competitor-scan` with optional `priority` or `category` filter

### Python Scanner

Run standalone or integrate with n8n via webhook:

```bash
# Scan all competitors
python3 scanner.py

# Scan by priority
python3 scanner.py --priority=CRITICAL

# Scan by category
python3 scanner.py --category="AI Coding Agents (IDE/CLI)"
```

### Webhook Handler

Start the Flask webhook server for n8n integration:

```bash
pip install flask requests
python3 webhook-handler.py
```

Endpoints:
- `POST /scan` - Trigger a scan (optional: `priority`, `category`)
- `GET /report` - Get latest scan results
- `GET /health` - Health check

## Competitor Categories

### AI Coding Agents (IDE/CLI) - 25 competitors
Cursor 3, Claude Code, OpenAI Codex, Google Antigravity, GitHub Copilot, Windsurf, OpenCode, Aider, Kilo Code, Continue, Tabnine, Amazon Q Developer, Replit Agent 4, Bolt.new, Devin, Augment Code, Morph, Google Jules, DeepSeek Coder, Sourcegraph Cody, Bito AI, MutableAI, Pieces, CodeRabbit, Grit

### Autonomous Coding Agents - 10 competitors
Roo Code, Cline, SWE-agent, OpenHands, Devika, GPT Engineer, AutoDev, Magentic, AutoGPT, BabyAGI

### Multi-Agent Frameworks - 7 competitors
MetaGPT, ChatDev, CAMEL, AutoGen, CrewAI, LangGraph, Google A2A

### Pivoted/Adjacent - 8 competitors
Sweep, Bloop, Mintlify, Codeium, Lovable, Vercel v0, PearAI, JetBrains Junie

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

- `all-competitors.json` - Master competitor list (50+ competitors)
- `competitor-research-results.json` - Latest scan results
- `auto-research-daily.sh` - Daily research script
- `scanner.py` - Standalone Python scanner
- `webhook-handler.py` - Flask webhook server for n8n integration
- `workflows/competitor-scanner-master.json` - n8n workflow definition

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub API token for authenticated requests |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications |
| `TELEGRAM_API_ID` | n8n Telegram API credential ID |
| `DISCORD_CHANNEL_ID` | Discord channel ID for notifications |
| `DISCORD_WEBHOOK_ID` | n8n Discord webhook credential ID |

## Mandate

**Team Coder MUST analyze competitors and implement missing features.**
Research runs automatically based on priority schedule.
Issues are automatically created in all 8 team coder repos.

> OpenSIN connects to **100+ LLM providers** and **1000+ models** - including OpenAI, Anthropic, Google, Mistral, Groq, Cerebras, TogetherAI, Ollama, local models, and 90+ more. Bring your own API key or use our free tier.

## 📚 Documentation

This repository follows the [Global Dev Docs Standard](https://github.com/OpenSIN-AI/Global-Dev-Docs-Standard).

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).
For security policy, see [SECURITY.md](SECURITY.md).
For the complete OpenSIN ecosystem, see [OpenSIN-AI Organization](https://github.com/OpenSIN-AI).

## 🔗 See Also

- [OpenSIN Core](https://github.com/OpenSIN-AI/OpenSIN) — Main platform
- [OpenSIN-Code](https://github.com/OpenSIN-AI/OpenSIN-Code) — CLI
- [OpenSIN-backend](https://github.com/OpenSIN-AI/OpenSIN-backend) — Backend
- [OpenSIN-Infrastructure](https://github.com/OpenSIN-AI/OpenSIN-Infrastructure) — Deploy
- [Global Dev Docs Standard](https://github.com/OpenSIN-AI/Global-Dev-Docs-Standard) — Docs
