"""
All data in this file is fabricated for the case study.
Nothing here is a real client, document, or figure.
"""
import random
from datetime import datetime, timedelta

random.seed(42)
TODAY = datetime(2026, 7, 18)

# ---------------------------------------------------------------------------
# USERS  (no real auth -- role is picked at /login and stored in the session)
# ---------------------------------------------------------------------------
USERS = {
    "sarah_chen":   {"name": "Sarah Chen",   "role": "client",    "initials": "SC", "context": "Individual - Return R-2025-001"},
    "jordan_lee":   {"name": "Jordan Lee",   "role": "client",    "initials": "JL", "context": "Individual - New client, Day 1"},
    "priya_nair":   {"name": "Priya Nair",   "role": "preparer",  "initials": "PN", "context": "Senior Preparer, 34 active returns"},
    "marcus_webb":  {"name": "Marcus Webb",  "role": "reviewer",  "initials": "MW", "context": "Reviewing Partner"},
    "dana_ortiz":   {"name": "Dana Ortiz",   "role": "admin",     "initials": "DO", "context": "Firm Administrator"},
    # demonstrates challenge 05's "employee who also has a personal return" case
    "priya_nair_personal": {"name": "Priya Nair", "role": "client", "initials": "PN", "context": "Personal Return R-2025-009 (staff)"},
}

ROLE_LABELS = {
    "client": "Client",
    "preparer": "Preparer",
    "reviewer": "Reviewer",
    "admin": "Firm Admin",
}

# ---------------------------------------------------------------------------
# RETURNS
# ---------------------------------------------------------------------------
RETURNS = {
    "R-2025-001": {
        "id": "R-2025-001", "client": "Sarah Chen", "client_key": "sarah_chen",
        "type": "Individual · Form 1040", "year": 2025,
        "status": "in_review", "preparer": "Priya Nair", "reviewer": "Marcus Webb",
        "next_action_owner": "preparer",
        "stages": ["intake", "prep", "review", "client_signoff", "filed"],
        "current_stage": "review",
        "blocking": None,
        "due_date": TODAY + timedelta(days=6),
    },
    "R-2025-002": {
        "id": "R-2025-002", "client": "Miller Bros LLC", "client_key": None,
        "type": "Business · Form 1120-S", "year": 2025,
        "status": "awaiting_client", "preparer": "Priya Nair", "reviewer": "Marcus Webb",
        "next_action_owner": "client",
        "stages": ["intake", "prep", "review", "client_signoff", "filed"],
        "current_stage": "prep",
        "blocking": "Missing K-1 allocation confirmation from client",
        "due_date": TODAY + timedelta(days=2),
    },
    "R-2025-003": {
        "id": "R-2025-003", "client": "David Okafor", "client_key": None,
        "type": "Individual · Form 1040", "year": 2025,
        "status": "ready_to_file", "preparer": "Priya Nair", "reviewer": "Marcus Webb",
        "next_action_owner": "reviewer",
        "stages": ["intake", "prep", "review", "client_signoff", "filed"],
        "current_stage": "client_signoff",
        "blocking": None,
        "due_date": TODAY + timedelta(days=1),
    },
    "R-2025-004": {
        "id": "R-2025-004", "client": "Jordan Lee", "client_key": "jordan_lee",
        "type": "Individual · Form 1040", "year": 2025,
        "status": "getting_started", "preparer": "Priya Nair", "reviewer": None,
        "next_action_owner": "client",
        "stages": ["intake", "prep", "review", "client_signoff", "filed"],
        "current_stage": "intake",
        "blocking": None,
        "due_date": TODAY + timedelta(days=30),
    },
    "R-2025-009": {
        "id": "R-2025-009", "client": "Priya Nair", "client_key": "priya_nair_personal",
        "type": "Individual · Form 1040", "year": 2025,
        "status": "in_review", "preparer": "Marcus Webb", "reviewer": "Dana Ortiz",
        "next_action_owner": "preparer",
        "stages": ["intake", "prep", "review", "client_signoff", "filed"],
        "current_stage": "prep",
        "blocking": None,
        "due_date": TODAY + timedelta(days=14),
    },
}

STATUS_META = {
    "getting_started":  {"label": "Getting Started",      "client_label": "Let's get started",              "color": "slate"},
    "in_review":        {"label": "In Review",             "client_label": "Your preparer is reviewing this", "color": "amber"},
    "awaiting_client":  {"label": "Awaiting Client",        "client_label": "We need something from you",     "color": "red"},
    "ready_to_file":     {"label": "Ready to File",         "client_label": "Ready for your signature",       "color": "teal"},
    "filed":             {"label": "Filed",                 "client_label": "Filed - you're all set",         "color": "green"},
}

