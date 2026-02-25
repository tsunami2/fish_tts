"""HTTP client for Fish Audio TTS."""

from __future__ import annotations

import urllib.error
import urllib.request
import json


class OpenAITTSEngine:
    """Talk to Fish Audio TTS endpoint."""

    def __init__(self, api_key: str, voice_id: str, url: str):
        self._api_key = api_key
        self._voice_id = voice_id
        self._url = url

    def get_tts(self, text: str) -> bytes:
        """Convert text to speech via Fish Audio API."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "reference_id": self._voice_id,
            "format": "wav",
            "latency": "normal",
        }
        req = urllib.request.Request(
            self._url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Fish Audio request failed ({exc.code}): {details}") from exc

    @staticmethod
    def get_supported_langs() -> list[str]:
        """Return language hints used by Home Assistant."""
        return ["en"]
