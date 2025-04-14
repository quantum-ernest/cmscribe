"""Context and response caching for providers."""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class CacheManager:
    """Manages caching of provider responses and contexts."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the cache manager."""
        if cache_dir is None:
            if os.name == "nt":  # Windows
                self.cache_dir = Path(os.getenv("APPDATA", "")) / "cmscribe" / "cache"
            else:  # Unix/macOS
                self.cache_dir = Path.home() / ".cache" / "cmscribe"
        else:
            self.cache_dir = cache_dir

        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, repo_name: str, provider: str, model: str) -> str:
        """Generate a unique cache key for the given parameters."""
        key_str = f"{repo_name}:{provider}:{model}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_cache_file(self, cache_key: str) -> Path:
        """Get the path to the cache file for the given key."""
        return self.cache_dir / f"{cache_key}.json"

    def get_context(self, repo_name: str, provider: str, model: str) -> Optional[Dict[str, Any]]:
        """Get cached context for the given repository, provider, and model."""
        cache_key = self._get_cache_key(repo_name, provider, model)
        cache_file = self._get_cache_file(cache_key)

        if not cache_file.exists():
            return None
        try:
            with open(cache_file) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    def save_context(
        self, repo_name: str, provider: str, model: str, context: Dict[str, Any]
    ) -> None:
        """Save context for the given repository, provider, and model."""
        cache_key = self._get_cache_key(repo_name, provider, model)
        cache_file = self._get_cache_file(cache_key)

        try:
            with open(cache_file, "w") as f:
                json.dump(context, f)
        except OSError as e:
            print(f"Warning: Failed to save cache: {e}")

    def clear_context(self, repo_name: str, provider: str, model: str) -> None:
        """Clear cached context for the given repository, provider, and model."""
        cache_key = self._get_cache_key(repo_name, provider, model)
        cache_file = self._get_cache_file(cache_key)

        try:
            if cache_file.exists():
                cache_file.unlink()
        except OSError as e:
            print(f"Warning: Failed to clear cache: {e}")

    def clear_all_contexts(self) -> None:
        """Clear all cached contexts."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except OSError as e:
            print(f"Warning: Failed to clear all caches: {e}")
