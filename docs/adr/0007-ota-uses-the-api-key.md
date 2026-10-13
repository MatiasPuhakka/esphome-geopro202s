# OTA uploads authenticate with the API key

`node.yaml` sets `ota: encryption: {}` with no `password` (#85). A bare encryption block takes the API encryption key, so OTA uploads are encrypted and authenticated with the same key that the API already uses, and the Node has one secret instead of two. With both a password and an API key set, every ESPHome 2026.9.1 build warned that the password costs about 3.5 KB of flash and 60 bytes of RAM, plus the password on the heap, and guards only uploaders that can't encrypt. Nothing that uploads to the Node is one of those.

Every upload now has to speak encrypted OTA. The firmware refuses an upload that doesn't encrypt with the key, and the uploader refuses a device that doesn't offer encryption, with no plaintext fallback. Both ends need ESPHome 2026.9.0 or later, which ADR 0002 already requires. Anyone holding the API key can flash the Node, as anyone holding it could already read and control it over the API.

Rotating the API key now also changes how OTA authenticates. The uploader encrypts with the key in the config it reads, but the Node still runs firmware with the old key, so the upload that ships a new key has to encrypt with the old one. One way, untested here: build with the new key, then `esphome upload --file <the new firmware.bin>` from a config whose `secrets.yaml` still holds the old key.
