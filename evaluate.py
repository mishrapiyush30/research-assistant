#!/usr/bin/env python3
"""
Evaluation script for the Research Assistant Agent.

This script evaluates the agent on a set of predefined queries and measures its performance.
"""

import os
import json
import time
from dotenv import load_dotenv

from agent import create_research_agent


# Test queries with expected tool usage
TEST_QUERIES = [
    {
        "query": "Who is the CEO of Microsoft?",
        "expected_tools": ["WikipediaTool"],
    },
    {
        "query": "What is 15 squared plus 27?",
        "expected_tools": ["CalculatorTool"],
    },
    {
        "query": "What's the current weather in London?",
        "expected_tools": ["WeatherTool"],
    },
    {
        "query": "What was the population of Japan in 2020 divided by 100?",
        "expected_tools": ["WikipediaTool", "CalculatorTool"],
    },
    {
        "query": "If the distance from Los Angeles to New York is about 2,800 miles, how many kilometers is that?",
        "expected_tools": ["CalculatorTool"],
    },
    {
        "query": "What's the capital of France and what's the current temperature there?",
        "expected_tools": ["WikipediaTool", "WeatherTool"],
    },
    {
        "query": "What was the population of India in 2020 squared?",
        "expected_tools": ["WikipediaTool", "CalculatorTool"],
    },
    {
        "query": "What's the square root of the distance in kilometers between Tokyo and Seoul?",
        "expected_tools": ["WikipediaTool", "CalculatorTool"],
    },
    {
        "query": "Is it currently raining in Seattle?",
        "expected_tools": ["WeatherTool"],
    },
    {
        "query": "What's the current temperature in Celsius in New York and what's its population?",
        "expected_tools": ["WikipediaTool", "WeatherTool"],
    },
]


class ToolTracker:
    """Track which tools are called during agent execution."""
    
    def __init__(self):
        """Initialize the tool tracker."""
        self.called_tools = set()
    
    def track_tool(self, tool_name):
        """Track a tool call."""
        self.called_tools.add(tool_name)
    
    def get_called_tools(self):
        """Get the set of called tools."""
        return self.called_tools


def patch_tools_for_tracking(agent_executor, tracker):
    """Patch the tools to track which ones are called."""
    for tool in agent_executor.tools:
        original_run = tool._run
        
        def create_tracking_run(original_func, tool_name):
            def tracking_run(self, query):
                tracker.track_tool(tool_name)
                return original_func(query)
            return tracking_run
        
        tool._run = create_tracking_run(original_run, tool.name)


def evaluate_agent():
    """Evaluate the agent on the test queries."""
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in your environment or in a .env file.")
        return 1
    
    # Create the agent
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    print(f"Initializing Research Assistant Agent with model: {model_name}")
    agent_executor = create_research_agent(
        model_name=model_name,
        verbose=False
    )
    
    # Results
    results = []
    tool_usage_count = 0
    total_queries = len(TEST_QUERIES)
    total_time = 0
    
    # Run evaluation
    print(f"\nEvaluating agent on {total_queries} queries...\n")
    
    for i, test_case in enumerate(TEST_QUERIES):
        query = test_case["query"]
        expected_tools = test_case["expected_tools"]
        
        print(f"Query {i+1}/{total_queries}: {query}")
        
        # Create a new tool tracker for this query
        tracker = ToolTracker()
        patch_tools_for_tracking(agent_executor, tracker)
        
        # Execute the query
        start_time = time.time()
        response = agent_executor.invoke({"input": query})
        end_time = time.time()
        
        # Calculate metrics
        execution_time = end_time - start_time
        total_time += execution_time
        called_tools = tracker.get_called_tools()
        
        # Check if at least one tool was called
        used_tool = len(called_tools) > 0
        if used_tool:
            tool_usage_count += 1
        
        # Store results
        result = {
            "query": query,
            "expected_tools": expected_tools,
            "called_tools": list(called_tools),
            "used_expected_tools": all(tool in called_tools for tool in expected_tools),
            "used_tool": used_tool,
            "execution_time": execution_time,
            "answer": response["output"]
        }
        results.append(result)
        
        # Print results for this query
        print(f"  Tools called: {', '.join(called_tools)}")
        print(f"  Expected tools: {', '.join(expected_tools)}")
        print(f"  Used expected tools: {'Yes' if result['used_expected_tools'] else 'No'}")
        print(f"  Execution time: {execution_time:.2f} seconds")
        print(f"  Answer: {response['output'][:100]}..." if len(response["output"]) > 100 else f"  Answer: {response['output']}")
        print()
    
    # Calculate overall metrics
    exact_tool_matches = sum(1 for r in results if r["used_expected_tools"])
    tool_usage_percentage = (tool_usage_count / total_queries) * 100
    median_time = sorted([r["execution_time"] for r in results])[total_queries // 2]
    
    # Print summary
    print("\n===== EVALUATION SUMMARY =====")
    print(f"Total queries: {total_queries}")
    print(f"Exact tool matches: {exact_tool_matches}/{total_queries} ({exact_tool_matches/total_queries*100:.1f}%)")
    print(f"Queries with tool usage: {tool_usage_count}/{total_queries} ({tool_usage_percentage:.1f}%)")
    print(f"Median execution time: {median_time:.2f} seconds")
    print(f"Average execution time: {total_time/total_queries:.2f} seconds")
    
    # Save results to file
    with open("evaluation_results.json", "w") as f:
        json.dump({
            "results": results,
            "summary": {
                "total_queries": total_queries,
                "exact_tool_matches": exact_tool_matches,
                "exact_tool_match_percentage": exact_tool_matches/total_queries*100,
                "queries_with_tool_usage": tool_usage_count,
                "tool_usage_percentage": tool_usage_percentage,
                "median_execution_time": median_time,
                "average_execution_time": total_time/total_queries
            }
        }, f, indent=2)
    
    print("\nDetailed results saved to evaluation_results.json")
    
    return 0


if __name__ == "__main__":
    exit(evaluate_agent()) 