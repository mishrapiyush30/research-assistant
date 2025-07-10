# Research Assistant Agent

A powerful research assistant that can answer complex questions by using multiple external tools. The agent uses LangChain's ReAct framework to intelligently select and use appropriate tools based on the query.

![Research Assistant Screenshot](docs/screenshot.png)

## Features

- **Multiple Tools**:
  - **WikipediaTool**: Lookup information on Wikipedia
  - **CalculatorTool**: Perform mathematical calculations
  - **WeatherTool**: Get current weather conditions

- **Smart Tool Selection**: Agent automatically decides which tools to use based on your question
- **Conversation Memory**: Maintains context across multiple queries
- **User-Friendly Interface**: Clean Streamlit web interface

## Technical Stack

- LangChain for agent orchestration
- OpenAI GPT-4 for reasoning
- Streamlit for web interface
- Python 3.8+

## Project Structure

```
research-assistant/
├── agent/
│   ├── __init__.py
│   └── agent.py
├── tools/
│   ├── __init__.py
│   ├── calculator_tool.py
│   ├── weather_tool.py
│   └── wikipedia_tool.py
├── tests/
├── app.py
├── main.py
└── requirements.txt
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   OPENAI_API_KEY=your_api_key
   MODEL_NAME=gpt-4  # or other OpenAI model
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your question in the input field
2. The agent will:
   - Analyze your question
   - Select appropriate tools
   - Execute tools to gather information
   - Synthesize a comprehensive answer

## Example Queries

- "Who is the current CEO of Apple?"
- "What is the square root of 144 divided by 3?"
- "What's the current weather in Tokyo?"
- "What was France's 2020 population squared?"
- "Distance from NYC to Paris in miles divided by 3" 