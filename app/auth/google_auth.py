from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials


load_dotenv()


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CLIENT_SECRETS_FILE = BASE_DIR / "google_client_secret.json"
TOKEN_FILE = BASE_DIR / "google_token.json"


# =========================================================
# GOOGLE SCOPES
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


# =========================================================
# REDIRECT URI
# =========================================================

REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"


# =========================================================
# CREATE GOOGLE FLOW
# =========================================================

def create_google_flow():
    if not CLIENT_SECRETS_FILE.exists():
        raise FileNotFoundError(
            f"Google client secret file not found: "
            f"{CLIENT_SECRETS_FILE}"
        )

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    return flow


# =========================================================
# GOOGLE LOGIN
# =========================================================

def get_authorization_url():
    flow = create_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes=False,
        prompt="consent",
    )

    return (
        authorization_url,
        state,
        flow.code_verifier,
    )


# =========================================================
# GOOGLE CALLBACK
# =========================================================

def exchange_code_for_token(
    code: str,
    code_verifier: str,
):
    flow = create_google_flow()

    # Restore PKCE verifier
    flow.code_verifier = code_verifier

    # Exchange authorization code
    flow.fetch_token(
        code=code
    )

    credentials = flow.credentials

    # Save credentials
    TOKEN_FILE.write_text(
        credentials.to_json(),
        encoding="utf-8",
    )

    return credentials


# =========================================================
# LOAD SAVED CREDENTIALS
# =========================================================

def get_saved_credentials():
    if not TOKEN_FILE.exists():
        return None

    try:
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES,
        )

        return credentials

    except Exception:
        return None