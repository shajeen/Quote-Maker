"""
Main entry point for the Quote Maker application.
"""

import uuid
import requests
from src.quote_maker import generator
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
    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        response = requests.post(url, params=params, files=files)

    if response.status_code == 200:
        print("Quote posted successfully to Facebook!")
    else:
        print(f"Error posting to Facebook: {response.text}")

def main():
    """Main function to run the quote maker."""
    print("~~~ Quote Maker ~~~")

    quote_text = input("Enter your quote: ")
    page_name = input("Enter your page name: ")
    logo_text = f"Published by, -{page_name}-"

    # Generate the image
    image_name = generator.create_quote_image(quote_text, logo_text)
    print(f"Generated image: {image_name}")

    # Ask for confirmation to post to Facebook
    post_to_fb = input("Is it ok to post in facebook? (yes/no): ").lower()
    if post_to_fb == "yes":
        # Post to Facebook
        post_to_facebook(image_name, logo_text)
    else:
        print("Image saved locally. Not posting to Facebook.")

if __name__ == "__main__":
    main()