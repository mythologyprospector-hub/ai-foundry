"""Runtime adapter boundary for local model execution."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping


class RuntimeAdapter(ABC):
    """Provider-neutral interface for invoking a local model runtime."""

    @abstractmethod
    def generate(
        self,
        *,
        model: str,
        prompt: str,
        parameters: Mapping[str, Any],
    ) -> str:
        """Generate text from a model without exposing provider details."""
        raise NotImplementedError


class OllamaRuntime(RuntimeAdapter):
    """Minimal Ollama adapter using its local HTTP API."""

    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        *,
        model: str,
        prompt: str,
        parameters: Mapping[str, Any],
    ) -> str:
        import json
        from urllib.request import Request, urlopen

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": dict(parameters),
        }
        request = Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
        return str(body["response"])
