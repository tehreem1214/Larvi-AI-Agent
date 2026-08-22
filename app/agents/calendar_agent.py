from datetime import datetime, timedelta
import re

from app.tools.calendar_tool import (
    get_upcoming_events,
    search_events,
    create_event,
    update_event,
    cancel_event,
)


# =========================================================
# TIMEZONE
# =========================================================

PAKISTAN_TIMEZONE = "Asia/Karachi"


# =========================================================
# DATE / TIME HELPERS
# =========================================================

def get_tomorrow_date():
    tomorrow = datetime.now() + timedelta(days=1)

    return tomorrow.strftime("%Y-%m-%d")


def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")


def make_datetime(date_str: str, time_str: str):
    return f"{date_str}T{time_str}:00+05:00"


# =========================================================
# PARSE TIME
# =========================================================

def parse_time(time_text: str):
    if not time_text:
        return None

    text = time_text.strip().upper()

    # Example: 4 PM, 4:30 PM
    match = re.search(
        r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM)",
        text,
    )

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        period = match.group(3)

        if hour < 1 or hour > 12:
            return None

        if minute < 0 or minute > 59:
            return None

        if period == "PM" and hour != 12:
            hour += 12

        if period == "AM" and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"

    # Example: 16:00
    match = re.search(
        r"\b(\d{1,2}):(\d{2})\b",
        text,
    )

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))

        if hour < 0 or hour > 23:
            return None

        if minute < 0 or minute > 59:
            return None

        return f"{hour:02d}:{minute:02d}"

    return None


# =========================================================
# EXTRACT TIME
# =========================================================

def extract_time(request: str):
    if not request:
        return None

    # 12-hour
    match = re.search(
        r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM))",
        request,
        re.IGNORECASE,
    )

    if match:
        return parse_time(match.group(1))

    # 24-hour
    match = re.search(
        r"\b(\d{1,2}:\d{2})\b",
        request,
        re.IGNORECASE,
    )

    if match:
        return parse_time(match.group(1))

    return None


# =========================================================
# EXTRACT CREATE TITLE
# =========================================================

def extract_create_title(request: str):
    patterns = [
        r"\bcalled\s+(.+)$",
        r"\bnamed\s+(.+)$",
        r"\btitled\s+(.+)$",
        r"\btitle\s+(.+)$",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            request,
            re.IGNORECASE,
        )

        if match:
            title = match.group(1).strip()

            title = re.sub(
                r"[.!?]+$",
                "",
                title,
            )

            return title.strip()

    return None


# =========================================================
# EXTRACT EVENT TITLE
# =========================================================

