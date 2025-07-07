
"""
Image generation logic for the Quote Maker application.
"""

import textwrap
import random
from PIL import Image, ImageDraw, ImageFont
from config import config

def create_quote_image(text: str, logo: str) -> str:
    """
    Creates an image with the given quote and logo.

    Args:
        text: The quote to display on the image.
        logo: The logo to display on the image.

    Returns:
        The path to the generated image.
    """
    font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)
    bg_color = random.choice(config.IMAGE_BG_COLORS)

    img = Image.new(
        config.IMAGE_TYPE,
        (config.IMAGE_WIDTH, config.IMAGE_HEIGHT),
        bg_color
    )
    draw = ImageDraw.Draw(img)

    wrapper = textwrap.TextWrapper(width=config.FONT_SIZE)
    text_lines = wrapper.wrap(text=text)

    # Calculate text position
    y_text = (config.IMAGE_HEIGHT - (len(text_lines) * config.FONT_SIZE)) / 2

    for line in text_lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x_text = (config.IMAGE_WIDTH - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        y_text += line_height

    # Add logo
    draw.text((10, 10), logo, font=font, fill=(255, 255, 255))

    # Save the image
    image_name = f"{random.randint(1000, 9999)}.png"
    img.save(image_name)
    return image_name
