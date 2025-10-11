import os
from instructor.core.exceptions import ConfigurationError, InstructorRetryException

from po_ai_buddy.ai import AI
from po_ai_buddy.config import Config 



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
    def __init__(self, config: Config, ai: AI):
        super().__init__()
        self.ai_instance = None
        self.config = config
        self.ai = ai
        self.indicator = self.config.get("indicator") + " " if len(self.config.get("indicator")) > 0 else ""
        self.client = None
        self.previous_msg = None


    def repl(self):  
        while True:
            if not self.previous_msg is None:
                user_input = self.previous_msg
            else:
                user_input = input(self.indicator).strip()
            
            if user_input.lower() in ("q", "quit", "exit"):
                print("Thanks for Using :)")
                exit(0)

            elif user_input.startswith("@") or self.previous_msg:  
                if user_input.startswith("@"):
                    self.alias = user_input.split(" ")[0][1:]
                    user_input = user_input.removeprefix("@"+self.alias)

                    _alias, self.provider = self.config.get_alias_and_provider(self.alias)
                    if _alias is None:
                        print(f"Model '{self.alias}' not found in config.")
                        raise Exception("Neither mentioned model found nor Default Model. Please check config file!")           
                    else:
                        self.alias = _alias

                    if not self.provider:
                        msg = f"Provider '{self.provider}' for alias '{self.alias}' don't exists"
                        raise Exception(msg)
                
                try:
                    self.client = self.ai.create_client(self.provider)
                    
                    ai_response = self.ai.process_input(self.client, user_input)
                    print(f"AI: {ai_response.output}")      # Don't Touch, actual output

                    if ai_response.cmd:
                        print(f"    CMD: {ai_response.cmd}")    # Don't Touch, actual output
                        confirm = input("Run[y] abort[n] [type more]: ").strip()
                        if confirm.lower() == "y":
                            self.ai.reset_context()
                            self.previous_msg = None
                            print(f"{self.indicator}{ai_response.cmd}")      # Don't Touch, actual output. Illusion to user
                            self.run_cmd(ai_response.cmd)
                            continue
                    else:
                        confirm = input("abort[n] [type more]: ").strip()

                    if confirm.lower() == "n":
                        self.ai.reset_context()
                        self.previous_msg = None
                    else:
                        self.previous_msg = confirm

                except ConfigurationError as e:
                    print(f"Provider '{self.provider}' might not be configured correctly or un-supported.\nSee below")
                    print(e)

                except ImportError as e:
                    print(f"Provider '{self.provider}' might need install.\nSee below")
                    print(e)
                
                except InstructorRetryException as e:
                    print(f"AI model failed to generate a valid response for provider '{self.provider}'. \n- Please try a different model or rephrase your query.\n- Check your API have access to that specific model?")
                    print(f"Details: {e}")
                    self.ai.reset_context()
                    self.previous_msg = None

                except ValueError as e:
                    print(f"Provider '{self.provider}' might be wrong configured/un-supported.\nSee below")
                    print(e)

                except Exception as e:
                    # Check for authentication-related errors by examining error message
                    error_msg = str(e).lower()
                    if any(keyword in error_msg for keyword in ['api_key', 'api key', 'authentication', 'unauthorized', 'credential', 'token', 'environment', 'environment variable', "error initializing", "client"]):
                        print(f"Maybe Authentication Error for provider, make sure to check:")
                        print(f"  - API key is missing, invalid, doesn't have the scope of specified model")
                        print(f"  - Check the environment variable, spelling mistake, wrong key, scope (e.g user-specific)")
                        print(f"  - Verify your config")
                        print(f"Details: {e}")
                        self.ai.reset_context()
                        self.previous_msg = None
                        continue

                    print(f"An error occurred:\nSee below:{e}")
                    print("Try re-running the program again.")

            else:   
                self.run_cmd(user_input)


    def __enter__(self):
        """Enter AI conversation mode"""
        self.ai.start_context()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        """Exit AI conversation mode"""
        if self.ai:
            self.ai.end_context()
        self.ai = None

