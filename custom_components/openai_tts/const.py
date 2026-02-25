"""Constants for the OpenAI-compatible TTS custom component."""

DOMAIN = "openai_tts"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_SPEED = "speed"
CONF_URL = "url"
CONF_VOICE = "voice"
UNIQUE_ID = "unique_id"

# Keep defaults OpenAI-compatible while providing fish.audio-friendly options.
MODELS: list[str] = [
    "tts-1",
    "tts-1-hd",
    "s1",
]

VOICES: list[str] = [
    "alloy",
    "echo",
    "fable",
    "nova",
    "onyx",
    "shimmer",
]

DEFAULT_URL = "https://api.fish.audio/v1/audio/speech"
