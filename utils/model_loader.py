import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI



class ConfigLoader:

    def __init__(self):
        load_dotenv()
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")

        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in .env file.")
        
            # Debugging only partial API key for safety
            print(f"Using GROQ_API_KEY: {groq_api_key[:6]}******")

            # Read model name directly from config.yaml
            model_name = self.config["llm"]["model_name"]

            # Initialize ChatGroq with recommended parameters
            llm = ChatGroq(
                model=model_name,          # must be 'model' not 'model_name'
                api_key=groq_api_key,
                temperature=0.0,           # deterministic responses for planning
                max_retries=2,             # retry on transient errors
                max_tokens=None,           # can set a limit if needed
                reasoning_format="parsed"  # optional; use 'raw' if parsing fails
            )

            return llm

    
    # def load_llm(self):
    #     """
    #     Load and return the LLM model.
    #     """
    #     print("LLM loading...")
    #     print(f"Loading model from provider: {self.model_provider}")
    #     if self.model_provider == "groq":
    #         print("Loading LLM from Groq..............")
    #         groq_api_key = os.getenv("GROQ_API_KEY")
    #         if not groq_api_key:
    #             raise ValueError("GROQ_API_KEY not found in .env file.")
    #         print(f"Using GROQ_API_KEY: {groq_api_key[:6]}******")  # Debug (partial key)
    #         model_name = self.config["llm"]["groq"]["model_name"]
    #         llm = ChatGroq(model_name=model_name, api_key=groq_api_key)
        
    #         return llm
