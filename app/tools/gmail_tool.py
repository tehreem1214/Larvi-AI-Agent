from app.auth.google_auth import get_saved_credentials

from googleapiclient.discovery import build

from email.mime.text import MIMEText

import base64


# =========================================================
# GMAIL SERVICE
# =========================================================

def get_gmail_service():
    """
    Create and return Gmail API service.
    """

    credentials = get_saved_credentials()

    if credentials is None:
        raise Exception(
            "Google account is not connected."
        )

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )


# =========================================================
# HELPER: EMAIL HEADERS
# =========================================================

def _get_headers(email_data):
    """
    Extract useful headers from Gmail message.
    """

    headers = (
        email_data
        .get("payload", {})
        .get("headers", [])
    )

    result = {
        "from": "",
        "to": "",
        "subject": "",
        "date": "",
    }

    for header in headers:

        name = header.get(
            "name",
            ""
        ).lower()

        value = header.get(
            "value",
            ""
        )

        if name == "from":
            result["from"] = value

        elif name == "to":
            result["to"] = value

        elif name == "subject":
            result["subject"] = value

        elif name == "date":
            result["date"] = value

    return result


# =========================================================
# GET RECENT EMAILS
# =========================================================

def get_recent_emails(max_results=10):
    """
    Get recent Gmail messages.
    """

    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        maxResults=max_results,
    ).execute()

    messages = result.get(
        "messages",
        []
    )

    emails = []

    for message in messages:

        email_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = _get_headers(
            email_data
        )

        emails.append(
            {
                "id": message["id"],
                **headers,
            }
        )

    return emails


# =========================================================
# SEARCH EMAILS
# =========================================================

def search_emails(
    query,
    max_results=10,
):
    """
    Search Gmail using Gmail search syntax.

    Example:
        from:foodpanda
        from:linkedin
        subject:invoice
    """

    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
    ).execute()

    messages = result.get(
        "messages",
        []
    )

    emails = []

    for message in messages:

        email_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = _get_headers(
            email_data
        )

        emails.append(
            {
                "id": message["id"],
                **headers,
            }
        )

    return emails


# =========================================================
# READ EMAIL
# =========================================================

def read_email(message_id):
    """
    Read a complete Gmail message.
    """

    service = get_gmail_service()

    email_data = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )

    headers = _get_headers(
        email_data
    )

    body = ""

    payload = email_data.get(
        "payload",
        {}
    )

    # -----------------------------------------------------
    # SIMPLE EMAIL BODY
    # -----------------------------------------------------

    body_data = (
        payload
        .get("body", {})
        .get("data")
    )

    if body_data:

        try:

            body = (
                base64.urlsafe_b64decode(
                    body_data
                )
                .decode(
                    "utf-8",
                    errors="ignore",
                )
            )

        except Exception:

            body = ""


    # -----------------------------------------------------
    # MULTIPART EMAIL
    # -----------------------------------------------------

    if not body:

        parts = payload.get(
            "parts",
            []
        )

        for part in parts:

            mime_type = part.get(
                "mimeType",
                ""
            )

            if mime_type == "text/plain":

                data = (
                    part
                    .get("body", {})
                    .get("data")
                )

                if data:

                    try:

                        body = (
                            base64.urlsafe_b64decode(
                                data
                            )
                            .decode(
                                "utf-8",
                                errors="ignore",
                            )
                        )

                    except Exception:

                        body = ""

                    if body:
                        break


    # -----------------------------------------------------
    # RETURN EMAIL
    # -----------------------------------------------------

    return {
        "id": message_id,
        **headers,
        "body": body,
    }


# =========================================================
# CREATE EMAIL DRAFT
# =========================================================

def create_draft(
    to: str,
    subject: str,
    body: str,
):
    """
    Create a normal Gmail draft.
    """

    service = get_gmail_service()

    message = MIMEText(
        body,
        "plain",
        "utf-8",
    )

    message["To"] = to
    message["Subject"] = subject

    encoded_message = (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode("utf-8")
    )

    draft_body = {
        "message": {
            "raw": encoded_message
        }
    }

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body=draft_body,
        )
        .execute()
    )

    return {
        "success": True,
        "draft_id": draft.get("id"),
        "message_id": (
            draft
            .get("message", {})
            .get("id")
        ),
        "message": (
            "Email draft created successfully."
        ),
    }


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    to: str,
    subject: str,
    body: str,
):
    """
    Send a new email.
    """

    service = get_gmail_service()

    message = MIMEText(
        body,
        "plain",
        "utf-8",
    )

    message["To"] = to
    message["Subject"] = subject

    encoded_message = (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode("utf-8")
    )

    send_body = {
        "raw": encoded_message
    }

    sent_message = (
        service.users()
        .messages()
        .send(
            userId="me",
            body=send_body,
        )
        .execute()
    )

    return {
        "success": True,
        "message_id": sent_message.get(
            "id"
        ),
        "message": (
            "Email sent successfully."
        ),
    }


# =========================================================
# REPLY TO EMAIL
# =========================================================

def reply_email(
    message_id: str,
    body: str,
):
    """
    Send a reply to an existing Gmail message.
    """

    service = get_gmail_service()

    original = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Message-ID",
                "References",
            ],
        )
        .execute()
    )

    headers = (
        original
        .get("payload", {})
        .get("headers", [])
    )

    original_sender = ""
    original_subject = ""
    message_id_header = ""
    references = ""

    for header in headers:

        name = (
            header
            .get("name", "")
            .lower()
        )

        value = header.get(
            "value",
            ""
        )

        if name == "from":

            original_sender = value

        elif name == "subject":

            original_subject = value

        elif name == "message-id":

            message_id_header = value

        elif name == "references":

            references = value

    if not original_sender:

        raise Exception(
            "Could not find the original sender."
        )

    # -----------------------------------------------------
    # REPLY SUBJECT
    # -----------------------------------------------------

    if original_subject.lower().startswith(
        "re:"
    ):

        reply_subject = original_subject

    else:

        reply_subject = (
            "Re: "
            + original_subject
        )

    # -----------------------------------------------------
    # CREATE REPLY MESSAGE
    # -----------------------------------------------------

    message = MIMEText(
        body,
        "plain",
        "utf-8",
    )

    message["To"] = original_sender
    message["Subject"] = reply_subject

    # -----------------------------------------------------
    # THREAD HEADERS
    # -----------------------------------------------------

    if message_id_header:

        message["In-Reply-To"] = (
            message_id_header
        )

        if references:

            message["References"] = (
                references
                + " "
                + message_id_header
            )

        else:

            message["References"] = (
                message_id_header
            )

    # -----------------------------------------------------
    # ENCODE
    # -----------------------------------------------------

    encoded_message = (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode("utf-8")
    )

    # -----------------------------------------------------
    # SEND REPLY
    # -----------------------------------------------------

    sent_message = (
        service.users()
        .messages()
        .send(
            userId="me",
            body={
                "raw": encoded_message
            },
        )
        .execute()
    )

    return {
        "success": True,
        "message_id": sent_message.get(
            "id"
        ),
        "message": (
            "Reply sent successfully."
        ),
    }
