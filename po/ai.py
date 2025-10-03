from typing import List, Dict, Optional
import json 
import os
'''
Able to 
Start a session
A: Take Input # Add to context(Human)
B: Give Output # Add to Context(AI)
C: Either end of Keep continuing BUT with context
End a session

Context Memory:
[
    {AI: ""} 
    {Human: ""} 
]

take_human_input ---+
    |               |
    V               |
Give to AI          |
    L_______________|


'''

'''

Make sure to give valid JSON obj if 
{
    "output": "<your-output-here>"
    "cmd": ""
}
'''

CMD = [
            {"push karo": "git push origin main"},
            {"pull karo": "git pull origin main"},
            {"tag push karo": "git push origin --tags"},
        ]


AI_IDENTIFIER = "/ai"
user_input="wOW"
is_context = True
PROMPT=f"""
ROLE:
You are a helpful terminal assistant. You can understand every commands.
You always answer very briefly and to the point.

INPUT:
{f"History: " is is_context}
Current input: {user_input}


OUTPUT FORMAT:
You ALWAYS give output in JSON format following this format:
{
    "output": "<your-output-here>",
    "cmd": "<command-to-execute-if-any>"
}
output: Should be a brief description of what you understood from the query.
cmd: If user have asked about a command, write it there or leave it empty.
"""

class AI:
    def __init__(self):
        self.context_memory: List[Dict[str, str]] = []
        self.is_context_active = False


    def start_context(self):
        """Start a new context session"""
        self.is_context_active = True
        self.context_memory = []


    def end_context(self):
        """End the current context session"""
        self.is_context_active = False
        self.context_memory = []


    def add_to_context(self, origin: str, content: str):
        """Add a message to the context"""
        if self.is_context_active:
            if 
            self.context_memory.append({
                "origin": origin,
                "content": content
            })


    def get_context_history(self) -> str:
        """Get formatted context history"""
        if not self.context_memory:
            return None
            # return "No context history"
        
        history = []
        for msg in self.context_memory:
            history.append(f"{msg['origin']}: {msg['content']}")
        return "\n".join(history)


    def process_input(self, query: str) -> str:
        """Process user query and return response"""
        # Remove AI identifier
        query = query.removeprefix(AI_IDENTIFIER).strip()
        
        # Add user input to context
        self.add_to_context("Human", query)

        # Generate AI response (placeholder for now)
        response = self.generate_response(query)

        # Add AI response to context
        self.add_to_context("AI", response)
           
        return response

    def generate_response(self, query: str) -> str:
        """Generate AI response based on query and context"""
        # for cmd in CMD:
        #     cmd_key = list(cmd.keys())[0]
        #     if cmd_key in query.lower:
        #         return f"Command: {cmd[cmd_key]}"

        try:
            ai_response = 
        ai_output = self.parse_ai_output(ai_response) if ai_response else None
        if ai_output is None:
            return f"AI didnt return valid JSON. Here is the response: \n{ai_response}"

        return ai_output"


    def parse_ai_output(self, ai_output: str) -> Optional[Dict[str, str]] | :
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
        






class Terminal:
    def __init__(self):
        self.cwd = os.getcwd()

    def run_cmd(self, cmd: str) -> str:
        try:
            output = os.system(cmd)
        except Exception as e:
            output = e
        return output
    

class SmartTerminal(Terminal):
    def __init__(self):
        super().__init__()
        self.ai_instance: AI = None
        self.in_ai_mode = False

    def repl(self):
        while True:
            # Show different prompt based on mode
            prompt_symbol = "$ (AI) " if self.in_ai_mode else "$ "
            user_input = input(prompt_symbol)
            
            if user_input.lower() in ("q", "quit", "exit"):
                print("Thanks for Using :)")
                exit(0)
            
            # Handle AI mode commands
            if self.in_ai_mode:
                if user_input.lower() == "ok":
                    print("Context accepted and cleared")
                    self.exit_ai_mode()
                    continue
                elif user_input.lower() == "discard":
                    print("Context discarded")
                    self.exit_ai_mode()
                    continue
                elif user_input.lower() == "history":
                    print("\n--- Context History ---")
                    print(self.ai_instance.get_context_history())
                    print("----------------------\n")
                    continue
                else:
                    # Continue conversation in AI mode
                    response = self.ai_instance.process_input(f"/ai {user_input}")
                    print(f"AI: {response}")
                    continue
            
            # Start AI mode
            if user_input.startswith(AI_IDENTIFIER):
                print("🤖 AI Mode Started (Type 'ok' to accept, 'discard' to cancel, 'history' to view context)")
                self.enter_ai_mode()
                response = self.ai_instance.process_input(user_input)
                print(f"AI: {response}")
                continue

            # Normal command execution
            self.run_cmd(user_input)

    def __enter__(self):
        """Enter AI conversation mode"""
        self.in_ai_mode = True
        self.ai_instance = AI()
        self.ai_instance.start_context()

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit AI conversation mode"""
        self.in_ai_mode = False
        if self.ai_instance:
            self.ai_instance.end_context()
        self.ai_instance = None

