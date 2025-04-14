# config.py
import configparser
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Cross-platform config dir
CONFIG_DIR = Path.home() / (".config" if os.name != "nt" else "AppDataRoaming") / "cmscribe"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "config.ini"

# Provider-specific default settings
PROVIDER_DEFAULTS = {
    "openai": {
        "model": "gpt-3.5-turbo",
        "endpoint": "https://api.openai.com/v1",
        "max_tokens": 50,
        "temperature": 0.7,
    },
    "ollama": {
        "model": "llama2",
        "endpoint": "http://localhost:11434",
        "max_tokens": 50,
        "temperature": 0.7,
    },
    "huggingface": {
        "model": "distilgpt2",
        "endpoint": "https://api-inference.huggingface.co/models",
        "max_tokens": 50,
        "temperature": 0.7,
    },
    "anthropic": {
        "model": "claude-3-sonnet-20240229",
        "endpoint": "https://api.anthropic.com",
        "max_tokens": 50,
        "temperature": 0.7,
    },
    "gemini": {
        "model": "gemini-pro",
        "endpoint": "https://generativelanguage.googleapis.com/v1",
        "max_tokens": 50,
        "temperature": 0.7,
    },
    "azure_openai": {
        "model": "gpt-35-turbo",
        "endpoint": "",  # Azure OpenAI requires custom endpoint
        "max_tokens": 50,
        "temperature": 0.7,
    },
}

# Core default settings
DEFAULT_CONFIG = {
    "Core": {
        "provider": "openai",  # Default provider
        "commit_format": "conventional",
        "auto_commit": "false",
        "cache_responses": "true",
    },
    "openai": {
        "model": "gpt-3.5-turbo",
        "endpoint": "https://api.openai.com/v1",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
    "anthropic": {
        "model": "claude-3-sonnet-20240229",
        "endpoint": "https://api.anthropic.com",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
    "gemini": {
        "model": "gemini-pro",
        "endpoint": "https://generativelanguage.googleapis.com/v1",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
    "azure_openai": {
        "model": "gpt-3.5-turbo",
        "endpoint": "",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
    "ollama": {
        "model": "llama2",
        "endpoint": "http://localhost:11434",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
    "huggingface": {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "endpoint": "https://api-inference.huggingface.co/models",
        "max_tokens": "50",
        "temperature": "0.7",
        "api_key": "",
    },
}

# Default models for each provider
DEFAULT_MODELS = {
    "openai": "gpt-3.5-turbo",
    "anthropic": "claude-3-sonnet-20240229",
    "gemini": "gemini-pro",
    "azure_openai": "gpt-3.5-turbo",
    "ollama": "llama2",
    "huggingface": "mistralai/Mistral-7B-Instruct-v0.2",
}


def get_config_path() -> Path:
    """Get the path to the configuration file."""
    if os.name == "nt":  # Windows
        config_dir = Path(os.getenv("APPDATA", "")) / "cmscribe"
    else:  # Unix/macOS
        config_dir = Path.home() / ".config" / "cmscribe"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.ini"


def load_config() -> configparser.ConfigParser:
    """Load the configuration from file."""
    config = configparser.ConfigParser()
    config_path = get_config_path()

    if config_path.exists():
        config.read(config_path)
    else:
        create_config()
        config.read(config_path)

    return config


def save_config(config: configparser.ConfigParser) -> None:
    """Save the configuration to file."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        config.write(f)


def create_config() -> None:
    """Create a new configuration file with default settings."""
    if Path(DEFAULT_CONFIG_PATH).exists():
        print(f"Config already exists at {DEFAULT_CONFIG_PATH}. Use 'update' to modify.")
        return
    config = configparser.ConfigParser()

    # Add all sections with their default values
    for section, values in DEFAULT_CONFIG.items():
        config[section] = values

    save_config(config)
    print("Configuration file created with default settings.")


def update_config(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    commit_format: Optional[str] = None,
    auto_commit: Optional[bool] = None,
    cache_responses: Optional[bool] = None,
    set_default: bool = False,
) -> None:
    """Update the configuration with new values."""
    config = load_config()

    # Update Core settings if provided
    if commit_format is not None:
        config["Core"]["commit_format"] = commit_format
    if auto_commit is not None:
        config["Core"]["auto_commit"] = str(auto_commit).lower()
    if cache_responses is not None:
        config["Core"]["cache_responses"] = str(cache_responses).lower()

    # If setting default provider
    if set_default and provider:
        config["Core"]["provider"] = provider

    # Update provider settings if provided
    if provider:
        # Ensure provider section exists
        if provider not in config:
            config[provider] = DEFAULT_CONFIG[provider]

        # Update provider settings
        if api_key is not None:
            config[provider]["api_key"] = api_key
        if endpoint is not None:
            config[provider]["endpoint"] = endpoint
        if model is not None:
            config[provider]["model"] = model
        if max_tokens is not None:
            config[provider]["max_tokens"] = str(max_tokens)
        if temperature is not None:
            config[provider]["temperature"] = str(temperature)

    save_config(config)


def get_provider_config(provider: Optional[str] = None) -> Dict[str, Any]:
    """Get configuration for a specific provider or the default provider."""
    config = load_config()

    # If no provider specified, use the default one
    if provider is None:
        provider = config["Core"]["provider"]

    # Ensure provider section exists
    if provider not in config:
        config[provider] = DEFAULT_CONFIG[provider]
        save_config(config)

    # Get provider settings
    provider_config = dict(config[provider])

    # Convert string values to appropriate types
    provider_config["max_tokens"] = int(provider_config["max_tokens"])
    provider_config["temperature"] = float(provider_config["temperature"])

    return provider_config


def get_default_provider() -> str:
    """Get the currently configured default provider."""
    config = load_config()
    return config["Core"]["provider"]
