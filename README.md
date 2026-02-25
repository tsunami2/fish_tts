# fish_tts
# Fish Audio TTS (OpenAI-Compatible) for Home Assistant

This custom component is based on the `openai_tts` integration and is tuned for using
[fish.audio](https://fish.audio/) as a Home Assistant Text-to-Speech provider.

## Description

This integration adds a TTS entity that can be used by Home Assistant Assist, automations,
and scripts. It sends text to an OpenAI-compatible endpoint and returns WAV audio.

By default, the config flow points to Fish Audio:

- `https://api.fish.audio/v1/audio/speech`

You can still use another OpenAI-compatible endpoint by changing the URL in the config flow.

## Features

- OpenAI-compatible TTS request format
- Default endpoint set for fish.audio
- Configurable model, voice, speed, URL, and API key
- Works with Home Assistant `tts.speak`

## Example Home Assistant service call

```yaml
service: tts.speak
target:
  entity_id: tts.openai_tts_shimmer
data:
  cache: true
  media_player_entity_id: media_player.bedroom_speaker
  message: Hello from Fish Audio text to speech.
```

## HACS installation

1. Go to **HACS** in Home Assistant.
2. Open the 3-dot menu and choose **Custom repositories**.
3. Add this repository URL and choose **Integration**.
4. Install the integration and restart Home Assistant.
5. Add the integration from **Settings → Devices & Services**.
6. Enter your Fish Audio API key (if required), then choose model and voice.

## Manual installation

1. Ensure your Home Assistant config directory has a `custom_components` folder.
2. Copy `custom_components/openai_tts` into that folder.
3. Restart Home Assistant.
4. Add the integration via **Settings → Devices & Services**.
