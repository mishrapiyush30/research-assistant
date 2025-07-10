"""Research Assistant Agent implementation."""

from typing import List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from tools import WikipediaTool, CalculatorTool, WeatherTool


def get_prompt_template() -> str:
    """Get the prompt template for the research assistant agent."""
    return """You are an advanced Research Assistant Agent that can answer complex questions by using external tools.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Previous conversation history:
{chat_history}

Question: {input}
{agent_scratchpad}"""


def create_research_agent(
    model_name: str = "gpt-4o",
    temperature: float = 0,
    verbose: bool = False,
    memory: Optional[ConversationBufferMemory] = None
) -> AgentExecutor:
    """Create a research assistant agent with the specified tools and model.
    
    Args:
        model_name: The name of the OpenAI model to use
        temperature: The temperature parameter for the model
        verbose: Whether to enable verbose output
        memory: Optional conversation memory to use
        
    Returns:
        An AgentExecutor instance
    """
    # Initialize the LLM
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    
    # Initialize tools
    tools = [
        WikipediaTool(),
        CalculatorTool(llm=llm),
        WeatherTool()
    ]
    
    # Create prompt
    prompt = PromptTemplate.from_template(
        template=get_prompt_template(),
        partial_variables={"tools": ""}  # Will be filled by the agent
    )
    
    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create memory if not provided
    if memory is None:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10,
    )
    
    return agent_executor 