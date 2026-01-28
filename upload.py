import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

creds = Credentials(
    None,
    refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["YOUTUBE_CLIENT_ID"],
    client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

youtube = build("youtube", "v3", credentials=creds)

video_path = "videos/short.mp4"

media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Cute AI Cat 😻",
            "description": "Cute AI cat animation 🐱✨ #shorts",
            "tags": ["cat", "aicat", "shorts"],
            "categoryId": "15"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=media
)

response = request.execute()
print("Uploaded:", response["id"])
