import argparse

from .ai import AI
from .config import Config
from .terminal import SmartTerminal
from . import __version__



def handle_config_command(args: argparse.Namespace, config: Config) -> None:
    """Handle --config subcommands"""
    match args.config_action:
        case 'show':
            print(f"Config loaded from: {config.config_path}")
            print(f"Is project config: {config.is_project_config()}")
            print(f"Is global config: {config.is_global_config()}")

        case 'set':
            if not args.key or not args.value:
                print("Error: --config set requires --key and --value")
                return
            config.set(args.key, args.value)
            print(f"Set {args.key} = {args.value}")
    
        case 'get':
            if not args.key:
                print("Error: --config get requires --key")
                return
            value = config.get(args.key)
            print(f"{args.key}: {value}")
    
        case 'path':
            print(f"Config file location: {config.config_path}")

        case _:
            print("No flag passed, read the documentation please.")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(description='AI Powered Terminal')
    
    # Add version argument
    parser.add_argument('--version', action='version', 
                       version=f'po-ai-buddy {__version__}',
                       help="Shows the version of the tool in `po-ai-buddy <version>` format.")
    
    # Config subcommand
    parser.add_argument('--config', dest='config_action', 
                       choices=['show', 'set', 'get', 'path'],
                       help='Config operations: show, set, get, path')
    
    # Additional arguments for config set/get
    parser.add_argument('--key', help='Config key for set/get operations')
    parser.add_argument('--value', help='Config value for set operation')
    
    # Regular query (when no flags)
    parser.add_argument('query', nargs='*', help='AI query or command')
    
    return parser


def main() -> None:
    config = Config()
    ai = AI()
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle config commands
    if args.config_action:
        handle_config_command(args, config)
        return
    
    with SmartTerminal(config, ai) as smart:
        # Quick Start
        if args.query:
            query = ' '.join(args.query)
            smart.repl(quick_start=True, quick_input=query)
        
        # Invoke
        else:
            smart.repl()



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

