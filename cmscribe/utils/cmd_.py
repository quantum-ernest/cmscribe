"""Command-line interface utilities."""

import argparse
from typing import Any, Dict, Optional

from cmscribe.core import (CommitFormat, create_config, get_default_provider,
                           get_provider_config, update_config)
from cmscribe.providers import (AnthropicProvider, AzureOpenAIProvider,
                                GeminiProvider, HuggingFaceProvider,
                                OllamaProvider, OpenAIProvider)


def get_provider(provider_name: str, config: Dict[str, Any]):
    """Get the appropriate provider instance based on the provider name."""
    providers = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "huggingface": HuggingFaceProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
    }

    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}")

    return providers[provider_name](config)


def process_gen_command(args: argparse.Namespace) -> None:
    """Process the generate command."""
    # Get provider configuration
    provider_name = args.provider or get_default_provider()
    provider_config = get_provider_config(provider_name)

    # Create provider instance
    provider = fetch_provider(provider_name, provider_config)
    if not provider:
        print(f"Error: Invalid provider '{provider_name}'")
        return

    # Clear context if requested
    if args.clear_context:
        provider.clear_context()
        print("Context cache cleared.")

    # Get commit format
    commit_format = args.format or provider_config.get("commit_format", "conventional")
    try:
        commit_format = CommitFormat(commit_format)
    except ValueError:
        print(f"Error: Invalid commit format '{commit_format}'")
        return

    # Generate commit message
    try:
        message, err = provider.generate_commit_message(commit_format)
        if message:
            print("\nGenerated commit message:")
            print(message)

            if args.auto:
                # TODO: Implement auto-commit functionality
                print("\nAuto-commit functionality coming soon!")
        else:
            print("No commit message generated.")
            print(err)
    except Exception as e:
        print(f"Error generating commit message: {str(e)}")


def process_create_config() -> None:
    """Process the create config command."""
    create_config()
    print("Configuration file created with default settings.")


def process_update_config(args: argparse.Namespace, update_config_parser: argparse.ArgumentParser) -> None:
    """Process the update config command."""
    if not args.provider and not any(
        [
            args.format,
            args.auto_commit is not None,
            args.cache_responses is not None,
        ]
    ):
        print("Error: No settings to update. Please provide at least one setting.")
        update_config_parser.print_help()
        return

    update_config(
        provider=args.provider,
        api_key=args.api_key,
        endpoint=args.endpoint,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        commit_format=args.format,
        auto_commit=args.auto_commit,
        cache_responses=args.cache_responses,
        set_default=args.set_default,
    )

    if args.set_default and args.provider:
        print(f"Default provider set to: {args.provider}")
    print("Configuration updated successfully.")


def fetch_provider(provider_name: str, config: dict) -> Optional["AIProvider"]:
    """Create a provider instance based on the provider name."""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "azure_openai": AzureOpenAIProvider,
        "ollama": OllamaProvider,
        "huggingface": HuggingFaceProvider,
    }

    provider_class = providers.get(provider_name)
    if not provider_class:
        return None

    return provider_class(config)
