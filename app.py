from flask import Flask, render_template, session, redirect, request, jsonify
import mock_data as data

app = Flask(__name__)
app.secret_key = "case-study-demo-key-not-for-production"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def current_user():
    key = session.get("user_key", "priya_nair")
    return key, data.USERS[key]


def render(tpl, **kw):
    """Injects everything base.html needs on every page (role-aware shell)."""
    key, user = current_user()
    current_return = session.get("current_return", "R-2025-001")
    default_return = user.get("context", "")
    # figure out a sane "my return" for a client role
    client_return = None
    for rid, r in data.RETURNS.items():
        if r.get("client_key") == key:
            client_return = rid
            break
    return render_template(
        tpl,
        role=user["role"],
        role_label=data.ROLE_LABELS[user["role"]],
        role_labels=data.ROLE_LABELS,
        user=user,
        all_users=data.USERS,
        current_return=kw.pop("return_id", current_return),
        default_return=client_return or "R-2025-001",
        **kw,
    )


# ---------------------------------------------------------------------------
# auth / role switching  (challenge 05)
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    if "user_key" not in session:
        return redirect("/login")
    _, user = current_user()
    if user["role"] == "client":
        return redirect("/portal")
    return redirect("/dashboard")


@app.route("/login")
def login():
    return render_template("login.html", all_users=data.USERS, role_labels=data.ROLE_LABELS)


@app.route("/switch-role/<user_key>")
def switch_role(user_key):
    if user_key in data.USERS:
        session["user_key"] = user_key
        user = data.USERS[user_key]
        if user["role"] == "client":
            for rid, r in data.RETURNS.items():
                if r.get("client_key") == user_key:
                    session["current_return"] = rid
    dest = "/portal" if data.USERS[user_key]["role"] == "client" else "/dashboard"
    if user_key == "jordan_lee":
        dest = "/onboarding"
    return redirect(dest)


# ---------------------------------------------------------------------------
# challenge 03 -- first time / onboarding
# ---------------------------------------------------------------------------
@app.route("/onboarding")
def onboarding():
    ret = data.RETURNS["R-2025-004"]
    checklist = [
        {"label": "Verify your identity", "done": True},
        {"label": "Upload last year's tax return", "done": True},
        {"label": "Upload your W-2 and 1099s", "done": False},
        {"label": "Answer 6 quick questions about your year", "done": False},
        {"label": "Review and e-sign engagement letter", "done": False},
    ]
    return render("onboarding.html", active="portal", ret=ret, checklist=checklist,
                  return_id="R-2025-004")


# ---------------------------------------------------------------------------
# challenge 06 (simplified) -- client portal home / status
# ---------------------------------------------------------------------------
@app.route("/portal")
def portal():
    key, user = current_user()
    rid = None
    for r_id, r in data.RETURNS.items():
        if r.get("client_key") == key:
            rid = r_id
            break
    rid = rid or "R-2025-001"
    ret = data.RETURNS[rid]
    meta = data.STATUS_META[ret["status"]]
    return render("portal.html", active="portal", ret=ret, meta=meta,
                  stage_labels=data.STAGE_LABELS, return_id=rid)


# ---------------------------------------------------------------------------
# challenge 07 -- actionable dashboard (real filter/sort against mock data)
# ---------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    filt = request.args.get("filter", "all")
    tasks = data.TASKS
    if filt != "all":
        tasks = [t for t in tasks if t["urgency"] == filt]
    counts = {
        "overdue": len([t for t in data.TASKS if t["urgency"] == "overdue"]),
        "urgent": len([t for t in data.TASKS if t["urgency"] == "urgent"]),
        "soon": len([t for t in data.TASKS if t["urgency"] == "soon"]),
        "later": len([t for t in data.TASKS if t["urgency"] == "later"]),
    }
    returns_list = list(data.RETURNS.values())
    return render("dashboard.html", active="dashboard", tasks=tasks[:20], counts=counts,
                  filt=filt, returns=returns_list, status_meta=data.STATUS_META,
                  total_tasks=len(data.TASKS))


# ---------------------------------------------------------------------------
# return overview -- challenge 06 (status) entry point + tabs
# ---------------------------------------------------------------------------
@app.route("/returns/<rid>")
def return_overview(rid):
    session["current_return"] = rid
    ret = data.RETURNS[rid]
    meta = data.STATUS_META[ret["status"]]
    return render("return_detail.html", active="overview", ret=ret, meta=meta,
                  stage_labels=data.STAGE_LABELS, return_id=rid)


# ---------------------------------------------------------------------------
# challenge 01 + 08 + 10 -- review, traceability, affordances, AI trust
# ---------------------------------------------------------------------------
@app.route("/returns/<rid>/review")
def review(rid):
    session["current_return"] = rid
    ret = data.RETURNS[rid]
    fields = [f for f in data.TRACE_FIELDS if f["return_id"] == rid]
    insights = data.AI_INSIGHTS.get(rid, [])
    return render("review.html", active="review", ret=ret, fields=fields,
                  insights=insights, return_id=rid)


@app.route("/api/ai/<field_id>")
def api_ai(field_id):
    """Fake AI explanation endpoint -- a stub returning plausible JSON."""
    field = next((f for f in data.TRACE_FIELDS if f["id"] == field_id), None)
    if not field:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "field": field["line"],
        "value": field["value"],
        "confidence": field["confidence"],
        "source_doc": field["source_doc"],
        "source_box": field["source_box"],
        "transformation": field["transformation"],
        "extracted_snippet": field["extracted_snippet"],
    })


# ---------------------------------------------------------------------------
# challenge 09 -- document library at scale, search/filter/hierarchy
# challenge 04 -- context preserved via query params + breadcrumbs
# ---------------------------------------------------------------------------
@app.route("/returns/<rid>/documents")
def documents(rid):
    session["current_return"] = rid
    ret = data.RETURNS[rid]
    q = request.args.get("q", "").strip().lower()
    cat = request.args.get("cat", "all")
    docs = data.DOCUMENTS
    if cat != "all":
        docs = [d for d in docs if d["category"] == cat]
    if q:
        docs = [d for d in docs if q in d["name"].lower() or q in d["client"].lower()]
    return render("documents.html", active="documents", ret=ret, docs=docs[:60],
                  total=len(docs), categories=data.DOC_CATEGORIES, q=q, cat=cat,
                  return_id=rid)


# ---------------------------------------------------------------------------
# challenge 02 -- collaboration (internal vs client-visible threads)
# ---------------------------------------------------------------------------
@app.route("/returns/<rid>/messages")
def messages(rid):
    session["current_return"] = rid
    ret = data.RETURNS[rid]
    key, user = current_user()
    thread = data.MESSAGES.get(rid, [])
    if user["role"] == "client":
        thread = [m for m in thread if m["visibility"] == "client"]
    return render("messages.html", active="messages", ret=ret, thread=thread,
                  return_id=rid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
