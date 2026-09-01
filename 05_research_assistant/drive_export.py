import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import os, json

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

def get_flow():
    client_config = json.loads(st.secrets["GDRIVE_OAUTH_CLIENT"])
    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def get_auth_url():
    flow = get_flow()
    auth_url, state = flow.authorization_url(prompt="consent")
    st.session_state["oauth_state"] = state
    return auth_url

def exchange_code(code):
    flow = get_flow()
    flow.fetch_token(code=code)
    st.session_state["drive_creds"] = flow.credentials
    return flow.credentials

def upload_to_user_drive(filename: str, content: str) -> str:
    creds = st.session_state.get("drive_creds")
    service = build("drive", "v3", credentials=creds)

    media = MediaInMemoryUpload(content.encode("utf-8"),
                                 mimetype="text/markdown")
    file = service.files().create(
        body={"name": filename},
        media_body=media,
        fields="webViewLink"
    ).execute()
    return file.get("webViewLink")