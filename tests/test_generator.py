
import os
import unittest
from src.quote_maker import generator

class TestGenerator(unittest.TestCase):

    def test_create_quote_image(self):
        """Test that the image is created successfully."""
        quote = "This is a test quote."
        logo = "Test Logo"
        image_path = generator.create_quote_image(quote, logo)

        # Check that the image file was created
        self.assertTrue(os.path.exists(image_path))

        # Clean up the created image file
        os.remove(image_path)

if __name__ == "__main__":
    unittest.main()
