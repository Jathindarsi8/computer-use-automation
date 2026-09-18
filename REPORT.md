# Design Report — Computer-Use Automation System

---

## 1. Architecture

The system is built around a three-phase pipeline:

**Phase 1 — Discovery (LLM-driven)**
An AI agent uses Gemini or Claude to observe a live browser, decide what action to take, execute it, and loop until the goal is complete. Built using LangGraph for agent orchestration and Playwright for browser control.

**Phase 2 — Artifact (Capability Recording)**
After a successful discovery run, the system saves a typed, versioned JSON artifact that captures every step, locator strategy, input parameters, output schema, and success checkpoint. This artifact is the reusable capability.

**Phase 3 — Replay (Deterministic Execution)**
Given a saved artifact and input parameters, the replay engine executes the flow without calling the LLM. It uses stable element targeting with fallback strategies and handles errors explicitly.

**Key trade-offs:**
- Chose Playwright over Selenium for better async support and more stable locators
- Chose LangGraph over raw loops for better state management and stuck detection
- Chose JSON artifacts over database for simplicity and human readability

---

## 2. Artifact Schema

The artifact schema is designed as a typed, versioned capability contract:

```json
{
  "capability_id": "add_item_to_cart_v1",
  "version": "1.0.0",
  "description": "Add specific item to cart and reach checkout",
  "target_url": "https://demo.opencart.com",
  "created_at": "2026-09-18T00:00:00",
  "input_schema": {
    "item_name": "string",
    "quantity": "integer"
  },
  "output_schema": {
    "cart_total": "string",
    "items_in_cart": "integer"
  },
  "steps": [...],
  "checkpoint": "cart_contains_item",
  "allowed_domains": ["demo.opencart.com"],
  "risky_actions": ["checkout", "payment"]
}
```

**Why this shape:**
- Versioned so multiple variants can coexist
- Typed inputs and outputs so calling agents know the contract
- Checkpoint condition separates success from failure explicitly
- Risky actions flagged so replay engine can require confirmation

---

## 3. Determinism and Error Handling

**How replay is deterministic:**
- Replay engine reads saved steps and executes them in order
- No LLM is called during replay
- Each step uses multiple locator strategies in priority order:
  1. data-testid attribute
  2. aria-label
  3. CSS selector
  4. XPath fallback
  5. Text content match

**Error taxonomy — three explicit categories:**

| Type | Example | Response |
|------|---------|----------|
| Business outcome | "item not found" | Return structured result — not a crash |
| Recoverable | Session timeout, slow load | Retry with wait — max 3 attempts |
| Hard failure | Element not found after all fallbacks | Stop and return detailed error report |

**Why this matters:**
Conflating business outcomes with failures is the most common design mistake. "No such member" is a legitimate answer the caller needs — not an exception.

---

## 4. Heterogeneity and Multi-Tenant

**Surface abstraction:**
The system separates the perception layer from the recorded flow:
- Web apps — Playwright DOM interaction
- Legacy web apps — accessibility tree + text matching
- Desktop apps — OS-level automation via pyautogui (design only)

The artifact schema stores semantic descriptions of targets, not raw CSS selectors, so the replay engine can adapt to minor UI drift.

**Multi-tenant reuse:**
- Base artifacts use parameterized patterns — /item/12345 becomes /item/:id
- Tenant-specific overrides stored as variant files alongside base artifact
- Version drift detected by comparing element fingerprints at replay time

**What was mocked:**
Desktop surface support and full multi-tenant variant management were designed but not implemented. The seam is clean — a SurfaceAdapter interface defines the contract.

---

## 5. Escalation and Handoff

**Stuck detection triggers:**
- Agent exceeds MAX_STEPS limit
- Same action attempted 3 times without state change
- Confidence score below threshold
- Risky/irreversible action encountered

**Handoff mechanism:**
1. Agent detects stuck state
2. System raises InterventionRequest with context — current goal, step, screenshot, reason
3. FastAPI operator endpoint receives request and exposes live session
4. Human operator takes control of same browser session
5. Human completes manual steps
6. Human signals resume via API endpoint
7. System records what human did and resumes

**What was mocked:**
Full real-time co-browsing operator console was mocked as a simple FastAPI endpoint. The control-transfer model and session handoff mechanism are real and well-reasoned.

---

## 6. Safety

**Allowlist enforcement:**
- Every action checked against configurable allowlist before execution
- Permitted domains — only demo.opencart.com
- Permitted actions — click, type, navigate, screenshot, scroll
- Blocked actions — payment, delete, submit_order

**Risky action handling:**
- Safe actions — execute immediately
- Risky actions — require explicit confirmation or escalate to human
- Irreversible actions — always escalate, never execute autonomously

**PII and secrets:**
- All logs run through redaction filter before writing
- Passwords, card numbers, tokens never persisted in artifacts or logs
- Credentials stored only in .env — never committed to repo

---

## 7. Cuts

**What was deliberately left out:**

| Cut | Reason | What to build next |
|-----|---------|-------------------|
| Desktop app support | Out of scope for one surface demo | Implement pyautogui adapter |
| Full operator console UI | Complex real-time co-browsing | Build React operator dashboard |
| Multi-tenant variant management | Needs more time | Build variant override system |
| Multi-run stability testing | Nice to have | Add flakiness reporting |
| Code generation from artifact | Stretch goal | Emit Playwright test files |

**If I had more time:**
Priority would be hardening the replay error taxonomy, building the real operator console, and implementing cross-tenant artifact canonicalization.
