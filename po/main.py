import argparse
import sys
from po.config import Config


def handle_config_command(args, config):
    """Handle --config subcommands"""
    if args.config_action == 'show':
        print(f"Config loaded from: {config.config_path}")
        print(f"Is project config: {config.is_project_config()}")
        print(f"Is global config: {config.is_global_config()}")

    
    # elif args.config_action == 'set':
    #     if not args.key or not args.value:
    #         print("Error: --config set requires --key and --value")
    #         return
    #     config.set(args.key, args.value)
    #     print(f"Set {args.key} = {args.value}")
    
    # elif args.config_action == 'get':
    #     if not args.key:
    #         print("Error: --config get requires --key")
    #         return
    #     value = config.get(args.key)
    #     print(f"{args.key}: {value}")
    
    # elif args.config_action == 'path':
    #     print(f"Config file location: {config.config_path}")

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
        # Your existing AI logic here
        return
    
    # No arguments - start interactive mode
    print("Starting AI Terminal...")
    # Your existing REPL logic here

if __name__ == "__main__":
    main()