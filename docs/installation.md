# Installation Guide: Gradium Phonon on Orange Pi 5

This document details the complete environment setup for running the Gradium
Phonon text-to-speech models on an Orange Pi 5 single board computer running
Ubuntu 24.04 LTS (aarch64).

## System Prerequisites

- Target Hardware: Orange Pi 5 (Rockchip RK3588S, 8GB RAM, ARM64 / aarch64)
- Operating System: Ubuntu 24.04 LTS (Noble Numbat)
- Audio System: PipeWire / ALSA default audio daemon
- Python Interpreter: Python 3.12 (standard on Ubuntu 24.04)

## Step 1: Install uv Package Manager

Install the fast `uv` binary into `~/.local/bin`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

Verify that `uv` is available:

```bash
uv --version
```

## Step 2: Create the Virtual Environment

Create a dedicated virtual environment under `~/venv/phonon`:

```bash
uv venv ~/venv/phonon
source ~/venv/phonon/bin/activate
```

## Step 3: Install Gradium Native Runtime (ptts)

Gradium provides an optimized standalone runtime packaged as a Rust wheel named
`ptts`. It does not require PyTorch or system-level speech packages like
`espeak-ng`.

Install `ptts` into the virtual environment:

```bash
uv pip install --python ~/venv/phonon/bin/python ptts
```

Test the runtime CLI:

```bash
~/venv/phonon/bin/ptts --build-info
```

## Step 4: Install PyTorch and Hugging Face Transformers

To load model weights (`gradium/phonon-31m-en` or `gradium/phonon-40m-en`)
directly through Hugging Face pipelines, install PyTorch and Transformers.

Because the Orange Pi 5 utilizes an ARM Cortex CPU rather than an Nvidia GPU,
install CPU-only PyTorch wheels to avoid unnecessary multi-gigabyte CUDA
dependencies:

```bash
uv pip install --python ~/venv/phonon/bin/python \
  --extra-index-url https://download.pytorch.org/whl/cpu \
  torch \
  transformers \
  accelerate \
  safetensors \
  huggingface_hub
```

## Step 5: Verify Audio Output Utilities

Ensure standard Ubuntu audio playback utilities are available:

```bash
which pw-play aplay
```

On Ubuntu 24.04 Desktop, PipeWire (`pw-play`) is installed by default and routes
audio directly to the default audio sink configured in Ubuntu Sound Settings.

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
