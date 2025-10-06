import argparse

from po_ai_buddy.ai import AI
from .config import Config
from .terminal import SmartTerminal



def handle_config_command(args, config):
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


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(description='AI Powered Terminal')
    
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


def main():
    config = Config()
    ai = AI()
    from pprint import pprint
    pprint(config.__dict__)
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle config commands
    if args.config_action:
        handle_config_command(args, config)
        return
    
    # Handle regular queries
    if args.query:
        query = ' '.join(args.query)
        print(f"Processing query: {query}")
        return
    
    with SmartTerminal(config, ai) as smart:
        smart.repl()



if __name__ == "__main__":
    main()