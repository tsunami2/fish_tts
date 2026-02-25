# fish_tts
# Fish Audio TTS for Home Assistant

This custom component is a fork of `openai_tts` adapted for
[Fish Audio](https://fish.audio/) usage in Home Assistant.

## What this integration asks for

Per Fish Audio quickstart/API usage, setup is focused on:

- **API key**
- **Voice ID**

The integration UI asks for those values directly.

## Endpoint

Default endpoint:

- `https://api.fish.audio/v1/tts`

You can override it in the config flow if needed.

## Features

- Fish Audio TTS support for Home Assistant `tts.speak`
- Config flow fields for API key + Voice ID
- WAV audio output

## Example Home Assistant service call

```yaml
service: tts.speak
target:
  entity_id: tts.fish_tts_your_voice_id
data:
  cache: true
  media_player_entity_id: media_player.bedroom_speaker
  message: Hello from Fish Audio text to speech.
```

## Installation (HACS)

1. Open **HACS**.
2. Add this repository as a custom integration.
3. Install and restart Home Assistant.
4. Go to **Settings → Devices & Services** and add **Fish TTS**.
5. Enter your Fish Audio API key and Voice ID.

## Manual installation

1. Copy `custom_components/openai_tts` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.
