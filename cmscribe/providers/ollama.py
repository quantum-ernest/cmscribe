"""Ollama provider implementation."""

from typing import Any, Dict

import requests

from cmscribe.core import CommitFormat

from .base import AIProvider


class OllamaProvider(AIProvider):
    """Provider for Ollama models."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the Ollama provider."""
        super().__init__(config)
        self.endpoint = config.get("endpoint", "http://localhost:11434")
        self._load_context()

    def get_default_model(self) -> str:
        return "llama2"

    def validate_config(self) -> bool: ...

    def generate_commit_message(self, commit_format: CommitFormat) -> tuple:
        """Generate a commit message using Ollama."""
        # Get the staged changes
        from cmscribe.utils import (get_file_content_before_after,
                                         get_staged_files)

        staged_files = get_staged_files()

        if not staged_files:
            return None, "No staged changes found."

        # Get the diff content
        content = get_file_content_before_after(staged_files)
        diff_content = "\n".join(
            [f"File: {file}\n{content[file]['after']}" for file in staged_files]
        )

        # Format the prompt
        prompt = self._format_prompt(diff_content, commit_format)

        # Prepare the request
        request_data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }

        # Add context if available
        if self._context:
            request_data["context"] = self._context.get("context", [])

        try:
            # Make the request
            response = requests.post(
                f"{self.endpoint}/api/generate", json=request_data, timeout=300
            )
            response.raise_for_status()

            # Process the response
            result = response.json()
            message = self._process_response(result)

            # Save the new context
            if "context" in result:
                self._save_context({"context": result["context"]})

            return message, None
        except requests.exceptions.RequestException as e:
            return None, f"Error generating commit message: {str(e)}"

    def _format_prompt(self, diff: str, commit_format: CommitFormat) -> str:
        """Format the prompt for Ollama."""
        format_instructions = {
            CommitFormat.CONVENTIONAL: (
                "Generate a commit message following the Conventional Commits format.\n"
                "Format: <type>(<scope>): <description>\n"
                "Types: feat, fix, chore, refactor, docs, test, ci, build"
            ),
            CommitFormat.SEMANTIC: (
                "Generate a commit message following Semantic Versioning.\n"
                "Format: <type>: <description>\n"
                "Types: major, minor, patch"
            ),
            CommitFormat.SIMPLE: (
                "Generate a simple commit message.\n" "Format: <description>"
            ),
            CommitFormat.ANGULAR: (
                "Generate a commit message following the Angular format.\n"
                "Format: <type>(<scope>): <description>\n"
                "Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
            ),
        }

        return (
            f"{format_instructions[commit_format]}\n\n"
            f"Here are the changes:\n{diff}\n\n"
            "Generate a commit message:"
        )

    def _process_response(self, response: Dict[str, Any]) -> str:
        """Process Ollama's response into a commit message."""
        return response.get("response", "").strip()
