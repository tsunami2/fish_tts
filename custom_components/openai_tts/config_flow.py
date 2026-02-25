"""Config flow for Fish Audio text-to-speech custom component."""
from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

import voluptuous as vol
from homeassistant import data_entry_flow
from homeassistant.config_entries import ConfigFlow
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_API_KEY, CONF_URL, CONF_VOICE_ID, DEFAULT_URL, DOMAIN, UNIQUE_ID

_LOGGER = logging.getLogger(__name__)


def generate_unique_id(user_input: dict[str, Any]) -> str:
    """Generate a unique ID from endpoint + voice ID."""
    url = urlparse(user_input[CONF_URL])
    return f"{url.hostname}_{user_input[CONF_VOICE_ID]}"


async def validate_user_input(user_input: dict[str, Any]) -> None:
    """Validate user input fields."""
    if not user_input.get(CONF_API_KEY):
        raise ValueError("API key is required")
    if not user_input.get(CONF_VOICE_ID):
        raise ValueError("Voice ID is required")


class OpenAITTSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fish Audio TTS."""

    VERSION = 1
    data_schema = vol.Schema(
        {
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_VOICE_ID): str,
            vol.Optional(CONF_URL, default=DEFAULT_URL): str,
        }
    )

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_user_input(user_input)
                unique_id = generate_unique_id(user_input)
                user_input[UNIQUE_ID] = unique_id
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                hostname = urlparse(user_input[CONF_URL]).hostname
                return self.async_create_entry(
                    title=f"Fish TTS ({hostname}, {user_input[CONF_VOICE_ID]})",
                    data=user_input,
                )
            except data_entry_flow.AbortFlow:
                return self.async_abort(reason="already_configured")
            except (HomeAssistantError, ValueError) as err:
                _LOGGER.exception(str(err))
                errors["base"] = "invalid_config"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception(str(err))
                errors["base"] = "unknown_error"

        return self.async_show_form(step_id="user", data_schema=self.data_schema, errors=errors)
