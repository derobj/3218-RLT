import os
import time
import tempfile
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

from caption import generate_caption
from video import build_reel

load_dotenv()

# Config
PAGE_TOKEN  = os.getenv("FB_PAGE_ACCESS_TOKEN")
IG_ID       = os.getenv("IG_ACCOUNT_ID")
PAGE_ID     = os.getenv("FB_PAGE_ID")

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
)

GRAPH = "https://graph.facebook.com/v20.0"


def upload_video(local_path: str) -> str:
    """Upload video to Cloudinary and return a public URL."""
    print("Uploading video to Cloudinary...")
    result = cloudinary.uploader.upload(
        local_path,
        resource_type = "video",
        folder        = "rlt-social",
    )
    url = result["secure_url"]
    print(f"Uploaded: {url}")
    return url


def post_instagram_reel(video_url: str, caption: str) -> str:
    """Create and publish an Instagram Reel. Returns the media ID."""
    print("Creating Instagram Reel container...")
    r = requests.post(
        f"{GRAPH}/{IG_ID}/media",
        data={
            "media_type":  "REELS",
            "video_url":   video_url,
            "caption":     caption,
            "access_token": PAGE_TOKEN,
        },
    )
    r.raise_for_status()
    container_id = r.json()["id"]
    print(f"Container created: {container_id}")

    # Poll until video is processed
    print("Waiting for video to process...")
    for attempt in range(20):
        time.sleep(15)
        status = requests.get(
            f"{GRAPH}/{container_id}",
            params={
                "fields":       "status_code",
                "access_token": PAGE_TOKEN,
            },
        ).json()
        code = status.get("status_code")
        print(f"  Status: {code}")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"Instagram video processing failed: {status}")
    else:
        raise RuntimeError("Timed out waiting for Instagram video processing")

    # Publish
    print("Publishing Reel...")
    pub = requests.post(
        f"{GRAPH}/{IG_ID}/media_publish",
        data={
            "creation_id":  container_id,
            "access_token": PAGE_TOKEN,
        },
    )
    pub.raise_for_status()
    media_id = pub.json()["id"]
    print(f"Instagram Reel published: {media_id}")
    return media_id


def post_facebook_video(video_url: str, caption: str) -> str:
    """Post the video to the Facebook Page. Returns the post ID."""
    print("Posting to Facebook...")
    r = requests.post(
        f"{GRAPH}/{PAGE_ID}/videos",
        data={
            "file_url":     video_url,
            "description":  caption,
            "access_token": PAGE_TOKEN,
        },
    )
    r.raise_for_status()
    post_id = r.json().get("id")
    print(f"Facebook post published: {post_id}")
    return post_id


def run():
    print("=== Road Less Traveled — Social Post ===\n")

    # 1. Generate caption
    print("Generating caption...")
    caption = generate_caption()
    print(f"\nCaption:\n{caption}\n")

    # 2. Build reel
    print("Building Reel video...")
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        tmp_path = f.name
    build_reel(tmp_path)
    print(f"Reel built: {tmp_path}\n")

    # 3. Upload to Cloudinary
    video_url = upload_video(tmp_path)

    # 4. Post to Instagram
    post_instagram_reel(video_url, caption)

    # 5. Post to Facebook
    post_facebook_video(video_url, caption)

    # 6. Clean up local temp file
    os.unlink(tmp_path)

    print("\n=== Done ===")


if __name__ == "__main__":
    run()
