"""Calculator Tool for the Research Assistant Agent."""

from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from langchain.chains import LLMMathChain
from langchain_openai import ChatOpenAI
from pydantic import Field


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""
    
    name: str = "CalculatorTool"
    description: str = """
    Useful for performing mathematical calculations.
    Input should be a mathematical expression (e.g., "2 + 2", "5 * 10", "sqrt(16)", "log(100)").
    Use this when you need to compute a numerical result.
    """
    
    llm_math_chain: Any = Field(default=None, exclude=True)
    
    def __init__(self, llm=None):
        """Initialize the calculator tool with an LLM."""
        super().__init__()
        # Use the provided LLM or create a default one
        if llm is None:
            from os import getenv
            from dotenv import load_dotenv
            load_dotenv()
            model_name = getenv("MODEL_NAME", "gpt-3.5-turbo")
            llm = ChatOpenAI(model_name=model_name, temperature=0)
        
        self.llm_math_chain = LLMMathChain.from_llm(llm=llm)
    
    def _run(self, query: str) -> str:
        """Run the calculator with the provided expression."""
        try:
            result = self.llm_math_chain.invoke({"question": query})
            return result["answer"]
        except Exception as e:
            return f"Error performing calculation: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Run the calculator asynchronously."""
        try:
            result = await self.llm_math_chain.ainvoke({"question": query})
            return result["answer"]
        except Exception as e:
            return f"Error performing calculation: {str(e)}" 