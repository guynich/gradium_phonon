# Audio Output and Playback on Ubuntu

This document describes how audio playback and real-time streaming are routed
to the default Ubuntu audio device on the Orange Pi 5.

## Audio Architecture on Orange Pi 5

Ubuntu 24.04 utilizes PipeWire as its primary modern audio server, alongside an
ALSA compatibility layer.

Hardware playback interfaces detected on the Orange Pi 5:

- Analog Audio Jack (ES8388 codec, `card 0`)
- HDMI Audio (`card 2`)
- DisplayPort Audio (`card 1`)
- USB Audio Devices (e.g. `card 3: UACDemoV10`)

## Routing to the Default Ubuntu Output Device

When running Ubuntu Desktop, you can select the active output sink under:

`Settings -> Sound -> Output -> Output Device`

Both `pw-play` (PipeWire native player) and `aplay` route output through the
system's default device:

```bash
# Playback using PipeWire default sink
pw-play output.wav

# Playback using ALSA default device
aplay output.wav
```

## Real-Time PCM Audio Streaming

Phonon models output mono audio at a sample rate of 24,000 Hz (24 kHz) with
32-bit floating point PCM values (`float32`).

Rather than waiting for the entire sentence to synthesize and writing a WAV file
to storage, audio can be streamed in real time directly to `pw-play`:

```python
import subprocess
import ptts

tts = ptts.TTS("hf://gradium/phonon-31m-en", lang="en")

cmd = [
    "pw-play",
    "--rate=24000",
    "--channels=1",
    "--format=f32",
    "-",
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

with tts.stream("Real-time low-latency audio streaming.", voice="Easton") as audio:
    for chunk in audio:
        proc.stdin.write(chunk.tobytes())

proc.stdin.close()
proc.wait()
```

This configuration achieves time-to-first-audio (TTFA) in less than one second
on the Orange Pi 5 CPU.

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
