
"""
Social media posting logic for the Quote Maker application.
"""

import requests
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from config import config


class SocialPlatform(ABC):
    """Abstract base class for social media platforms."""
    
    @abstractmethod
    def post_image(self, image_path: str, message: str) -> bool:
        """Post an image with a message to the platform."""
        pass


class FacebookPoster(SocialPlatform):
    """Facebook posting implementation."""
    
    def __init__(self, page_id: str, access_token: str):
        """
        Initialize Facebook poster.
        
        Args:
            page_id: Facebook page ID
            access_token: Facebook access token
        """
        self.page_id = page_id
        self.access_token = access_token
        self.logger = logging.getLogger(__name__)
    
    def post_image(self, image_path: str, message: str) -> bool:
        """
        Posts an image to a Facebook page.

        Args:
            image_path: The path to the image to post.
            message: The message to accompany the image.
            
        Returns:
            True if successful, False otherwise.
        """
        if not self.access_token:
            self.logger.error("Facebook access token is not configured")
            return False
        
        url = f"https://graph.facebook.com/{self.page_id}/photos"
        params = {
            "access_token": self.access_token,
            "message": message,
        }
        
        try:
            with open(image_path, "rb") as image_file:
                files = {"source": image_file}
                response = requests.post(url, params=params, files=files, timeout=30)
            
            response.raise_for_status()
            self.logger.info("Quote posted successfully to Facebook!")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error posting to Facebook: {e}")
            return False
        except FileNotFoundError:
            self.logger.error(f"Image file not found at {image_path}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error occurred: {e}")
            return False


class TwitterPoster(SocialPlatform):
    """Twitter posting implementation (placeholder)."""
    
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """
        Initialize Twitter poster.
        
        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_token_secret: Twitter access token secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.logger = logging.getLogger(__name__)
    
    def post_image(self, image_path: str, message: str) -> bool:
        """
        Posts an image to Twitter (placeholder implementation).
        
        Args:
            image_path: The path to the image to post.
            message: The message to accompany the image.
            
        Returns:
            True if successful, False otherwise.
        """
        self.logger.warning("Twitter posting not implemented yet")
        return False


class InstagramPoster(SocialPlatform):
    """Instagram posting implementation (placeholder)."""
    
    def __init__(self, access_token: str):
        """
        Initialize Instagram poster.
        
        Args:
            access_token: Instagram access token
        """
        self.access_token = access_token
        self.logger = logging.getLogger(__name__)
    
    def post_image(self, image_path: str, message: str) -> bool:
        """
        Posts an image to Instagram (placeholder implementation).
        
        Args:
            image_path: The path to the image to post.
            message: The message to accompany the image.
            
        Returns:
            True if successful, False otherwise.
        """
        self.logger.warning("Instagram posting not implemented yet")
        return False


class SocialPoster:
    """Main social media poster class that coordinates different platforms."""
    
    def __init__(self, config_manager=None):
        """
        Initialize the SocialPoster.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager or config
        self.platforms: Dict[str, SocialPlatform] = {}
        self.logger = logging.getLogger(__name__)
        self._setup_platforms()
    
    def _setup_platforms(self):
        """Setup available social media platforms."""
        # Setup Facebook
        if hasattr(self.config_manager, 'FACEBOOK_PAGE_ID') and hasattr(self.config_manager, 'FACEBOOK_ACCESS_TOKEN'):
            if self.config_manager.FACEBOOK_ACCESS_TOKEN:
                self.platforms['facebook'] = FacebookPoster(
                    self.config_manager.FACEBOOK_PAGE_ID,
                    self.config_manager.FACEBOOK_ACCESS_TOKEN
                )
    
    def add_platform(self, name: str, platform: SocialPlatform):
        """Add a social media platform."""
        self.platforms[name] = platform
    
    def post_to_platform(self, platform_name: str, image_path: str, message: str) -> bool:
        """
        Post to a specific platform.
        
        Args:
            platform_name: Name of the platform
            image_path: Path to the image
            message: Message to post
            
        Returns:
            True if successful, False otherwise.
        """
        if platform_name not in self.platforms:
            self.logger.error(f"Platform '{platform_name}' not configured")
            return False
        
        return self.platforms[platform_name].post_image(image_path, message)
    
    def post_to_all_platforms(self, image_path: str, message: str) -> Dict[str, bool]:
        """
        Post to all configured platforms.
        
        Args:
            image_path: Path to the image
            message: Message to post
            
        Returns:
            Dictionary mapping platform names to success status.
        """
        results = {}
        for platform_name, platform in self.platforms.items():
            results[platform_name] = platform.post_image(image_path, message)
        return results
    
    def get_available_platforms(self) -> list:
        """Get list of available platforms."""
        return list(self.platforms.keys())


# Backward compatibility function
def post_to_facebook(image_path: str, message: str):
    """
    Legacy function for backward compatibility.
    
    Args:
        image_path: The path to the image to post.
        message: The message to accompany the image.
    """
    poster = SocialPoster()
    success = poster.post_to_platform('facebook', image_path, message)
    if success:
        print("Quote posted successfully to Facebook!")
    else:
        print("Failed to post to Facebook.")
