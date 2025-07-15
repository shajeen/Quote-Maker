"""
Main entry point for the Quote Maker application.
"""

import logging
import argparse
import sys
from pathlib import Path

from src.quote_maker.quote_fetcher import QuoteFetcher
from src.quote_maker.generator import ImageGenerator
from src.quote_maker.facebook import SocialPoster
from config.config import ConfigManager


def setup_logging(config_manager: ConfigManager):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config_manager.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config_manager.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Quote Maker - Generate and share quote images')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--quote-source', choices=['manual', 'api', 'file'], 
                       default='manual', help='Source for quotes')
    parser.add_argument('--quote-file', help='Path to quotes file (for file source)')
    parser.add_argument('--api-url', help='API URL for quotes (for api source)')
    parser.add_argument('--no-post', action='store_true', 
                       help='Generate image only, do not post to social media')
    parser.add_argument('--platform', choices=['facebook', 'all'], 
                       default='facebook', help='Social media platform to post to')
    parser.add_argument('--output', help='Output path for generated image')
    return parser.parse_args()


class QuoteMakerApp:
    """Main application class for Quote Maker."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize the Quote Maker application.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_manager = ConfigManager(config_file)
        setup_logging(self.config_manager)
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.quote_fetcher = QuoteFetcher()
        self.image_generator = ImageGenerator(self.config_manager)
        self.social_poster = SocialPoster(self.config_manager)
        
        self.logger.info("Quote Maker application initialized")
    
    def get_user_input(self):
        """Get quote and page name from user input."""
        print("~~~ Quote Maker ~~~")
        
        quote_text = input("Enter your quote: ").strip()
        if not quote_text:
            print("Quote cannot be empty. Exiting.")
            return None, None
        
        page_name = input("Enter your page name: ").strip()
        if not page_name:
            print("Page name cannot be empty. Exiting.")
            return None, None
        
        return quote_text, page_name
    
    def get_quote_from_source(self, source: str, **kwargs):
        """Get quote from specified source."""
        if source == 'manual':
            quote_text, page_name = self.get_user_input()
            if not quote_text or not page_name:
                return None
            return {
                'text': quote_text,
                'author': page_name
            }
        else:
            quote_data = self.quote_fetcher.get_quote(source, **kwargs)
            if not quote_data:
                self.logger.error(f"Failed to get quote from {source}")
                return None
            return quote_data
    
    def run(self, args):
        """Run the main application logic."""
        try:
            # Get quote from specified source
            quote_kwargs = {}
            if args.quote_file:
                quote_kwargs['file_path'] = args.quote_file
            if args.api_url:
                quote_kwargs['api_url'] = args.api_url
            
            quote_data = self.get_quote_from_source(args.quote_source, **quote_kwargs)
            if not quote_data:
                return False
            
            # Prepare logo text
            if args.quote_source == 'manual':
                logo_text = f"Published by, -{quote_data['author']}-"
            else:
                logo_text = f"'{quote_data['text']}' - {quote_data['author']}"
                # For non-manual sources, get page name from user
                page_name = input("Enter your page name: ").strip()
                if page_name:
                    logo_text = f"Published by, -{page_name}-"
            
            # Generate image
            self.logger.info("Generating quote image...")
            image_path = self.image_generator.create_quote_image(
                quote_data['text'], 
                logo_text,
                args.output
            )
            
            if not image_path:
                print("Image generation failed.")
                return False
            
            print(f"Generated image: {image_path}")
            
            # Post to social media if requested
            if not args.no_post:
                if args.quote_source == 'manual':
                    post_confirm = input("Is it ok to post to social media? (yes/no): ").lower()
                    if not post_confirm.startswith('y'):
                        print("Image saved locally. Not posting to social media.")
                        return True
                
                self.logger.info(f"Posting to {args.platform}...")
                if args.platform == 'facebook':
                    success = self.social_poster.post_to_platform('facebook', image_path, logo_text)
                elif args.platform == 'all':
                    results = self.social_poster.post_to_all_platforms(image_path, logo_text)
                    success = any(results.values())
                
                if success:
                    print("Posted successfully to social media!")
                else:
                    print("Failed to post to social media.")
            
            return True
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")
            return False


def main():
    """Main function to run the quote maker."""
    args = parse_arguments()
    
    app = QuoteMakerApp(args.config)
    success = app.run(args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()