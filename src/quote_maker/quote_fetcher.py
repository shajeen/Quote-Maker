"""
Quote fetching logic for the Quote Maker application.
"""

import json
import csv
import sqlite3
import requests
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import logging


class QuoteSource(ABC):
    """Abstract base class for quote sources."""
    
    @abstractmethod
    def get_quote(self) -> Optional[Dict[str, str]]:
        """Get a quote from the source."""
        pass


class APIQuoteSource(QuoteSource):
    """Quote source from external API."""
    
    def __init__(self, api_url: str, headers: Optional[Dict[str, str]] = None):
        self.api_url = api_url
        self.headers = headers or {}
        self.logger = logging.getLogger(__name__)
    
    def get_quote(self) -> Optional[Dict[str, str]]:
        """Fetch quote from API."""
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Handle different API response formats
            if isinstance(data, dict):
                return {
                    'text': data.get('text', data.get('quote', '')),
                    'author': data.get('author', 'Unknown')
                }
            elif isinstance(data, list) and len(data) > 0:
                quote = data[0]
                return {
                    'text': quote.get('text', quote.get('quote', '')),
                    'author': quote.get('author', 'Unknown')
                }
            return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error parsing API response: {e}")
            return None


class FileQuoteSource(QuoteSource):
    """Quote source from local files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
    
    def get_quote(self) -> Optional[Dict[str, str]]:
        """Get quote from file based on file extension."""
        try:
            if self.file_path.endswith('.json'):
                return self._get_from_json()
            elif self.file_path.endswith('.csv'):
                return self._get_from_csv()
            else:
                return self._get_from_text()
        except Exception as e:
            self.logger.error(f"Error reading file {self.file_path}: {e}")
            return None
    
    def _get_from_json(self) -> Optional[Dict[str, str]]:
        """Load quote from JSON file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                import random
                quote = random.choice(data)
                return {
                    'text': quote.get('text', quote.get('quote', '')),
                    'author': quote.get('author', 'Unknown')
                }
        return None
    
    def _get_from_csv(self) -> Optional[Dict[str, str]]:
        """Load quote from CSV file."""
        import random
        quotes = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            quotes = list(reader)
        
        if quotes:
            quote = random.choice(quotes)
            return {
                'text': quote.get('text', quote.get('quote', '')),
                'author': quote.get('author', 'Unknown')
            }
        return None
    
    def _get_from_text(self) -> Optional[Dict[str, str]]:
        """Load quote from plain text file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return {
                    'text': content,
                    'author': 'Unknown'
                }
        return None


class DatabaseQuoteSource(QuoteSource):
    """Quote source from SQLite database."""
    
    def __init__(self, db_path: str, table_name: str = 'quotes'):
        self.db_path = db_path
        self.table_name = table_name
        self.logger = logging.getLogger(__name__)
    
    def get_quote(self) -> Optional[Dict[str, str]]:
        """Get random quote from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT text, author FROM {self.table_name} ORDER BY RANDOM() LIMIT 1")
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return {
                    'text': result[0],
                    'author': result[1] or 'Unknown'
                }
            return None
            
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")
            return None


class ManualQuoteSource(QuoteSource):
    """Quote source for user-provided quotes."""
    
    def __init__(self, text: str, author: str = 'Unknown'):
        self.text = text
        self.author = author
    
    def get_quote(self) -> Optional[Dict[str, str]]:
        """Return the manually provided quote."""
        if self.text.strip():
            return {
                'text': self.text,
                'author': self.author
            }
        return None


class QuoteFetcher:
    """Main quote fetcher class that coordinates different sources."""
    
    def __init__(self):
        self.sources: List[QuoteSource] = []
        self.logger = logging.getLogger(__name__)
    
    def add_source(self, source: QuoteSource):
        """Add a quote source."""
        self.sources.append(source)
    
    def get_quote(self, source_type: str = 'manual', **kwargs) -> Optional[Dict[str, str]]:
        """Get quote from specified source type."""
        try:
            if source_type == 'api':
                source = APIQuoteSource(kwargs.get('api_url'), kwargs.get('headers'))
            elif source_type == 'file':
                source = FileQuoteSource(kwargs.get('file_path'))
            elif source_type == 'database':
                source = DatabaseQuoteSource(kwargs.get('db_path'), kwargs.get('table_name', 'quotes'))
            elif source_type == 'manual':
                source = ManualQuoteSource(kwargs.get('text'), kwargs.get('author', 'Unknown'))
            else:
                self.logger.error(f"Unknown source type: {source_type}")
                return None
            
            return source.get_quote()
            
        except Exception as e:
            self.logger.error(f"Error fetching quote: {e}")
            return None
    
    def get_quote_from_sources(self) -> Optional[Dict[str, str]]:
        """Get quote from any available source."""
        for source in self.sources:
            quote = source.get_quote()
            if quote:
                return quote
        return None