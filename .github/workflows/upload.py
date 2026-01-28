import os
import random
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

CLIENT_ID = os.environ["YOUTUBE_CLIENT_ID"]
CLIENT_SECRET = os.environ["YOUTUBE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["YOUTUBE_REFRESH_TOKEN"]

creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

youtube = build("youtube", "v3", credentials=creds)

# Pick a video from repo folder "videos/"
video_files = os.listdir("videos")
video_file = random.choice(video_files)

titles = [
    "This AI cat is too cute 😭🐱",
    "I can’t stop watching this cat 😻",
    "AI made the cutest cat ever 🐾",
]

descriptions = [
    "Cute AI cat animation 🐱✨ #shorts",
    "This made my day 😻 #aicat",
]

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": random.choice(titles),
            "description": random.choice(descriptions),
            "tags": ["cat", "aicat", "shorts"],
            "categoryId": "15"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=f"videos/{video_file}"
)

response = request.execute()
print("Uploaded:", response["id"])
