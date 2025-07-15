
"""
Configuration for the Quote Maker application.
"""

# Font settings
FONT_PATH = "src/quote_maker/fonts/Quote.ttf"
FONT_SIZE = 50

# Image settings
IMAGE_TYPE = "RGBA"
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 600
IMAGE_BG_COLORS = [(255, 0, 0), (51, 0, 51), (0, 0, 255), (0, 0, 0)]

# Facebook API settings
FACEBOOK_PAGE_ID = "your_page_id"
import os

FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "your_access_token")
