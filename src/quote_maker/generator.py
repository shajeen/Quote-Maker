
"""
Image generation logic for the Quote Maker application.
"""

import textwrap
import random
import uuid
import logging
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from config import config


class ImageGenerator:
    """Handles image generation for quotes."""
    
    def __init__(self, config_manager=None):
        """
        Initialize the ImageGenerator.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager or config
        self.logger = logging.getLogger(__name__)
    
    def create_quote_image(self, text: str, logo: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Creates an image with the given quote and logo.

        Args:
            text: The quote to display on the image.
            logo: The logo to display on the image.
            output_path: Custom output path for the image (optional).

        Returns:
            The path to the generated image or None if failed.
        """
        try:
            font = self._load_font()
            if not font:
                return None
            
            bg_color = self._get_random_background_color()
            
            img = Image.new(
                self.config_manager.IMAGE_TYPE,
                (self.config_manager.IMAGE_WIDTH, self.config_manager.IMAGE_HEIGHT),
                bg_color
            )
            draw = ImageDraw.Draw(img)

            # Process and draw text
            text_lines = self._wrap_text(text)
            y_text = self._calculate_text_position(
                len(text_lines), self.config_manager.FONT_SIZE, self.config_manager.IMAGE_HEIGHT
            )

            for line in text_lines:
                x_text, line_height = self._draw_text_line(draw, line, font, y_text)
                y_text += line_height

            # Add logo
            self._draw_logo(draw, logo, font)

            # Save the image
            image_name = output_path or f"{uuid.uuid4()}.png"
            img.save(image_name)
            self.logger.info(f"Image saved: {image_name}")
            return image_name
            
        except Exception as e:
            self.logger.error(f"Error generating image: {e}")
            return None
    
    def _load_font(self) -> Optional[ImageFont.FreeTypeFont]:
        """Load the font file."""
        try:
            return ImageFont.truetype(self.config_manager.FONT_PATH, self.config_manager.FONT_SIZE)
        except IOError:
            self.logger.error(f"Font file not found at {self.config_manager.FONT_PATH}")
            return None
    
    def _get_random_background_color(self) -> Tuple[int, int, int]:
        """Get a random background color."""
        return random.choice(self.config_manager.IMAGE_BG_COLORS)
    
    def _wrap_text(self, text: str) -> list:
        """Wrap text based on font size."""
        wrapper = textwrap.TextWrapper(width=self.config_manager.FONT_SIZE)
        return wrapper.wrap(text=text)
    
    def _draw_text_line(self, draw: ImageDraw.Draw, line: str, font: ImageFont.FreeTypeFont, y_text: float) -> Tuple[float, float]:
        """Draw a single line of text and return its position and height."""
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x_text = (self.config_manager.IMAGE_WIDTH - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
        return x_text, line_height
    
    def _draw_logo(self, draw: ImageDraw.Draw, logo: str, font: ImageFont.FreeTypeFont):
        """Draw the logo on the image."""
        draw.text((10, 10), logo, font=font, fill=(255, 255, 255))
    
    def _calculate_text_position(self, text_lines: int, font_size: int, image_height: int) -> float:
        """Calculate the starting y-coordinate for vertically centering text."""
        return (image_height - (text_lines * font_size)) / 2


# Backward compatibility function
def create_quote_image(text: str, logo: str) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        text: The quote to display on the image.
        logo: The logo to display on the image.

    Returns:
        The path to the generated image.
    """
    generator = ImageGenerator()
    return generator.create_quote_image(text, logo)
