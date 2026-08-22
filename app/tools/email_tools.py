from app.auth.google_auth import get_saved_credentials
from googleapiclient.discovery import build


def get_gmail_service():
    credentials = get_saved_credentials()

    if credentials is None:
        raise Exception("Google account is not connected.")

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )


def get_recent_emails(max_results=10):
    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        maxResults=max_results,
    ).execute()

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=[
                "From",
                "To",
                "Subject",
                "Date",
            ],
        ).execute()

        headers = email_data.get("payload", {}).get(
            "headers",
            [],
        )

        email_info = {
            "id": message["id"],
            "from": "",
            "to": "",
            "subject": "",
            "date": "",
        }

        for header in headers:
            name = header.get("name")
            value = header.get("value", "")

            if name == "From":
                email_info["from"] = value

            elif name == "To":
                email_info["to"] = value

            elif name == "Subject":
                email_info["subject"] = value

            elif name == "Date":
                email_info["date"] = value

        emails.append(email_info)

    return emails