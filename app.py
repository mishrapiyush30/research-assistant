#!/usr/bin/env python3
"""
Streamlit web interface for the Research Assistant Agent.
"""

import os
import time
import streamlit as st
from dotenv import load_dotenv

from agent import create_research_agent


def initialize():
    """Initialize the Streamlit app."""
    # Set page config
    st.set_page_config(
        page_title="Research Assistant Agent",
        page_icon="🔍",
        layout="wide",
    )
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Error: OPENAI_API_KEY environment variable not set.")
        st.info("Please set it in your environment or in a .env file.")
        st.stop()
    
    # Create the agent if it doesn't exist in session state
    if "agent" not in st.session_state:
        with st.spinner("Initializing Research Assistant Agent..."):
            model_name = os.getenv("MODEL_NAME", "gpt-4o")
            st.session_state.agent = create_research_agent(
                model_name=model_name,
                verbose=False
            )
            st.session_state.model_name = model_name
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    """Display the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """Run the Streamlit app."""
    # Initialize the app
    initialize()
    
    # Display header
    st.title("🔍 Research Assistant Agent")
    st.markdown(f"Powered by {st.session_state.model_name}")
    
    # Display chat history
    display_chat_history()
    
    # Get user input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                start_time = time.time()
                response = st.session_state.agent.invoke({"input": prompt})
                end_time = time.time()
                
                answer = response["output"]
                execution_time = end_time - start_time
                
                message_placeholder.markdown(answer)
                st.caption(f"Response time: {execution_time:.2f} seconds")
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                message_placeholder.markdown(f"Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
    
    # Display sidebar with info
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This Research Assistant Agent can answer complex questions by using external tools:
        
        - **WikipediaTool**: Lookup information on Wikipedia
        - **CalculatorTool**: Perform mathematical calculations
        - **WeatherTool**: Get current weather conditions
        
        The agent decides which tools to use based on your question.
        """)
        
        st.header("Examples")
        examples = [
            "Who is the current CEO of Apple?",
            "What is the square root of 144 divided by 3?",
            "What's the current weather in Tokyo?",
            "What was France's 2020 population squared?",
            "Distance from NYC to Paris in miles divided by 3",
        ]
        
        for example in examples:
            if st.button(example):
                # Clear input and add example as user message
                st.session_state.messages.append({"role": "user", "content": example})
                st.rerun()
        
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main() 