STAGE_LABELS = {
    "intake": "Intake", "prep": "Preparation", "review": "Review",
    "client_signoff": "Client Sign-off", "filed": "Filed",
}

# ---------------------------------------------------------------------------
# TRACEABILITY  -- challenge 01. Real line items with fabricated source links.
# ---------------------------------------------------------------------------
TRACE_FIELDS = [
    {
        "id": "f1", "return_id": "R-2025-001", "line": "Line 1a - Wages, salaries, tips",
        "value": "$84,200.00", "state": "verified",
        "source_doc": "W-2 - Acme Robotics Inc.", "source_page": "Page 1 of 1",
        "source_box": "Box 1 - Wages, tips, other comp.",
        "transformation": "Direct copy, no adjustment applied.",
        "confidence": 99, "extracted_snippet": "Box 1: 84,200.00",
    },
    {
        "id": "f2", "return_id": "R-2025-001", "line": "Line 2b - Taxable interest",
        "value": "$412.00", "state": "ai_generated",
        "source_doc": "1099-INT - Chase Bank", "source_page": "Page 1 of 1",
        "source_box": "Box 1 - Interest income",
        "transformation": "Direct copy, no adjustment applied.",
        "confidence": 96, "extracted_snippet": "Box 1: 412.00",
    },
    {
        "id": "f3", "return_id": "R-2025-001", "line": "Line 3a - Qualified dividends",
        "value": "$1,180.00", "state": "ai_generated",
        "source_doc": "1099-DIV - Fidelity Investments", "source_page": "Page 1 of 2",
        "source_box": "Box 1b - Qualified dividends",
        "transformation": "Direct copy, no adjustment applied.",
        "confidence": 94, "extracted_snippet": "Box 1b: 1,180.00",
    },
    {
        "id": "f4", "return_id": "R-2025-001", "line": "Schedule C - Gross receipts",
        "value": "$18,650.00", "state": "needs_review",
        "source_doc": "Freelance income log.xlsx (client upload)", "source_page": "Rows 1-42",
        "source_box": "Column: Amount Received",
        "transformation": "Summed 42 transactions from client-uploaded spreadsheet. Three rows flagged as possible duplicates and excluded.",
        "confidence": 71, "extracted_snippet": "SUM(B2:B44) minus 3 flagged duplicate rows",
    },
    {
        "id": "f5", "return_id": "R-2025-001", "line": "Schedule A - Mortgage interest",
        "value": "$9,340.00", "state": "verified",
        "source_doc": "Form 1098 - Wells Fargo Home Mortgage", "source_page": "Page 1 of 1",
        "source_box": "Box 1 - Mortgage interest received",
        "transformation": "Direct copy, no adjustment applied. Verified by Priya Nair on Jul 12.",
        "confidence": 99, "extracted_snippet": "Box 1: 9,340.00",
    },
    {
        "id": "f6", "return_id": "R-2025-001", "line": "Line 25a - Federal tax withheld",
        "value": "$11,088.00", "state": "locked",
        "source_doc": "W-2 - Acme Robotics Inc.", "source_page": "Page 1 of 1",
        "source_box": "Box 2 - Federal income tax withheld",
        "transformation": "Direct copy. Locked after reviewer sign-off on Jul 14.",
        "confidence": 99, "extracted_snippet": "Box 2: 11,088.00",
    },
]

# ---------------------------------------------------------------------------
# DOCUMENT LIBRARY  -- challenge 09 (scale) + challenge 04 (linking)
# ---------------------------------------------------------------------------
DOC_CATEGORIES = ["W-2", "1099-INT", "1099-DIV", "1099-NEC", "1098", "K-1",
                   "Receipt", "Bank Statement", "Prior Year Return", "Correspondence"]
CLIENTS_FOR_DOCS = ["Sarah Chen", "Miller Bros LLC", "David Okafor", "Jordan Lee", "Priya Nair"]

def _gen_documents(n=180):
    docs = []
    for i in range(1, n + 1):
        cat = random.choice(DOC_CATEGORIES)
        client = random.choice(CLIENTS_FOR_DOCS)
        days_ago = random.randint(0, 120)
        docs.append({
            "id": f"DOC-{1000+i}",
            "name": f"{cat} - {client.split()[0]}{'' if cat in ('Receipt','Bank Statement','Correspondence') else ''} #{i}",
            "category": cat,
            "client": client,
            "uploaded": (TODAY - timedelta(days=days_ago)).strftime("%b %d, %Y"),
            "pages": random.randint(1, 4),
            "linked_task": random.choice([True, False, False]),
            "status": random.choice(["Processed", "Processed", "Processed", "Needs Review", "Flagged"]),
        })
    return docs

