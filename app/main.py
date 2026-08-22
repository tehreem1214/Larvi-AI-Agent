import re

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.auth.google_auth import (
    get_authorization_url,
    exchange_code_for_token,
    get_saved_credentials,
)

from app.tools.gmail_tool import (
    get_recent_emails,
    search_emails,
    read_email,
    create_draft,
    send_email,
    reply_email,
)

from app.tools.calendar_tool import (
    get_upcoming_events,
)

from app.agents.master_agent import (
    ask_ai,
    summarize_email,
)

from app.agents.calendar_agent import (
    calendar_agent,
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Larvi",
    description="Autonomous Email & Calendar AI Agent",
    version="1.0.0",
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Larvi AI Agent is running!"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# GOOGLE LOGIN
# =========================================================

@app.get("/auth/login")
def google_login():
    try:
        authorization_url, state, code_verifier = (
            get_authorization_url()
        )

        response = RedirectResponse(
            url=authorization_url
        )

        response.set_cookie(
            key="google_code_verifier",
            value=code_verifier,
            httponly=True,
            samesite="lax",
        )

        return response

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# GOOGLE CALLBACK
# =========================================================

@app.get("/auth/callback")
def google_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {
            "success": False,
            "error": "Authorization code not received",
        }

    code_verifier = request.cookies.get(
        "google_code_verifier"
    )

    if not code_verifier:
        return {
            "success": False,
            "error": (
                "Google code verifier not found. "
                "Please start login again."
            ),
        }

    try:
        exchange_code_for_token(
            code,
            code_verifier,
        )

        return {
            "success": True,
            "message": "Google authentication successful!",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# GOOGLE AUTH STATUS
# =========================================================

@app.get("/auth/status")
def auth_status():
    try:
        credentials = get_saved_credentials()

        if credentials is None:
            return {
                "authenticated": False,
                "message": "Google account is not connected.",
            }

        return {
            "authenticated": True,
            "message": "Google account is connected.",
        }

    except Exception as e:
        return {
            "authenticated": False,
            "error": str(e),
        }


# =========================================================
# GMAIL TEST
# =========================================================

@app.get("/gmail/test")
def gmail_test():
    try:
        emails = get_recent_emails(5)

        return {
            "success": True,
            "emails": emails,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# GMAIL SEARCH
# =========================================================

@app.get("/gmail/search")
def gmail_search(query: str):
    try:
        emails = search_emails(
            query,
            10,
        )

        return {
            "success": True,
            "query": query,
            "emails": emails,
        }

    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e),
        }


# =========================================================
# GMAIL READ
# =========================================================

@app.get("/gmail/read")
def gmail_read(message_id: str):
    try:
        email = read_email(
            message_id
        )

        if not email:
            return {
                "success": False,
                "message_id": message_id,
                "error": "Email could not be read.",
            }

        return {
            "success": True,
            "email": email,
        }

    except Exception as e:
        return {
            "success": False,
            "message_id": message_id,
            "error": str(e),
        }


# =========================================================
# GMAIL SUMMARIZE
# =========================================================

@app.get("/gmail/summarize")
def gmail_summarize(message_id: str):
    try:
        email = read_email(
            message_id
        )

        if not email:
            return {
                "success": False,
                "message_id": message_id,
                "error": "Email could not be read.",
            }

        summary = summarize_email(
            email
        )

        return {
            "success": True,
            "message_id": message_id,
            "summary": summary,
        }

    except Exception as e:
        return {
            "success": False,
            "message_id": message_id,
            "error": str(e),
        }


# =========================================================
# CREATE GMAIL DRAFT
# =========================================================

@app.get("/gmail/draft")
def gmail_draft(
    to: str,
    subject: str,
    body: str,
):
    try:
        draft = create_draft(
            to=to,
            subject=subject,
            body=body,
        )

        return {
            "success": True,
            "message": "Email draft created successfully.",
            "draft": draft,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# SEND GMAIL EMAIL
# =========================================================

@app.get("/gmail/send")
def gmail_send(
    to: str,
    subject: str,
    body: str,
):
    try:
        result = send_email(
            to=to,
            subject=subject,
            body=body,
        )

        return {
            "success": True,
            "message": "Email sent successfully.",
            "result": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# REPLY TO GMAIL EMAIL
# =========================================================

@app.get("/gmail/reply")
def gmail_reply(
    message_id: str,
    body: str,
):
    try:
        result = reply_email(
            message_id=message_id,
            body=body,
        )

        return {
            "success": True,
            "message": "Reply sent successfully.",
            "result": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# CALENDAR TEST
# =========================================================

@app.get("/calendar/test")
def calendar_test():
    try:
        events = get_upcoming_events(10)

        return {
            "success": True,
            "events": events,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# =========================================================
# LARVI MASTER AGENT
# =========================================================

@app.get("/agent")
def agent(request: str):

    try:

        user_request = request.strip()

        if not user_request:
            return {
                "success": False,
                "request": request,
                "response": "Please enter a request.",
            }

        lower_request = user_request.lower()


        # =====================================================
        # CALENDAR REQUESTS
        # =====================================================

        calendar_keywords = [
            "calendar",
            "schedule",
            "scheduled",
            "meeting",
            "meetings",
            "event",
            "events",
            "appointment",
            "appointments",
            "reschedule",
            "cancel",
            "delete",
            "remove",
            "update",
            "move",
            "book",
        ]

        is_calendar_request = any(
            keyword in lower_request
            for keyword in calendar_keywords
        )

        if is_calendar_request:

            calendar_response = calendar_agent(
                user_request
            )

            return {
                "success": True,
                "request": request,
                "response": calendar_response,
            }


        # =====================================================
        # READ EMAIL BY ID
        # =====================================================

        if (
            "read email" in lower_request
            or "open email" in lower_request
            or "read the email" in lower_request
            or "open the email" in lower_request
        ):

            words = lower_request.split()

            email_id = None

            for word in words:

                cleaned_word = word.strip(
                    ".,!?;:\"'()[]{}"
                )

                if (
                    len(cleaned_word) >= 12
                    and cleaned_word.isalnum()
                ):

                    email_id = cleaned_word
                    break

            if not email_id:

                return {
                    "success": False,
                    "request": request,
                    "response": (
                        "Email ID nahi mili. "
                        "Example: read email 1a024f2b579676f7"
                    ),
                }

            email = read_email(
                email_id
            )

            if not email:

                return {
                    "success": False,
                    "request": request,
                    "response": "Email read nahi ho saki.",
                }

            return {
                "success": True,
                "request": request,
                "response": (
                    f"Subject: "
                    f"{email.get('subject', 'No subject')}\n"
                    f"From: "
                    f"{email.get('from', 'Unknown')}\n"
                    f"Date: "
                    f"{email.get('date', 'Unknown')}\n\n"
                    f"{email.get('body', 'No email body available.')}"
                ),
            }


        # =====================================================
        # RECENT EMAILS
        # =====================================================

        if (
            "recent email" in lower_request
            or "recent emails" in lower_request
            or "latest email" in lower_request
            or "latest emails" in lower_request
            or "show my emails" in lower_request
            or "show my email" in lower_request
            or "show emails" in lower_request
            or "show email" in lower_request
        ):

            emails = get_recent_emails(5)

            if not emails:

                return {
                    "success": True,
                    "request": request,
                    "response": (
                        "Aapki koi recent email nahi mili."
                    ),
                }

            email_lines = []

            for index, email in enumerate(
                emails,
                start=1,
            ):

                email_lines.append(
                    f"{index}. Subject: "
                    f"{email.get('subject', 'No subject')}\n"
                    f"   From: "
                    f"{email.get('from', 'Unknown')}\n"
                    f"   Date: "
                    f"{email.get('date', 'Unknown')}\n"
                    f"   ID: "
                    f"{email.get('id', '')}"
                )

            response = (
                "Aapki recent emails:\n\n"
                + "\n\n".join(email_lines)
            )

            return {
                "success": True,
                "request": request,
                "response": response,
            }


        # =====================================================
        # SEARCH EMAILS
        # =====================================================

        if (
            "find email" in lower_request
            or "find emails" in lower_request
            or "search email" in lower_request
            or "search emails" in lower_request
            or "email from" in lower_request
            or "emails from" in lower_request
        ):

            query = ""

            if "linkedin" in lower_request:
                query = "from:linkedin"

            elif "foodpanda" in lower_request:
                query = "from:foodpanda"

            elif "coinmarketcap" in lower_request:
                query = "from:coinmarketcap"

            else:

                return {
                    "success": True,
                    "request": request,
                    "response": (
                        "Please specify the sender or "
                        "keyword you want me to search for."
                    ),
                }

            emails = search_emails(
                query,
                10,
            )

            if not emails:

                return {
                    "success": True,
                    "request": request,
                    "response": (
                        "Mujhe is search ke liye "
                        "koi email nahi mili."
                    ),
                }

            email_lines = []

            for index, email in enumerate(
                emails,
                start=1,
            ):

                email_lines.append(
                    f"{index}. Subject: "
                    f"{email.get('subject', 'No subject')}\n"
                    f"   From: "
                    f"{email.get('from', 'Unknown')}\n"
                    f"   Date: "
                    f"{email.get('date', 'Unknown')}\n"
                    f"   ID: "
                    f"{email.get('id', '')}"
                )

            response = (
                "Search results:\n\n"
                + "\n\n".join(email_lines)
            )

            return {
                "success": True,
                "request": request,
                "response": response,
            }


        # =====================================================
        # SUMMARIZE EMAIL
        # =====================================================

        if (
            "summarize" in lower_request
            or "summarise" in lower_request
            or "summary of" in lower_request
        ):

            emails = []

            if "foodpanda" in lower_request:

                emails = search_emails(
                    "from:foodpanda",
                    10,
                )

            elif "linkedin" in lower_request:

                emails = search_emails(
                    "from:linkedin",
                    10,
                )

            elif "coinmarketcap" in lower_request:

                emails = search_emails(
                    "from:coinmarketcap",
                    10,
                )

            else:

                words = lower_request.split()

                email_id = None

                for word in words:

                    cleaned_word = word.strip(
                        ".,!?;:\"'()[]{}"
                    )

                    if (
                        len(cleaned_word) >= 12
                        and cleaned_word.isalnum()
                    ):

                        email_id = cleaned_word
                        break

                if email_id:

                    email = read_email(
                        email_id
                    )

                    if not email:

                        return {
                            "success": False,
                            "request": request,
                            "response": (
                                "Email read nahi ho saki."
                            ),
                        }

                    summary = summarize_email(
                        email
                    )

                    return {
                        "success": True,
                        "request": request,
                        "response": summary,
                    }

                emails = get_recent_emails(1)


            if not emails:

                return {
                    "success": True,
                    "request": request,
                    "response": (
                        "Summarize karne ke liye "
                        "koi email nahi mili."
                    ),
                }

            email_id = emails[0].get(
                "id"
            )

            if not email_id:

                return {
                    "success": False,
                    "request": request,
                    "response": "Email ID nahi mili.",
                }

            email = read_email(
                email_id
            )

            if not email:

                return {
                    "success": False,
                    "request": request,
                    "response": (
                        "Email read nahi ho saki."
                    ),
                }

            summary = summarize_email(
                email
            )

            return {
                "success": True,
                "request": request,
                "response": summary,
            }


        # =====================================================
        # CREATE EMAIL DRAFT
        # =====================================================

        if (
            "create a draft" in lower_request
            or "create draft" in lower_request
            or "draft an email" in lower_request
        ):

            match = re.search(
                r"to\s+(\S+)\s+"
                r"subject\s+(.+?)\s+"
                r"body\s+(.+)$",
                user_request,
                re.IGNORECASE,
            )

            if not match:

                return {
                    "success": False,
                    "request": request,
                    "response": (
                        "Draft banane ke liye format use karein:\n\n"
                        "create a draft email to "
                        "email@example.com "
                        "subject Test Subject "
                        "body Hello"
                    ),
                }

            to = match.group(1).strip()

            subject = match.group(2).strip()

            body = match.group(3).strip()


            # -------------------------------------------------
            # ACTUAL GMAIL DRAFT CREATION
            # -------------------------------------------------

            draft = create_draft(
                to=to,
                subject=subject,
                body=body,
            )


            draft_id = ""

            if isinstance(draft, dict):

                draft_id = (
                    draft.get("id")
                    or draft.get("draft_id")
                    or draft.get("message_id")
                    or ""
                )


            return {
                "success": True,
                "request": request,
                "response": (
                    "Email draft successfully "
                    "Gmail mein create ho gaya.\n\n"
                    f"To: {to}\n"
                    f"Subject: {subject}\n"
                    f"Draft ID: {draft_id}"
                ),
            }


        # =====================================================
        # SEND EMAIL
        # =====================================================

        if (
            "send email" in lower_request
            or "send an email" in lower_request
            or "send a email" in lower_request
        ):

            match = re.search(
                r"to\s+(\S+)\s+"
                r"subject\s+(.+?)\s+"
                r"body\s+(.+)$",
                user_request,
                re.IGNORECASE,
            )

            if not match:

                return {
                    "success": False,
                    "request": request,
                    "response": (
                        "Email send karne ke liye format use karein:\n\n"
                        "send email to "
                        "email@example.com "
                        "subject Test "
                        "body Hello"
                    ),
                }

            to = match.group(1).strip()

            subject = match.group(2).strip()

            body = match.group(3).strip()


            result = send_email(
                to=to,
                subject=subject,
                body=body,
            )


            return {
                "success": True,
                "request": request,
                "response": (
                    "Email successfully send ho gayi.\n\n"
                    f"To: {to}\n"
                    f"Subject: {subject}\n"
                    f"Result: {result}"
                ),
            }


        # =====================================================
        # REPLY EMAIL
        # =====================================================

        if (
            "reply to email" in lower_request
            or "reply email" in lower_request
            or "reply to the email" in lower_request
        ):

            match = re.search(
                r"reply\s+(?:to\s+)?(?:the\s+)?email\s+"
                r"([A-Za-z0-9]+)\s+"
                r"with\s+(.+)$",
                user_request,
                re.IGNORECASE,
            )

            if not match:

                return {
                    "success": False,
                    "request": request,
                    "response": (
                        "Reply ke liye format use karein:\n\n"
                        "reply to email "
                        "1a0293b0bb491c28 "
                        "with Hello, this is my reply."
                    ),
                }

            message_id = match.group(1).strip()

            body = match.group(2).strip()


            result = reply_email(
                message_id=message_id,
                body=body,
            )


            return {
                "success": True,
                "request": request,
                "response": (
                    "Reply successfully send ho gaya.\n\n"
                    f"Email ID: {message_id}\n"
                    f"Reply: {body}\n"
                    f"Result: {result}"
                ),
            }


        # =====================================================
        # GENERAL AI
        # =====================================================

        response = ask_ai(
            user_request=user_request,
            context="",
        )

        return {
            "success": True,
            "request": request,
            "response": response,
        }


    except Exception as e:

        return {
            "success": False,
            "request": request,
            "error": str(e),
        }
