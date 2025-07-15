
"""
Facebook posting logic for the Quote Maker application.
"""

import requests
from config import config

def post_to_facebook(image_path: str, message: str):
    """
    Posts an image to a Facebook page.

    Args:
        image_path: The path to the image to post.
        message: The message to accompany the image.
    """
    url = f"https://graph.facebook.com/{config.FACEBOOK_PAGE_ID}/photos"
    params = {
        "access_token": config.FACEBOOK_ACCESS_TOKEN,
        "message": message,
    }
    try:
        with open(image_path, "rb") as image_file:
            files = {"source": image_file}
            response = requests.post(url, params=params, files=files)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print("Quote posted successfully to Facebook!")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Facebook: {e}")
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
