from typing import List, Dict, Optional
from instructor.core.exceptions import ConfigurationError

import instructor
from pydantic import BaseModel, Field



class AIResponse(BaseModel):
    """Pydantic model for the AI's JSON response."""
    output: str
    cmd: str = Field(default="")

    def __str__(self):
        return f"Output: {self.output} \n CMD: {self.cmd}"


CMD = [
    {"push karo": "git push origin main"},
    {"pull karo": "git pull origin main"},
    {"tag push karo": "git push origin --tags"},
]

  

class AI:
    def __init__(self):
        self.context_memory: List[Dict[str, str]] = []

    def get_prompt(self):
                return f"""
You are a helpful terminal assistant. Your goal is to understand the user's request and provide a concise natural language response and, if applicable, a shell command to execute.

Use the `AIResponse` tool to format your answer.

The user's request is:
{self.get_context_history(mark_current_input=True)}
"""

    def create_client(self, provider: str, api_key: str | None = None):
        """Creates an instructor client for the given provider."""
        try:
            # If an API key is provided, use it. Otherwise, instructor will
            # look for environment variables.
            if api_key:
                return instructor.from_provider(provider, api_key=api_key)
            else:
                return instructor.from_provider(provider)
        except (ValueError, ImportError, ConfigurationError) as e:
            raise


    def start_context(self) -> None:
        """Start a new context session"""
        self.context_memory = []

    def reset_context(self) -> None:
        """Reset exisiting context session"""
        self.context_memory = []

    def end_context(self) -> None:
        """End the current context session"""
        self.context_memory = []

    def add_to_context(self, origin: str, content: str):
        """Add a message to the context"""
        self.context_memory.append({
            "origin": origin,
            "content": content
        })


    def get_context_history(self, mark_current_input: bool = False) -> str:
        """Get formatted context history"""
        if not self.context_memory:
            return ""
        
        history = []
        last = len(self.context_memory) - 1 if len(self.context_memory) > 0 else 0
        for i, msg in enumerate(self.context_memory):
            if mark_current_input and i < last:
                history.append(f"{msg['origin']}: {msg['content']}")
            else:
                history.append(f"Current Input({msg['origin']}): {msg['content']}")
        return "\n".join(history)


    def process_input(self, client, query: str) -> AIResponse:
        """Process user query and return response"""        
        self.add_to_context("Human", query)
        response = self.generate_response(client)
        self.add_to_context("AI", str(response))
        return response


    def generate_response(self, client) -> str:
        """Generate AI response based on query and context"""
        ai_output_obj = client.chat.completions.create(
            response_model=AIResponse,
            messages=[{"role": "user", "content": self.get_prompt()}],
        )
        return ai_output_obj

    def parse_ai_output(self, ai_output: str) -> Optional[Dict[str, str]]:
        """Parse AI output to extract command and output"""
        try:
            import json
            data = json.loads(ai_output)
            if "output" in data and "cmd" in data:
                return (data, True)
            else:
                return (ai_output, False)
        except json.JSONDecodeError:
            return (ai_output, False)
        






