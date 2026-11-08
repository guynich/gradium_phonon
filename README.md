# Gradium Phonon model on Orange Pi 5

Text-to-speech installation, inference runtimes, and audio configuration
for the Orange Pi 5 single board computer (8GB RAM, ARM CPU, aarch64, 
Ubuntu 24.04).

Coding assistant: Antigravity CLI.

## Overview

This repository provides setup instructions, usage examples, and test scripts
for running Gradium Phonon on-device speech synthesis models.

Supported runtimes:
- Gradium Native Runtime (`ptts`): Standalone Rust-based inference engine.
- Hugging Face Transformers: PyTorch pipelines using `gradium/phonon-31m-en`
  and `gradium/phonon-40m-en`.

Audio output routes through the default Ubuntu audio sink via PipeWire or ALSA.

## Documentation Index

Detailed guides are located in the `docs/` directory:

- [docs/installation.md](docs/installation.md):
  Step-by-step setup using `uv` and virtual environments.
- [docs/runtimes.md](docs/runtimes.md):
  In-depth comparison of `ptts` native runtime versus Hugging Face.
- [docs/models_and_licensing.md](docs/models_and_licensing.md):
  Overview of 31M (Apache 2.0) and 40M (CC BY-NC 4.0 gated) models and voices.
- [docs/voices.md](docs/voices.md):
  Full catalog reference and descriptions for all 37 English voice options.
- [docs/audio_output.md](docs/audio_output.md):
  Audio device discovery, PipeWire default routing, and PCM streaming.

## Example Scripts

Executable scripts are available in the `src/` directory:

- [src/ptts_speak.py](src/ptts_speak.py):
  Python runner for `ptts` with streaming and file playback support.
- [src/hf_speak.py](src/hf_speak.py):
  Hugging Face Transformers inference and audio generation script.
- [src/ptts_cli_demo.sh](src/ptts_cli_demo.sh):
  Shell helper demonstrating `ptts` CLI execution.

## Quick Start

1. Set up the virtual environment:
   ```bash
   uv venv ~/venv/phonon
   uv pip install --python ~/venv/phonon/bin/python ptts
   ```

2. Generate and stream speech:
   ```bash
   ~/venv/phonon/bin/python src/ptts_speak.py --stream "Hello Orange Pi 5."
   ```

3. Stream a file using a specific voice at a slower pace:

   ```bash
   ~/venv/phonon/bin/python src/ptts_speak.py \
     --voice "Toby" \
     --speed 0.8 \
     --stream samples/a_tale_of_two_cities.txt
   ```

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
