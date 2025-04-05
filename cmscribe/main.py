"""Main entry point for the application."""

import argparse
import json

from cmscribe.core import CacheManager, get_default_provider
from cmscribe.utils import (process_create_config, process_gen_command,
                            process_update_config)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI-powered commit message generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser("gen", help="Generate a commit message")
    gen_parser.add_argument(
        "--provider","-p",
        help="AI provider to use (overrides default)",
        choices=[
            "openai",
            "anthropic",
            "gemini",
            "azure_openai",
            "ollama",
            "huggingface",
        ],
    )
    gen_parser.add_argument(
        "--format", "-f",
        help="Commit message format",
        choices=["conventional", "semantic", "simple", "angular"],
    )
    gen_parser.add_argument(
        "--auto", "-a",
        action="store_true",
        help="Automatically commit after generating message",
    )
    gen_parser.add_argument(
        "--clear-context", "-cc",
        action="store_true",
        help="Clear context cache before generation",
    )

    # Config commands
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Config commands"
    )

    # Create config
    create_parser = config_subparsers.add_parser(
        "create", help="Create new configuration"
    )

    # Update config
    update_parser = config_subparsers.add_parser("update", help="Update configuration")
    update_parser.add_argument(
        "--provider", "-p",
        help="AI provider to configure",
        choices=[
            "openai",
            "anthropic",
            "gemini",
            "azure_openai",
            "ollama",
            "huggingface",
        ],
    )
    update_parser.add_argument(
        "--api-key", "-a",
        help="API key for the provider",
    )
    update_parser.add_argument(
        "--endpoint", "-e",
        help="API endpoint for the provider",
    )
    update_parser.add_argument(
        "--model", "-m",
        help="Model to use with the provider",
    )
    update_parser.add_argument(
        "--max-tokens", "-mt",
        type=int,
        help="Maximum tokens for generation",
    )
    update_parser.add_argument(
        "--temperature", "-t",
        type=float,
        help="Temperature for generation",
    )
    update_parser.add_argument(
        "--format", "-f",
        help="Default commit message format",
        choices=["conventional", "semantic", "simple", "angular"],
    )
    update_parser.add_argument(
        "--auto-commit", "-ac",
        type=bool,
        help="Enable/disable auto-commit",
    )
    update_parser.add_argument(
        "--cache-responses", "-cr",
        type=bool,
        help="Enable/disable response caching",
    )
    update_parser.add_argument(
        "--set-default", "-sd",
        action="store_true",
        help="Set the specified provider as default",
    )

    # Show config
    show_parser = config_subparsers.add_parser(
        "show", help="Show current configuration"
    )

    # Cache commands
    cache_parser = subparsers.add_parser("cache", help="Cache management")
    cache_subparsers = cache_parser.add_subparsers(
        dest="cache_command", help="Cache commands"
    )

    # Clear cache
    clear_parser = cache_subparsers.add_parser("clear", help="Clear cache")
    clear_parser.add_argument(
        "--provider", "-p",
        help="Provider to clear cache for",
        choices=[
            "openai",
            "anthropic",
            "gemini",
            "azure_openai",
            "ollama",
            "huggingface",
        ],
    )
    clear_parser.add_argument(
        "--model", "-m",
        help="Model to clear cache for",
    )
    clear_parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Clear all caches",
    )

    args = parser.parse_args()

    if args.command == "gen":
        process_gen_command(args)
    elif args.command == "config":
        if args.config_command == "create":
            process_create_config()
        elif args.config_command == "update":
            process_update_config(args)
        elif args.config_command == "show":
            from cmscribe.core import load_config
            config = load_config()
            print("\nCurrent Configuration:")
            print("\nCore Settings:")
            for key, value in config["Core"].items():
                print(f"  {key}: {value}")

            print("\nProvider Settings:")
            for section in config.sections():
                if section != "Core":
                    print(f"\n{section}:")
                    for key, value in config[section].items():
                        if key != "api_key":  # Don't show API keys
                            print(f"  {key}: {value}")

            print(f"\nDefault Provider: {get_default_provider()}")
    elif args.command == "cache":
        cache_manager = CacheManager()
        if args.cache_command == "clear":
            if args.all:
                cache_manager.clear_all_contexts()
                print("All caches cleared.")
            elif args.provider:
                from cmscribe.utils import get_repo_name
                repo_name = get_repo_name()
                if args.model:
                    cache_manager.clear_context(repo_name, args.provider, args.model)
                    print(
                        f"Cache cleared for {args.provider} ({args.model}) in current repository."
                    )
                else:
                    for cache_file in cache_manager.cache_dir.glob("*.json"):
                        try:
                            with open(cache_file, "r") as f:
                                data = json.load(f)
                                if data.get("provider") == args.provider:
                                    cache_file.unlink()
                        except (json.JSONDecodeError, IOError):
                            continue
                    print(f"All caches cleared for {args.provider}.")
            else:
                print("Please specify --provider or --all to clear caches.")


if __name__ == "__main__":
    main()
