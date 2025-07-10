"""Tests for the WikipediaTool."""

import pytest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the parent directory to the path so we can import the tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import WikipediaTool


class TestWikipediaTool:
    """Test suite for the WikipediaTool."""
    
    def test_init(self):
        """Test that the tool can be initialized."""
        tool = WikipediaTool()
        assert tool.name == "WikipediaTool"
        assert "Wikipedia" in tool.description
    
    @patch('wikipedia.search')
    @patch('wikipedia.page')
    def test_run_success(self, mock_page, mock_search):
        """Test successful execution of the tool."""
        # Mock the search results
        mock_search.return_value = ["Python (programming language)"]
        
        # Mock the page object
        mock_page_obj = MagicMock()
        mock_page_obj.title = "Python (programming language)"
        mock_page_obj.summary = "Python is a high-level programming language."
        mock_page_obj.url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        mock_page.return_value = mock_page_obj
        
        # Create the tool and run it
        tool = WikipediaTool()
        result = tool._run("Python programming")
        
        # Check the result
        assert "Python (programming language)" in result
        assert "high-level programming language" in result
        assert "https://en.wikipedia.org/wiki/Python_(programming_language)" in result
        
        # Verify the mocks were called correctly
        mock_search.assert_called_once_with("Python programming")
        mock_page.assert_called_once_with("Python (programming language)", auto_suggest=False)
    
    @patch('wikipedia.search')
    def test_run_no_results(self, mock_search):
        """Test execution when no search results are found."""
        # Mock empty search results
        mock_search.return_value = []
        
        # Create the tool and run it
        tool = WikipediaTool()
        result = tool._run("NonexistentTopic12345")
        
        # Check the result
        assert "No Wikipedia results found for: NonexistentTopic12345" in result
        
        # Verify the mock was called correctly
        mock_search.assert_called_once_with("NonexistentTopic12345")
    
    @patch('wikipedia.search')
    @patch('wikipedia.page')
    def test_run_disambiguation(self, mock_page, mock_search):
        """Test execution when a disambiguation page is encountered."""
        # Mock the search results
        mock_search.return_value = ["Python"]
        
        # Mock the disambiguation error
        from wikipedia import DisambiguationError
        mock_page.side_effect = DisambiguationError("Python", ["Python (programming language)", "Monty Python"])
        
        # Create a mock for the second call to page
        mock_page_obj = MagicMock()
        mock_page_obj.title = "Python (programming language)"
        mock_page_obj.summary = "Python is a high-level programming language."
        mock_page_obj.url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        
        # Set up the mock to return the mock_page_obj on the second call
        mock_page.side_effect = [
            DisambiguationError("Python", ["Python (programming language)", "Monty Python"]),
            mock_page_obj
        ]
        
        # Create the tool and run it
        tool = WikipediaTool()
        result = tool._run("Python")
        
        # Check the result
        assert "Python (programming language)" in result
        assert "high-level programming language" in result 