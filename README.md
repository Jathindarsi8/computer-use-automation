# Computer-Use Automation System

A production-grade computer-use automation system that lets an AI agent operate real web UIs, record successful flows as reusable capability artifacts, and replay them deterministically without the LLM in the loop.

Built for interface.ai take-home assignment.

---

## What This Does

1. Takes a natural language goal
2. Uses Gemini/Claude to operate a real browser UI
3. Records the successful flow as a typed JSON artifact
4. Replays the artifact deterministically without LLM
5. Escalates to human when stuck
6. Enforces safety guardrails throughout

---

## Project Structure

```
computer-use-automation/
├── agent/              # LLM discovery loop
├── artifacts/          # Capability schema and storage
├── replay/             # Deterministic replay engine
├── guardrails/         # Safety and allowlist enforcement
├── handoff/            # Human escalation mechanism
├── evidence/           # Screenshots and logs from runs
├── config.py           # Configuration and API keys
├── main.py             # Entry point
├── README.md           # This file
└── REPORT.md           # Design write-up
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Jathindarsi8/computer-use-automation
cd computer-use-automation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure API keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_key_here
ANTHROPIC_API_KEY=your_claude_key_here
TARGET_URL=https://demo.opencart.com
MAX_STEPS=20
```

---

## How To Run

### Run Discovery Agent

```bash
python main.py --goal "Add MacBook to cart and reach checkout" --target https://demo.opencart.com
```

### Replay Saved Artifact

```bash
python main.py --replay artifacts/add_item_to_cart_v1.json
```

---

## Evidence

All discovery run evidence is saved in `/evidence/`:
- Screenshots at each step
- Structured JSON logs
- Final capability artifact

---

## Tech Stack

- **Browser automation:** Playwright
- **Agent loop:** LangGraph
- **LLM:** Google Gemini (testing) + Anthropic Claude (final run)
- **Artifact storage:** Pydantic + JSON
- **Operator handoff:** FastAPI
- **Language:** Python 3.10+

---

## Design Write-up

See [REPORT.md](REPORT.md) for full architecture and design decisions.
