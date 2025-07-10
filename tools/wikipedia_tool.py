"""Wikipedia Tool for the Research Assistant Agent."""

from typing import Dict, Any, Optional
import wikipedia
from langchain.tools import BaseTool


class WikipediaTool(BaseTool):
    """Tool for searching Wikipedia."""
    
    name: str = "WikipediaTool"
    description: str = """
    Useful for retrieving information about people, places, events, concepts, etc.
    Input should be a search query. The tool will return a summary of the Wikipedia article.
    Use this when you need factual information or background knowledge.
    """
    
    def _run(self, query: str) -> str:
        """Run the tool with the provided query."""
        try:
            # First try to find the exact page
            page_results = wikipedia.search(query)
            if not page_results:
                return f"No Wikipedia results found for: {query}"
            
            # Try to get the most relevant page
            try:
                page = wikipedia.page(page_results[0], auto_suggest=False)
            except wikipedia.DisambiguationError as e:
                # If disambiguation page, take the first option
                page = wikipedia.page(e.options[0], auto_suggest=False)
            
            # Get summary and basic info
            summary = page.summary
            
            # Return formatted result
            result = f"Title: {page.title}\n\nSummary: {summary}\n\nURL: {page.url}"
            return result
            
        except Exception as e:
            return f"Error retrieving information from Wikipedia: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Run the tool asynchronously."""
        # For simplicity, we'll just call the synchronous version
        return self._run(query) 