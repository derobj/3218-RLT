import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID     = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")
TOKEN      = os.getenv("FB_PAGE_ACCESS_TOKEN")


def get_long_lived_token(short_token: str) -> str:
    """Exchange a short-lived token for a 60-day token."""
    url = "https://graph.facebook.com/oauth/access_token"
    params = {
        "grant_type":        "fb_exchange_token",
        "client_id":         APP_ID,
        "client_secret":     APP_SECRET,
        "fb_exchange_token": short_token,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["access_token"]


def get_page_token(long_lived_user_token: str, page_id: str) -> str:
    """Get a never-expiring Page Access Token from a long-lived user token."""
    url = f"https://graph.facebook.com/{page_id}"
    params = {
        "fields":       "access_token",
        "access_token": long_lived_user_token,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["access_token"]


def refresh_token() -> str:
    """
    Full refresh flow: short-lived → long-lived user token → permanent page token.
    Returns the permanent page token.
    """
    print("Refreshing access token...")
    long_lived  = get_long_lived_token(TOKEN)
    page_token  = get_page_token(long_lived, os.getenv("FB_PAGE_ID"))
    print("Token refreshed successfully.")
    return page_token


if __name__ == "__main__":
    token = refresh_token()
    print(f"\nNew Page Access Token:\n{token}")
    print("\nUpdate FB_PAGE_ACCESS_TOKEN in your .env file with this value.")
