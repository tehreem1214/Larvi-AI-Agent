from datetime import datetime, timezone
from typing import Optional

from app.auth.google_auth import get_saved_credentials
from googleapiclient.discovery import build


# =========================================================
# GOOGLE CALENDAR SERVICE
# =========================================================

def get_calendar_service():
    credentials = get_saved_credentials()

    if credentials is None:
        raise Exception("Google account is not connected.")

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )


# =========================================================
# FORMAT EVENT
# =========================================================

def _format_event(event):
    start = event.get("start", {})
    end = event.get("end", {})

    start_time = (
        start.get("dateTime")
        or start.get("date")
        or ""
    )

    end_time = (
        end.get("dateTime")
        or end.get("date")
        or ""
    )

    return {
        "id": event.get("id", ""),
        "summary": event.get(
            "summary",
            "No title",
        ),
        "description": event.get(
            "description",
            "",
        ),
        "location": event.get(
            "location",
            "",
        ),
        "start": start_time,
        "end": end_time,
        "status": event.get(
            "status",
            "",
        ),
        "html_link": event.get(
            "htmlLink",
            "",
        ),
    }


# =========================================================
# GET UPCOMING EVENTS
# =========================================================

def get_upcoming_events(max_results=10):

    service = get_calendar_service()

    now = datetime.now(
        timezone.utc
    ).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = result.get(
        "items",
        []
    )

    return [
        _format_event(event)
        for event in events
    ]


# =========================================================
# SEARCH EVENTS
# =========================================================

def search_events(
    query: str,
    max_results=10,
):

    service = get_calendar_service()

    now = datetime.now(
        timezone.utc
    ).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        q=query,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = result.get(
        "items",
        []
    )

    return [
        _format_event(event)
        for event in events
    ]


# =========================================================
# GET EVENT DETAILS
# =========================================================

def get_event(event_id: str):

    service = get_calendar_service()

    event = service.events().get(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    return _format_event(event)


# =========================================================
# CHECK AVAILABILITY
# =========================================================

def check_availability(
    start_time: str,
    end_time: str,
):

    service = get_calendar_service()

    body = {
        "timeMin": start_time,
        "timeMax": end_time,
        "items": [
            {
                "id": "primary"
            }
        ],
    }

    result = service.freebusy().query(
        body=body
    ).execute()

    calendars = result.get(
        "calendars",
        {}
    )

    primary = calendars.get(
        "primary",
        {}
    )

    busy_periods = primary.get(
        "busy",
        []
    )

    return {
        "available": len(
            busy_periods
        ) == 0,
        "busy": busy_periods,
        "start": start_time,
        "end": end_time,
    }


# =========================================================
# CREATE EVENT
# =========================================================

def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
):

    service = get_calendar_service()

    event_body = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Karachi",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body,
    ).execute()

    return {
        "success": True,
        "event": _format_event(
            created_event
        ),
        "message": "Calendar event created successfully.",
    }


# =========================================================
# UPDATE EVENT
# =========================================================

def update_event(
    event_id: str,
    summary: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
):

    service = get_calendar_service()

    event = service.events().get(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    if summary is not None:
        event["summary"] = summary

    if description is not None:
        event["description"] = description

    if location is not None:
        event["location"] = location

    if start_time is not None:
        event["start"] = {
            "dateTime": start_time,
            "timeZone": "Asia/Karachi",
        }

    if end_time is not None:
        event["end"] = {
            "dateTime": end_time,
            "timeZone": "Asia/Karachi",
        }

    updated_event = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event,
    ).execute()

    return {
        "success": True,
        "event": _format_event(
            updated_event
        ),
        "message": "Calendar event updated successfully.",
    }


# =========================================================
# RESCHEDULE EVENT
# =========================================================

def reschedule_event(
    event_id: str,
    new_start_time: str,
    new_end_time: str,
):

    return update_event(
        event_id=event_id,
        start_time=new_start_time,
        end_time=new_end_time,
    )


# =========================================================
# DELETE EVENT
# =========================================================

def delete_event(event_id: str):

    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id,
    ).execute()

    return {
        "success": True,
        "event_id": event_id,
        "message": "Calendar event deleted successfully.",
    }


# =========================================================
# CANCEL EVENT
# =========================================================

def cancel_event(event_id: str):

    return delete_event(
        event_id
    )
def search_events(query: str, max_results=10):
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        q=query,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = result.get("items", [])

    return [
        _format_event(event)
        for event in events
    ]