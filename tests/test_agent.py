"""Tests for the Research Assistant Agent."""

import pytest
import os
from unittest.mock import patch, MagicMock, PropertyMock

import sys

# Add the parent directory to the path so we can import the agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import create_research_agent
from langchain_core.runnables.base import Runnable
from langchain.tools import BaseTool


class TestAgent:
    """Test suite for the Research Assistant Agent."""
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-dummy-key-for-testing"})
    @patch('agent.agent.ChatOpenAI')
    @patch('agent.agent.WikipediaTool')
    @patch('agent.agent.CalculatorTool')
    @patch('agent.agent.WeatherTool')
    @patch('agent.agent.create_react_agent')
    @patch('agent.agent.AgentExecutor')
    def test_create_agent(self, mock_agent_executor, mock_create_agent, 
                         mock_weather_tool, mock_calculator_tool, 
                         mock_wikipedia_tool, mock_chat_openai):
        """Test that the agent can be created."""
        # Create a proper mock that inherits from Runnable
        class MockLLM(Runnable):
            def invoke(self, input, config=None):
                return {"generations": [{"text": "response"}]}
        
        mock_llm_instance = MockLLM()
        mock_chat_openai.return_value = mock_llm_instance
        
        # Create real tool instances instead of mocks
        class MockWikipediaTool(BaseTool):
            name: str = "WikipediaTool"
            description: str = "Mock Wikipedia Tool"
            
            def _run(self, query: str) -> str:
                return "Mock Wikipedia result"
                
            async def _arun(self, query: str) -> str:
                return "Mock Wikipedia result"
        
        class MockCalculatorTool(BaseTool):
            name: str = "CalculatorTool"
            description: str = "Mock Calculator Tool"
            
            def _run(self, query: str) -> str:
                return "Mock Calculator result"
                
            async def _arun(self, query: str) -> str:
                return "Mock Calculator result"
        
        class MockWeatherTool(BaseTool):
            name: str = "WeatherTool"
            description: str = "Mock Weather Tool"
            
            def _run(self, query: str) -> str:
                return "Mock Weather result"
                
            async def _arun(self, query: str) -> str:
                return "Mock Weather result"
        
        # Set up the tool mocks to return our real tool instances
        mock_wikipedia_tool_instance = MockWikipediaTool()
        mock_calculator_tool_instance = MockCalculatorTool()
        mock_weather_tool_instance = MockWeatherTool()
        
        mock_wikipedia_tool.return_value = mock_wikipedia_tool_instance
        mock_calculator_tool.return_value = mock_calculator_tool_instance
        mock_weather_tool.return_value = mock_weather_tool_instance
        
        # Mock the agent
        mock_agent_instance = MagicMock()
        mock_create_agent.return_value = mock_agent_instance
        
        # Mock the agent executor
        mock_agent_executor_instance = MagicMock()
        mock_agent_executor.return_value = mock_agent_executor_instance
        
        # Call the function
        agent = create_research_agent(model_name="gpt-4o", verbose=True)
        
        # Verify the mocks were called correctly
        mock_chat_openai.assert_called_once_with(model_name="gpt-4o", temperature=0)
        mock_wikipedia_tool.assert_called_once()
        mock_calculator_tool.assert_called_once_with(llm=mock_llm_instance)
        mock_weather_tool.assert_called_once()
        
        # Check that create_react_agent was called with the right parameters
        mock_create_agent.assert_called_once()
        args, kwargs = mock_create_agent.call_args
        assert kwargs["llm"] == mock_llm_instance
        assert len(kwargs["tools"]) == 3
        assert kwargs["tools"][0] == mock_wikipedia_tool_instance
        assert kwargs["tools"][1] == mock_calculator_tool_instance
        assert kwargs["tools"][2] == mock_weather_tool_instance
        
        # Check that AgentExecutor was called with the right parameters
        mock_agent_executor.assert_called_once()
        args, kwargs = mock_agent_executor.call_args
        assert kwargs["agent"] == mock_agent_instance
        assert len(kwargs["tools"]) == 3
        assert kwargs["verbose"] == True
        
        # Check that the function returns the agent executor
        assert agent == mock_agent_executor_instance 