def extract_event_title(request: str):
    text = request.strip()

    patterns = [
        # Update
        r"^\s*update\s+(?:the\s+)?(.+?)\s+to\s+.+$",
        r"^\s*reschedule\s+(?:the\s+)?(.+?)\s+to\s+.+$",
        r"^\s*move\s+(?:the\s+)?(.+?)\s+to\s+.+$",
        r"^\s*change\s+(?:the\s+)?(.+?)\s+to\s+.+$",

        # Cancel
        r"^\s*cancel\s+(?:the\s+)?(.+?)\s*$",
        r"^\s*delete\s+(?:the\s+)?(.+?)\s*$",
        r"^\s*remove\s+(?:the\s+)?(.+?)\s*$",

        # Find
        r"^\s*find\s+(?:the\s+)?(.+?)\s*$",
        r"^\s*search\s+(?:for\s+)?(?:the\s+)?(.+?)\s*$",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            title = match.group(1).strip()

            title = re.sub(
                r"[.!?]+$",
                "",
                title,
            )

            return title.strip()

    return None


# =========================================================
# FIND EVENT BY TITLE
# =========================================================

def find_event_by_title(title: str):
    if not title:
        return None

    events = search_events(
        title,
        50,
    )

    if not events:
        return None

    wanted = title.strip().lower()

    exact_matches = []

    for event in events:
        summary = event.get(
            "summary",
            "",
        ).strip().lower()

        if summary == wanted:
            exact_matches.append(event)

    # Exact match preferred
    if exact_matches:
        # Calendar API normally returns upcoming events
        # in start-time order. We choose the first exact
        # upcoming event to avoid modifying an old duplicate.
        return exact_matches[0]

    # Fallback: first search result
    return events[0]


# =========================================================
# FORMAT EVENTS
# =========================================================

def format_events(events):
    if not events:
        return (
            "Aapke calendar mein koi upcoming "
            "event nahi hai."
        )

    lines = []

    for index, event in enumerate(
        events,
        start=1,
    ):
        lines.append(
            f"{index}. "
            f"{event.get('summary', 'Untitled event')}\n"
            f"   Start: "
            f"{event.get('start', 'Unknown')}\n"
            f"   End: "
            f"{event.get('end', 'Unknown')}\n"
            f"   Event ID: "
            f"{event.get('id', '')}"
        )

    return (
        "Aapke upcoming calendar events:\n\n"
        + "\n\n".join(lines)
    )


# =========================================================
# SHOW CALENDAR
# =========================================================

def show_calendar():
    events = get_upcoming_events(10)

    return format_events(events)


# =========================================================
# CREATE EVENT
# =========================================================

def handle_create_event(user_request: str):
    request = user_request.strip()

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = extract_create_title(request)

    if not title:
        return (
            "Event ka title nahi mila.\n\n"
            "Example:\n"
            "Schedule a meeting tomorrow at 4 PM "
            "called Larvi Test"
        )

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    time_value = extract_time(request)

    if not time_value:
        return (
            "Meeting ka time nahi mila.\n\n"
            "Example: tomorrow at 4 PM"
        )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    lower_request = request.lower()

    if "tomorrow" in lower_request:
        date_value = get_tomorrow_date()

    elif "today" in lower_request:
        date_value = get_today_date()

    else:
        date_value = get_today_date()

    # -----------------------------------------------------
    # START
    # -----------------------------------------------------

    start_time = make_datetime(
        date_value,
        time_value,
    )

    # -----------------------------------------------------
    # END = 1 HOUR
    # -----------------------------------------------------

    start_dt = datetime.fromisoformat(
        start_time
    )

    end_dt = start_dt + timedelta(
        hours=1
    )

    end_time = end_dt.isoformat()

    # -----------------------------------------------------
    # CREATE EVENT
    # -----------------------------------------------------

    result = create_event(
        summary=title,
        start_time=start_time,
        end_time=end_time,
    )

    if not result.get("success"):
        return (
            "Calendar event create nahi ho saka."
        )

    event = result.get(
        "event",
        {},
    )

    return (
        "Meeting successfully Google Calendar "
        "mein create ho gayi.\n\n"
        f"Title: {event.get('summary', title)}\n"
        f"Start: {event.get('start', start_time)}\n"
        f"End: {event.get('end', end_time)}\n"
        f"Event ID: {event.get('id', '')}"
    )


# =========================================================
# UPDATE EVENT
# =========================================================

def handle_update_event(user_request: str):
    request = user_request.strip()

    # -----------------------------------------------------
    # EVENT TITLE
    # -----------------------------------------------------

    title = extract_event_title(request)

    if not title:
        return (
            "Update karne wale event ka naam nahi mila.\n\n"
            "Example:\n"
            "update the Larvi Test to 5 PM tomorrow"
        )

    # -----------------------------------------------------
    # FIND EVENT
    # -----------------------------------------------------

    event = find_event_by_title(title)

    if not event:
        return (
            f"'{title}' naam ka calendar "
            "event nahi mila."
        )

    event_id = event.get("id")

    if not event_id:
        return (
            "Event ID nahi mili, is liye "
            "event update nahi kiya ja saka."
        )

    # -----------------------------------------------------
    # NEW TIME
    # -----------------------------------------------------

    new_time = extract_time(request)

    if not new_time:
        return (
            "Naya time nahi mila.\n\n"
            "Example:\n"
            "update the Larvi Test to 5 PM tomorrow"
        )

    # -----------------------------------------------------
    # NEW DATE
    # -----------------------------------------------------

    lower_request = request.lower()

    if "tomorrow" in lower_request:
        new_date = get_tomorrow_date()

    elif "today" in lower_request:
        new_date = get_today_date()

    else:
        old_start = event.get(
            "start",
            "",
        )

        if "T" in old_start:
            new_date = old_start.split(
                "T"
            )[0]
        else:
            new_date = get_today_date()

    # -----------------------------------------------------
    # NEW START
    # -----------------------------------------------------

    new_start = make_datetime(
        new_date,
        new_time,
    )

    # -----------------------------------------------------
    # NEW END = 1 HOUR
    # -----------------------------------------------------

    start_dt = datetime.fromisoformat(
        new_start
    )

    new_end = (
        start_dt + timedelta(hours=1)
    ).isoformat()

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    result = update_event(
        event_id=event_id,
        start_time=new_start,
        end_time=new_end,
    )

    if not result.get("success"):
        return (
            "Calendar event update nahi ho saka."
        )

    updated_event = result.get(
        "event",
        {},
    )

    return (
        "Meeting successfully update "
        "ho gayi.\n\n"
        f"Title: "
        f"{updated_event.get('summary', title)}\n"
        f"New Start: "
        f"{updated_event.get('start', new_start)}\n"
        f"New End: "
        f"{updated_event.get('end', new_end)}\n"
        f"Event ID: "
        f"{updated_event.get('id', event_id)}"
    )


# =========================================================
# FIND EVENT
# =========================================================

def handle_find_event(user_request: str):
    title = extract_event_title(
        user_request
    )

    if not title:
        return (
            "Please event ka naam batayein."
        )

    event = find_event_by_title(
        title
    )

    if not event:
        return (
            f"'{title}' naam ka event nahi mila."
        )

    return (
        "Event mil gaya:\n\n"
        f"Title: {event.get('summary', 'Untitled')}\n"
        f"Start: {event.get('start', 'Unknown')}\n"
        f"End: {event.get('end', 'Unknown')}\n"
        f"Event ID: {event.get('id', '')}"
    )


# =========================================================
# CANCEL EVENT
# =========================================================

def handle_cancel_event(user_request: str):
    title = extract_event_title(
        user_request
    )

    if not title:
        return (
            "Cancel karne wale event ka "
            "naam nahi mila."
        )

    event = find_event_by_title(
        title
    )

    if not event:
        return (
            f"'{title}' naam ka event "
            "nahi mila."
        )

    event_id = event.get("id")

    if not event_id:
        return "Event ID nahi mili."

    result = cancel_event(
        event_id
    )

    if not result.get("success"):
        return (
            "Event cancel nahi ho saka."
        )

    return (
        f"Event '{title}' successfully "
        "cancel kar diya gaya."
    )


# =========================================================
# CALENDAR AGENT
# =========================================================

def calendar_agent(
    user_request: str,
) -> str:

    request = user_request.strip()

    if not request:
        return (
            "Calendar request empty hai."
        )

    lower_request = request.lower()

    # =====================================================
    # 1. CANCEL
    # =====================================================

    if (
        lower_request.startswith("cancel ")
        or lower_request.startswith("delete ")
        or lower_request.startswith("remove ")
    ):
        return handle_cancel_event(
            request
        )

    # =====================================================
    # 2. UPDATE
    # =====================================================

    if (
        lower_request.startswith("update ")
        or lower_request.startswith("reschedule ")
        or lower_request.startswith("move ")
        or lower_request.startswith("change ")
    ):
        return handle_update_event(
            request
        )

    # =====================================================
    # 3. CREATE
    # =====================================================

    if (
        lower_request.startswith("schedule ")
        or lower_request.startswith("create ")
        or lower_request.startswith("book ")
        or lower_request.startswith("add ")
    ):
        return handle_create_event(
            request
        )

    # =====================================================
    # 4. FIND
    # =====================================================

    if (
        lower_request.startswith("find ")
        or lower_request.startswith("search ")
    ):
        return handle_find_event(
            request
        )

    # =====================================================
    # 5. SHOW CALENDAR
    # =====================================================

    show_commands = [
        "what is in my calendar",
        "what's in my calendar",
        "what is on my calendar",
        "show my calendar",
        "show calendar",
        "show my events",
        "show events",
        "calendar events",
        "upcoming events",
        "upcoming event",
        "my calendar",
        "my events",
    ]

    if any(
        command in lower_request
        for command in show_commands
    ):
        return show_calendar()

    # =====================================================
    # 6. FALLBACK
    # =====================================================

    return (
        "Calendar request samajh nahi aayi.\n\n"
        "Examples:\n"
        "- Schedule a meeting tomorrow at 4 PM "
        "called Larvi Test\n"
        "- What is in my calendar\n"
        "- Find Larvi Test\n"
        "- Update the Larvi Test to 5 PM tomorrow\n"
        "- Cancel Larvi Test"
    )
