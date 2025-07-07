import os
import unittest
from src.quote_maker import generator
from src.quote_maker import generator_cy

class TestGenerator(unittest.TestCase):

    def test_create_quote_image(self):
        """Test that the image is created successfully."""
        quote = "This is a test quote."
        logo = "Test Logo"
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_long_quote(self):
        """Test with a long quote that requires text wrapping."""
        quote = "This is a very long quote that should definitely wrap to multiple lines in the generated image."
        logo = "Test Logo"
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_empty_quote(self):
        """Test with an empty quote."""
        quote = ""
        logo = "Test Logo"
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_empty_logo(self):
        """Test with an empty logo."""
        quote = "This is a test quote."
        logo = ""
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_special_characters_quote(self):
        """Test with a quote containing special characters."""
        quote = "!@#$%^&*()_+-=[]{};':\",./<>?"
        logo = "Test Logo"
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_special_characters_logo(self):
        """Test with a logo containing special characters."""
        quote = "This is a test quote."
        logo = "!@#$%^&*()_+-=[]{};':\",./<>?"
        image_path = generator.create_quote_image(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_create_quote_image_cy(self):
        """Test the Cython version of the image generator."""
        quote = "This is a test quote."
        logo = "Test Logo"
        image_path = generator_cy.create_quote_image_cy(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_long_quote_cy(self):
        """Test the Cython version with a long quote."""
        quote = "This is a very long quote that should definitely wrap to multiple lines in the generated image."
        logo = "Test Logo"
        image_path = generator_cy.create_quote_image_cy(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_empty_quote_cy(self):
        """Test the Cython version with an empty quote."""
        quote = ""
        logo = "Test Logo"
        image_path = generator_cy.create_quote_image_cy(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_empty_logo_cy(self):
        """Test the Cython version with an empty logo."""
        quote = "This is a test quote."
        logo = ""
        image_path = generator_cy.create_quote_image_cy(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

    def test_special_characters_quote_cy(self):
        """Test the Cython version with special characters."""
        quote = "!@#$%^&*()_+-=[]{};':\",./<>?"
        logo = "Test Logo"
        image_path = generator_cy.create_quote_image_cy(quote, logo)
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

if __name__ == "__main__":
    unittest.main()