from ollama import chat

from app.agents.email_agent import email_agent
from app.agents.calendar_agent import calendar_agent

from app.tools.gmail_tool import (
    get_recent_emails,
    search_emails,
    read_email,
)


MODEL = "llama3.2:latest"


# =========================================================
# GENERAL AI
# =========================================================

def ask_ai(user_request: str, context: str = "") -> str:

    prompt = f"""
You are Larvi, a personal AI assistant.

User request:
{user_request}

Available information:
{context}

Rules:
- Answer naturally.
- Use only the provided information.
- Do not invent facts.
- Keep the answer short and useful.
"""

    try:
        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.2,
                "num_predict": 150,
            },
        )

        result = response.message.content.strip()

        if not result:
            return "AI ne koi response generate nahi kiya."

        return result

    except Exception as e:
        return f"AI response failed: {str(e)}"


# =========================================================
# CLEAN EMAIL BODY
# =========================================================

def clean_email_body(body: str) -> str:

    if not body:
        return ""

    body = body.replace("\r\n", "\n")
    body = body.replace("\r", "\n")

    lines = []

    for line in body.split("\n"):

        line = line.strip()

        if not line:
            continue

        if "{ font-family:" in line:
            continue

        if line.startswith("* {"):
            continue

        if line.startswith("social-icons"):
            continue

        if line.startswith("Privacy"):
            continue

        if line.startswith("Unsubscribe"):
            continue

        if line.startswith("General terms"):
            continue

        if line.startswith("http") and len(line) > 200:
            continue

        lines.append(line)

    cleaned = "\n".join(lines)

    if len(cleaned) > 3000:
        cleaned = cleaned[:3000]

    return cleaned


# =========================================================
# SUMMARIZE EMAIL
# =========================================================

def summarize_email(email: dict) -> str:

    if not email:
        return "Email information available nahi hai."

    subject = email.get(
        "subject",
        "No subject",
    )

    sender = email.get(
        "from",
        "Unknown sender",
    )

    body = email.get(
        "body",
        "",
    )

    cleaned_body = clean_email_body(body)

    if not cleaned_body:
        return (
            f"Subject: {subject}\n"
            f"From: {sender}\n\n"
            "Is email ka readable body content "
            "available nahi hai."
        )

    prompt = f"""
Summarize this email.

Sender:
{sender}

Subject:
{subject}

Email:
{cleaned_body}

Return EXACTLY this format:

Main point: <one short sentence>

Important: <one short sentence>

Action: <one short sentence or No action required>

Rules:
- Use ONLY information present in the email.
- Do not invent information.
- Do not explain reasoning.
- Keep it concise.
"""

    try:

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0,
                "num_predict": 100,
            },
        )

        result = response.message.content.strip()

        if not result:
            return "AI summary generate nahi ho saki."

        return result

    except Exception as e:
        return f"AI summary failed: {str(e)}"


# =========================================================
# AUTONOMOUS EMAIL SUMMARY
# =========================================================

def autonomous_email_summary(user_request: str) -> str:

    request = user_request.lower().strip()

    if "foodpanda" in request:
        query = "from:foodpanda"

    elif "linkedin" in request:
        query = "from:linkedin"

    elif "coinmarketcap" in request:
        query = "from:coinmarketcap"

    else:
        query = None

    if query:
        emails = search_emails(query, 10)
    else:
        emails = get_recent_emails(10)

    if not emails:
        return "Summarize karne ke liye koi email nahi mili."

    email = emails[0]

    email_id = email.get("id")

    if not email_id:
        return "Email ID nahi mili."

    full_email = read_email(email_id)

    if not full_email:
        return "Email read nahi ho saki."

    return summarize_email(full_email)


# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(user_request: str) -> str:

    request = user_request.lower().strip()

    # =====================================================
    # CALENDAR - CHECK FIRST
    # =====================================================

    calendar_words = [
        "calendar",
        "schedule",
        "scheduled",
        "meeting",
        "meetings",
        "appointment",
        "appointments",
        "event",
        "events",
        "upcoming",
        "reschedule",
        "cancel",
        "delete event",
        "remove event",
        "update event",
        "update the",
    ]

    for word in calendar_words:

        if word in request:
            return "CALENDAR"

    # =====================================================
    # EMAIL
    # =====================================================

    email_words = [
        "email",
        "emails",
        "gmail",
        "inbox",
        "mail",
        "draft",
        "send email",
        "reply email",
    ]

    for word in email_words:

        if word in request:
            return "EMAIL"

    # =====================================================
    # GENERAL
    # =====================================================

    return "GENERAL"


# =========================================================
# MAIN LARVI AGENT
# =========================================================

def run_agent(user_request: str) -> str:

    request = user_request.strip()

    lower_request = request.lower()

    if not request:
        return "Please apni request enter karein."

    # =====================================================
    # EMAIL SUMMARY
    # =====================================================

    if (
        "summarize" in lower_request
        or "summarise" in lower_request
        or "summary" in lower_request
    ):

        if (
            "email" in lower_request
            or "foodpanda" in lower_request
            or "linkedin" in lower_request
            or "coinmarketcap" in lower_request
        ):

            return autonomous_email_summary(
                request
            )

    # =====================================================
    # INTENT
    # =====================================================

    intent = detect_intent(request)

    # =====================================================
    # CALENDAR
    # =====================================================

    if intent == "CALENDAR":

        return calendar_agent(
            request
        )

    # =====================================================
    # EMAIL
    # =====================================================

    if intent == "EMAIL":

        return email_agent(
            request
        )

    # =====================================================
    # GENERAL
    # =====================================================

    return ask_ai(
        request
    )