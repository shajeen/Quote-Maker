"""
Main entry point for the Quote Maker application.
"""

import uuid

from src.quote_maker import generator
from src.quote_maker import facebook
from config import config



def main():
    """Main function to run the quote maker."""
    print("~~~ Quote Maker ~~~")

    quote_text = input("Enter your quote: ")
    if not quote_text.strip():
        print("Quote cannot be empty. Exiting.")
        return

    page_name = input("Enter your page name: ")
    if not page_name.strip():
        print("Page name cannot be empty. Exiting.")
        return

    logo_text = f"Published by, -{page_name}-"

    # Generate the image
    image_name = generator.create_quote_image(quote_text, logo_text)
    if image_name:
        print(f"Generated image: {image_name}")

        # Ask for confirmation to post to Facebook
        post_to_fb = input("Is it ok to post in facebook? (yes/no): ").lower()
        if post_to_fb.startswith("y"):
            # Post to Facebook
            facebook.post_to_facebook(image_name, logo_text)
        else:
            print("Image saved locally. Not posting to Facebook.")
    else:
        print("Image generation failed. Not proceeding with Facebook post.")

if __name__ == "__main__":
    main()