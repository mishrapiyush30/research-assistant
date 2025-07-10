#!/usr/bin/env python3
"""
Research Assistant Agent CLI.

This script provides a command-line interface for interacting with the Research Assistant Agent.
"""

import os
import time
import argparse
from dotenv import load_dotenv

from agent import create_research_agent


def main():
    """Run the Research Assistant Agent CLI."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Research Assistant Agent CLI")
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "gpt-4o"),
        help="The OpenAI model to use (default: from .env or gpt-4o)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=os.getenv("VERBOSE", "false").lower() == "true",
        help="Enable verbose output (default: from .env or false)"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to run (if not provided, interactive mode is used)"
    )
    args = parser.parse_args()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in your environment or in a .env file.")
        return 1
    
    # Create the agent
    print(f"Initializing Research Assistant Agent with model: {args.model}")
    agent_executor = create_research_agent(
        model_name=args.model,
        verbose=args.verbose
    )
    
    # Single query mode
    if args.query:
        start_time = time.time()
        response = agent_executor.invoke({"input": args.query})
        end_time = time.time()
        
        print("\nFinal Answer:", response["output"])
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return 0
    
    # Interactive mode
    print("\nResearch Assistant Agent ready! Type 'exit' or 'quit' to end the session.")
    print("Ask a question to get started...\n")
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        if not query.strip():
            continue
        
        try:
            start_time = time.time()
            response = agent_executor.invoke({"input": query})
            end_time = time.time()
            
            print("\nFinal Answer:", response["output"])
            print(f"Time taken: {end_time - start_time:.2f} seconds")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    return 0


if __name__ == "__main__":
    exit(main()) 