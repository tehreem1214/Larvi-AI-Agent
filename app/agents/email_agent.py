from app.tools.gmail_tool import (
    get_recent_emails,
    search_emails,
    read_email,
    create_draft,
    send_email,
    reply_email,
)


def email_agent(user_request: str):
    """
    Handles email-related requests.
    """

    request = user_request.lower().strip()

    # =====================================================
    # RECENT EMAILS
    # =====================================================

    if (
        "recent email" in request
        or "recent emails" in request
        or "latest email" in request
        or "latest emails" in request
        or "show my emails" in request
        or "show my email" in request
        or "show emails" in request
        or "show email" in request
    ):

        emails = get_recent_emails(10)

        if not emails:
            return "Aapki inbox mein koi recent email nahi mili."

        response = "Aapki recent emails:\n\n"

        for i, email in enumerate(emails, start=1):

            response += (
                f"{i}. Subject: "
                f"{email.get('subject', 'No subject')}\n"
                f"   From: "
                f"{email.get('from', 'Unknown')}\n"
                f"   Date: "
                f"{email.get('date', 'Unknown')}\n"
                f"   ID: "
                f"{email.get('id', '')}\n\n"
            )

        return response

    # =====================================================
    # SEARCH EMAILS
    # =====================================================

    if (
        "find email" in request
        or "find emails" in request
        or "search email" in request
        or "search emails" in request
        or "email from" in request
        or "emails from" in request
    ):

        if "foodpanda" in request:
            query = "from:foodpanda"

        elif "linkedin" in request:
            query = "from:linkedin"

        elif "coinmarketcap" in request:
            query = "from:coinmarketcap"

        else:
            return (
                "Please specify the sender. "
                "Example: find emails from foodpanda"
            )

        emails = search_emails(query, 10)

        if not emails:
            return "Mujhe is search ke liye koi email nahi mili."

        response = "Search results:\n\n"

        for i, email in enumerate(emails, start=1):

            response += (
                f"{i}. Subject: "
                f"{email.get('subject', 'No subject')}\n"
                f"   From: "
                f"{email.get('from', 'Unknown')}\n"
                f"   Date: "
                f"{email.get('date', 'Unknown')}\n"
                f"   ID: "
                f"{email.get('id', '')}\n\n"
            )

        return response

    # =====================================================
    # READ EMAIL
    # =====================================================

    if (
        "read email" in request
        or "open email" in request
    ):

        words = request.split()
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
            return (
                "Email ID nahi mili.\n"
                "Example: read email 1a024f2b579676f7"
            )

        email = read_email(email_id)

        if not email:
            return "Email read nahi ho saki."

        return (
            f"Subject: {email.get('subject', 'No subject')}\n"
            f"From: {email.get('from', 'Unknown')}\n"
            f"Date: {email.get('date', 'Unknown')}\n\n"
            f"{email.get('body', 'No email body available.')}"
        )

    # =====================================================
    # CREATE DRAFT
    # =====================================================

    if "create draft" in request or "make draft" in request:

        return (
            "Draft creation is available through the "
            "/gmail/draft endpoint."
        )

    # =====================================================
    # SEND EMAIL
    # =====================================================

    if (
        "send email" in request
        or "send an email" in request
    ):

        return (
            "Email sending is available, but Larvi requires "
            "the recipient, subject, and body before sending."
        )

    # =====================================================
    # REPLY TO EMAIL
    # =====================================================

    if (
        "reply to email" in request
        or "reply email" in request
        or "reply to" in request
    ):

        return (
            "Reply feature is ready. "
            "Please provide the email ID and reply message."
        )

    # =====================================================
    # DEFAULT
    # =====================================================

    return (
        "Email request samajh nahi aayi. "
        "Aap recent emails, search, read, draft, send "
        "ya reply email ke liye request kar sakti hain."
    )