DOCUMENTS = _gen_documents(180)

# ---------------------------------------------------------------------------
# TASKS  -- challenge 07 (actionable dashboard, needs volume + real prioritization)
# ---------------------------------------------------------------------------
TASK_TYPES = ["Review flagged deduction", "Confirm client-uploaded document", "Chase missing 1099",
              "Approve AI-extracted values", "Client signature needed", "Resolve K-1 discrepancy",
              "Second-review checklist", "Reply to client question"]

def _gen_tasks(n=54):
    tasks = []
    for i in range(1, n + 1):
        due_in = random.randint(-2, 10)
        urgency = "overdue" if due_in < 0 else ("urgent" if due_in <= 1 else ("soon" if due_in <= 4 else "later"))
        tasks.append({
            "id": f"T-{500+i}",
            "title": random.choice(TASK_TYPES),
            "return_id": random.choice(list(RETURNS.keys())),
            "client": random.choice(CLIENTS_FOR_DOCS),
            "owner": random.choice(["Priya Nair", "Marcus Webb", "You"]),
            "due_in_days": due_in,
            "urgency": urgency,
            "blocked": random.random() < 0.15,
        })
    urgency_rank = {"overdue": 0, "urgent": 1, "soon": 2, "later": 3}
    tasks.sort(key=lambda t: (urgency_rank[t["urgency"]], t["due_in_days"]))
    return tasks

TASKS = _gen_tasks(54)

# ---------------------------------------------------------------------------
# MESSAGES  -- challenge 02 (collaboration, internal vs client-visible)
# ---------------------------------------------------------------------------
MESSAGES = {
    "R-2025-001": [
        {"id": "m1", "author": "Priya Nair", "role": "preparer", "visibility": "client",
         "linked_doc": "Freelance income log.xlsx", "time": "Jul 10, 2:14 PM",
         "text": "I found 3 rows in your freelance log that look like duplicate entries (same amount, same day). Can you confirm before I finalize Schedule C?"},
        {"id": "m2", "author": "Sarah Chen", "role": "client", "visibility": "client",
         "linked_doc": "Freelance income log.xlsx", "time": "Jul 10, 6:02 PM",
         "text": "Good catch - those were re-uploads from a spreadsheet sync error. Please exclude them."},
        {"id": "m3", "author": "Priya Nair", "role": "preparer", "visibility": "internal",
         "linked_doc": "Freelance income log.xlsx", "time": "Jul 10, 6:05 PM",
         "text": "Client confirmed duplicates - excluding rows 12, 27, 39 from Schedule C total. Marking field for reviewer sign-off."},
        {"id": "m4", "author": "Marcus Webb", "role": "reviewer", "visibility": "internal",
         "linked_doc": None, "time": "Jul 12, 9:40 AM",
         "text": "Mortgage interest and W-2 fields verified against source docs. Good to move to client sign-off once Schedule C is closed out."},
    ],
    "R-2025-002": [
        {"id": "m5", "author": "Priya Nair", "role": "preparer", "visibility": "client",
         "linked_doc": "K-1 - Miller Bros LLC", "time": "Jul 15, 11:00 AM",
         "text": "We need written confirmation of each partner's ownership percentage before we can finalize the K-1 allocations. This is currently blocking the return."},
    ],
}

# ---------------------------------------------------------------------------
# AI OUTPUTS  -- challenge 10 (trustworthy AI). Served via a fake JSON endpoint.
# ---------------------------------------------------------------------------
AI_INSIGHTS = {
    "R-2025-001": [
        {
            "id": "ai1", "type": "recommendation", "severity": "medium",
            "title": "Possible missing 1099-NEC",
            "body": "Last year's return included a 1099-NEC from 'Bluepeak Consulting' for $3,200. No matching document has been uploaded this year.",
            "confidence": 68,
            "evidence": ["2024 return, Schedule C, payer 'Bluepeak Consulting'", "No 2025 document tagged to this payer"],
            "action": "Ask the client whether this income continued in 2025.",
        },
        {
            "id": "ai2", "type": "extraction_flag", "severity": "low",
            "title": "Duplicate rows detected in freelance income log",
            "body": "3 of 45 rows in the uploaded spreadsheet appear to be duplicates based on matching date and amount.",
            "confidence": 82,
            "evidence": ["Row 12 = Row 13 (date + amount)", "Row 27 = Row 28", "Row 39 = Row 40"],
            "action": "Confirm with client and exclude if duplicates.",
        },
    ]
}
