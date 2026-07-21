# GreenLedger — AI-Powered Tax Platform (Case Study Prototype)

A working prototype covering all 10 challenges from the case study brief, built as a
Flask app to mirror GreenGrowth's actual stack (Python/Flask/Postgres monolith,
Tailwind-style utility CSS, vanilla JS). Interactivity is handled with a small dose
of Alpine.js so the review screen genuinely works end-to-end without a JS build step.

## Running it

```bash
pip install -r requirements.txt
python3 app.py
```
Open `http://localhost:5050`. You'll land on a role picker — pick any of the six
demo accounts to see the product from that seat.

## How the 10 challenges map to the build

| # | Challenge | Where to look |
|---|---|---|
| 01 | Source Document Traceability | `/returns/R-2025-001/review` — click any return field to see it thread back to a source document, page, and the exact transformation applied |
| 02 | Client & CPA Collaboration | `/returns/R-2025-001/messages` — internal-vs-client-visible threads, messages linked to specific documents, an outstanding-request tracker |
| 03 | Where to Start | log in as **Jordan Lee** — day-one onboarding, single next action, nav intentionally hides tabs with nothing in them yet |
| 04 | Getting Lost in the App | breadcrumbs on every page; a message links directly to the document it's about; return tabs (Overview/Review/Documents/Messages) persist context as you move between them |
| 05 | Role-Aware Experiences | the account switcher in the top bar — try **Priya Nair (staff)**, who has both a preparer login and her own personal return, to see the multi-role case |
| 06 | Return Status & Progress | `/portal` (client view — one plain-language status) vs `/returns/R-2025-001` (staff view — full stage tracker) driven by the same underlying data |
| 07 | An Actionable Dashboard | `/dashboard` — 54 mock tasks ranked by a real (if simple) urgency function, filterable, blocked items surfaced inline |
| 08 | Clickable vs. Editable | the field affordance system (legend at the top of the Review screen) — editable / AI-generated / needs-review / verified / locked, reused consistently across screens |
| 09 | Complexity Made Navigable | `/returns/R-2025-001/documents` — 180 generated mock documents, real search + category filtering |
| 10 | Trustworthy AI | AI insight cards at the top of the Review screen (confidence score, "why the AI flagged this," suggested action, accept/dismiss) plus the per-field confidence + evidence panel |

## What's real vs. simulated

**Real and working:**
- Flask routing, session-based role switching, server-side rendering
- The prioritization logic on the dashboard (sorts/filters real Python data structures by urgency)
- Search and category filtering on the document library (actual filtering against 180 mock records, not a static list)
- The `/api/ai/<field_id>` endpoint is a genuine Flask JSON endpoint the frontend calls via `fetch()` — the traceability panel is really client-server, just against fabricated data
- The affordance/status/badge system is one shared CSS component set reused across every screen, not per-screen one-offs

**Simulated / fabricated, as the brief invited:**
- All clients, returns, documents, messages, and dollar amounts are fake (seeded so numbers stay consistent on reload)
- No real OCR, document parsing, or LLM calls — extraction confidence scores and "why the AI flagged this" evidence are hardcoded per field
- No real database — data lives in `mock_data.py` in memory; a restart resets everything
- No real auth — the role switcher is a plain session-cookie swap, not a login system
- "Send" on the message composer and "Mark verified" / "Flag for correction" buttons are visually wired but don't persist (no backend write) — deliberately, since the brief asked for concept over infrastructure

## Decisions worth flagging

- **Chose Flask over a JS framework** to mirror GreenGrowth's actual monolith, since the JD specifically lists Python/Flask/Postgres/Tailwind/vanilla JS as the stack.
- **One shared design system, not ten separate UIs.** Since 6+ challenges are really the same underlying problem (how do you visually communicate trust, status, and ownership), I built one token/component set (badges, field states, stage tracker) once and reused it everywhere, rather than styling each challenge independently.
- **Status has two vocabularies on purpose** (challenge 06): staff see a 5-stage pipeline; clients see one plain-language line plus "is anything needed from me." Same underlying `current_stage` data, two presentations — this is the actual design answer to "statuses everyone interprets the same way," rather than one shared label.
