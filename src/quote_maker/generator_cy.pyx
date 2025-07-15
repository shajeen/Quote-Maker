
"""
Cython version of the image generation logic.
"""

import textwrap
import random
from PIL import Image, ImageDraw, ImageFont
from config import config

def create_quote_image_cy(str text, str logo):
    """
    Creates an image with the given quote and logo (Cython version).

    Args:
        text: The quote to display on the image.
        logo: The logo to display on the image.

    Returns:
        The path to the generated image.
    """
    try:
        font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)
    except IOError:
        print(f"Error: Font file not found at {config.FONT_PATH}")
        return None

    bg_color = random.choice(config.IMAGE_BG_COLORS)

    try:
        img = Image.new(
            config.IMAGE_TYPE,
            (config.IMAGE_WIDTH, config.IMAGE_HEIGHT),
            bg_color
        )
        draw = ImageDraw.Draw(img)

        wrapper = textwrap.TextWrapper(width=config.FONT_SIZE)
        text_lines = wrapper.wrap(text=text)

        y_text = _calculate_text_position(
            len(text_lines), config.FONT_SIZE, config.IMAGE_HEIGHT
        )

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
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def _calculate_text_position(
    text_lines: int, font_size: int, image_height: int
) -> float:
    """Calculates the starting y-coordinate for vertically centering text.

    Args:
        text_lines: The number of lines of text.
        font_size: The font size.
        image_height: The height of the image.

    Returns:
        The y-coordinate for the text.
    """
    return (image_height - (text_lines * font_size)) / 2
