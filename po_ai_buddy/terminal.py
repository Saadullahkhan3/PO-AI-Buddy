import os

from po_ai_buddy.ai import AI
from po_ai_buddy.config import Config 

'''
Since I wanto to allow user to switch betwwen models, so it can't be in AI class
if self.ai_identifier:
    query = query.removeprefix(self.ai_identifier).strip()
'''

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
    def __init__(self, config: Config):
        super().__init__()
        self.ai_instance = None
        self.in_ai_mode = False
        self.config = config
        self.ai: AI = AI()
        self.indicator = self.config.get("indicator") + " " if len(self.config.get("indicator")) > 0 else ""

    def define_model(self):
        self.aliases = [m["alias"] for m in self.config.get("models")]
        self.providers = [m["provider"] for m in self.config.get("models")]

    def repl(self):
        # If context removed,
        # self.ai.start_context() if self.ai.context_memory == [] else None
        previous_msg = None
        while True:
            if not previous_msg is None:
                user_input = confirm
            else:
                user_input = input(self.indicator)
            
            # Quit
            if user_input.lower() in ("q", "quit", "exit"):
                print("Thanks for Using :)")
                exit(0)

            # Model mention
            elif user_input.startswith("@"):
                alias = user_input.split(" ")[0]
                user_input = user_input.removeprefix(alias)

                if not self.config.alias_exists(alias):
                    print(f"Model '{alias}' not found in config.")
                    alias = self.config.get('default_model')
                    if alias is None:
                        raise Exception("Neither mentioned model found nor Default Model. Please check config file!")           
                    print(f"Fallback to default model '{alias}'") 

                provider = self.config.provider_for_alias(alias)
                if provider is None:
                    msg = f"Provider for alias '{alias}' don't exists"
                    raise Exception(msg)
                
                try:
                    client = self.ai.create_client(provider)

                except Exception as e:
                    print(f"Provider '{provider}' might be wrong configured/un-supported or not installed.\nSee below")
                    print(e)

                ai_response = self.ai.process_input(client, user_input)
                print(f"AI: {ai_response.output}")
                if ai_response.cmd:
                    print(f"CMD: {ai_response.cmd}")
                    confirm = input("Run CMD? (y/n/type more): ").strip()
                    if confirm.lower() == "y":
                        self.run_cmd(user_input)
                    elif confirm.lower() == "n":
                        self.ai.end_context()
                        print("Context Ended!")
                    # Move to next iteration
                    else:
                        previous_msg = confirm

            # Normal command execution
            self.run_cmd(user_input)

    def __enter__(self):
        """Enter AI conversation mode"""
        # self.ai_instance = AI()
        self.ai.start_context()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit AI conversation mode"""
        if self.ai:
            self.ai.end_context()
        self.ai = None

