import os
import random
import subprocess
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# ---------- AUTH ----------
creds = Credentials(
    None,
    refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["YOUTUBE_CLIENT_ID"],
    client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

youtube = build("youtube", "v3", credentials=creds)

# ---------- PICK RANDOM VIDEO ----------
VIDEOS_DIR = "videos"

videos = [
    f for f in os.listdir(VIDEOS_DIR)
    if f.lower().endswith(".mp4")
]

if not videos:
    raise Exception("No MP4 videos found in videos folder")

video_file = random.choice(videos)
video_path = os.path.join(VIDEOS_DIR, video_file)

print(f"Uploading: {video_file}")

# ---------- UPLOAD ----------
media = MediaFileUpload(
    video_path,
    mimetype="video/mp4",
    resumable=True
)

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

video_id = response.get("id")
print("Uploaded:", video_id)

# ---------- DELETE + COMMIT AFTER SUCCESS ----------
if video_id:
    os.remove(video_path)
    print(f"Deleted local file: {video_file}")

    # Configure git (GitHub Actions environment)
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"])

    # Commit deletion back to repo
    subprocess.run(["git", "add", "videos"])
    subprocess.run(["git", "commit", "-m", f"Delete uploaded video: {video_file}"])
    subprocess.run(["git", "push"])
