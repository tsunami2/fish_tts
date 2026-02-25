"""Setting up TTS entity."""

from __future__ import annotations

import logging

from homeassistant.components.tts import TextToSpeechEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import MaxLengthExceeded
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_API_KEY, CONF_URL, CONF_VOICE_ID, DOMAIN, UNIQUE_ID
from .openaitts_engine import OpenAITTSEngine

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Fish Text-to-speech platform via config entry."""

    engine = OpenAITTSEngine(
        config_entry.data[CONF_API_KEY],
        config_entry.data[CONF_VOICE_ID],
        config_entry.data[CONF_URL],
    )
    async_add_entities([OpenAITTSEntity(hass, config_entry, engine)])


class OpenAITTSEntity(TextToSpeechEntity):
    """The Fish TTS entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, config: ConfigEntry, engine: OpenAITTSEngine):
        """Initialize TTS entity."""
        self.hass = hass
        self._engine = engine
        self._config = config

        self._attr_unique_id = config.data.get(UNIQUE_ID)
        if self._attr_unique_id is None:
            self._attr_unique_id = config.data[CONF_VOICE_ID]

        self.entity_id = generate_entity_id("tts.fish_tts_{}", config.data[CONF_VOICE_ID], hass=hass)

    @property
    def default_language(self):
        """Return the default language."""
        return "en"

    @property
    def supported_languages(self):
        """Return the list of supported languages."""
        return self._engine.get_supported_langs()

    @property
    def device_info(self):
        """Return device metadata."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "model": f"{self._config.data[CONF_VOICE]}",
            "manufacturer": "Fish Audio / OpenAI-compatible"
        }

    @property
    def name(self):
        """Return entity name."""
        return self._config.data[CONF_VOICE_ID]

    def get_tts_audio(self, message, language, options=None):
        """Convert a given text to speech and return it as bytes."""
        try:
            if len(message) > 4096:
                raise MaxLengthExceeded

            speech_bytes = self._engine.get_tts(message)
            return "wav", speech_bytes
        except MaxLengthExceeded:
            _LOGGER.error("Maximum length of the message exceeded")
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Fish TTS error: %s", err)

        return None, None
