"""Tests for the CalculatorTool."""

import pytest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the parent directory to the path so we can import the tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import CalculatorTool
from langchain_core.runnables.base import Runnable


class TestCalculatorTool:
    """Test suite for the CalculatorTool."""
    
    def test_init(self):
        """Test that the tool can be initialized."""
        # Create a proper mock that inherits from Runnable
        class MockLLM(Runnable):
            def invoke(self, input, config=None):
                return {"generations": [{"text": "4"}]}
        
        mock_llm = MockLLM()
        tool = CalculatorTool(llm=mock_llm)
        
        assert tool.name == "CalculatorTool"
        assert "mathematical calculations" in tool.description
        assert tool.llm_math_chain is not None
    
    @patch('langchain.chains.LLMMathChain.invoke')
    def test_run_success(self, mock_invoke):
        """Test successful execution of the tool."""
        # Create a proper mock that inherits from Runnable
        class MockLLM(Runnable):
            def invoke(self, input, config=None):
                return {"generations": [{"text": "4"}]}
        
        mock_llm = MockLLM()
        
        # Mock the LLMMathChain invoke method
        mock_invoke.return_value = {"answer": "4"}
        
        # Create the tool and run it
        tool = CalculatorTool(llm=mock_llm)
        result = tool._run("2 + 2")
        
        # Check the result
        assert result == "4"
        
        # Verify the mock was called correctly
        mock_invoke.assert_called_once_with({"question": "2 + 2"})
    
    @patch('langchain.chains.LLMMathChain.invoke')
    def test_run_error(self, mock_invoke):
        """Test execution when an error occurs."""
        # Create a proper mock that inherits from Runnable
        class MockLLM(Runnable):
            def invoke(self, input, config=None):
                return {"generations": [{"text": "4"}]}
        
        mock_llm = MockLLM()
        
        # Mock the LLMMathChain invoke method to raise an exception
        mock_invoke.side_effect = Exception("Invalid expression")
        
        # Create the tool and run it
        tool = CalculatorTool(llm=mock_llm)
        result = tool._run("invalid / expression")
        
        # Check the result
        assert "Error performing calculation" in result
        assert "Invalid expression" in result
        
        # Verify the mock was called correctly
        mock_invoke.assert_called_once_with({"question": "invalid / expression"}) 