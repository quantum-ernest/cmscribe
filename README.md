# Cmscribe

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

AI-powered commit message generator that leverages various AI providers to create meaningful commit messages from your code changes.

</div>

## 🌟 Features

- **Multiple AI Providers**
  - OpenAI
  - Anthropic
  - Google
  - Azure OpenAI
  - Ollama ✅
  - HuggingFace

- **Commit Message Formats**
  - Conventional Commits (`<type>(<scope>): <description>`)
  - Semantic Versioning (`<type>: <description>`)
  - Simple format (`<description>`)
  - Angular format (`<type>(<scope>): <description>`)

- **Smart Configuration**
  - Multiple provider configurations
  - Default provider setting
  - Environment variable support
  - Provider-specific defaults
  - Easy provider switching

- **Developer Experience**
  - Auto-commit support
  - Response caching
  - Git hook integration
  - Cross-platform support

## 🚀 Installation

### Using `uv` (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install cmscribe
```

### Using `pip`

```bash
pip install cmscribe
```

## 💻 Usage

### Basic Usage

```bash
# Generate a commit message for staged changes
cmscribe gen

# Generate with a specific provider (overrides default)
cmscribe gen --provider openai

# Generate with a specific commit format
cmscribe gen --format conventional

# Generate and auto-commit
cmscribe gen --auto
```

### Configuration Management

#### Quick Setup

```bash
# Create initial configuration with all providers
cmscribe config create

# Configure OpenAI
cmscribe config update --provider openai --api-key YOUR_API_KEY

# Configure Anthropic
cmscribe config update --provider anthropic --api-key YOUR_API_KEY

# Configure Google
cmscribe config update --provider gemini --api-key YOUR_API_KEY

# Set OpenAI as default provider
cmscribe config update --provider openai --set-default
```

#### Provider-Specific Configuration

Each provider has sensible defaults, but you can customize them:

```bash
# OpenAI with custom settings
cmscribe config update --provider openai \
    --api-key YOUR_API_KEY \
    --model gpt-4 \
    --max-tokens 100 \
    --temperature 0.8

# Ollama (local)
cmscribe config update --provider ollama \
    --model llama2 \
    --endpoint http://localhost:11434

# Ollama (remote)
cmscribe config update --provider ollama \
    --model llama2 \
    --endpoint http://your-server:11434

# Azure OpenAI
cmscribe config update --provider azure_openai \
    --api-key YOUR_API_KEY \
    --endpoint YOUR_ENDPOINT \
    --model gpt-4
```

#### Core Settings

Configure global settings that apply to all providers:

```bash
# Set default commit format
cmscribe config update --format conventional

# Enable auto-commit
cmscribe config update --auto-commit true

# Enable response caching
cmscribe config update --cache-responses true
```

#### Environment Variables

You can also use environment variables for sensitive information:

```bash
# OpenAI
export OPENAI_API_KEY="your-api-key"

# Anthropic
export ANTHROPIC_API_KEY="your-api-key"

# Google
export GOOGLE_API_KEY="your-api-key"

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"
```

#### View Configuration

View your current configuration:

```bash
cmscribe config show
```

## 🔧 Configuration File

The configuration file is located at:
- Unix/macOS: `~/.config/cmscribe/config.ini`
- Windows: `%APPDATA%\cmscribe\config.ini`

### Example Configuration

```ini
[Core]
provider = openai
commit_format = conventional
auto_commit = false
cache_responses = true

[openai]
model = gpt-3.5-turbo
endpoint = https://api.openai.com/v1
max_tokens = 50
temperature = 0.7
api_key = your-api-key

[anthropic]
model = claude-3-sonnet-20240229
endpoint = https://api.anthropic.com
max_tokens = 50
temperature = 0.7
api_key = your-api-key

[gemini]
model = gemini-pro
endpoint = https://generativelanguage.googleapis.com/v1
max_tokens = 50
temperature = 0.7
api_key = your-api-key

[ollama]
model = llama2
endpoint = http://localhost:11434
max_tokens = 50
temperature = 0.7
api_key = 

[huggingface]
model = mistralai/Mistral-7B-Instruct-v0.2
endpoint = https://api-inference.huggingface.co/models
max_tokens = 50
temperature = 0.7
api_key = your-api-key
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=cmscribe

# Run specific test file
uv run pytest test/test_providers.py
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Format code
uv run black .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
