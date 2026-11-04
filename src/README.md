# Source Scripts Overview

This directory contains three independent runnable scripts demonstrating
different methods to run Gradium Phonon on the Orange Pi 5.

## Relationship Between the Scripts

The three scripts are completely independent of one another. None of them
import or rely on each other. They demonstrate three distinct usage paradigms:

1. [ptts_speak.py](ptts_speak.py):
   - Backend: Gradium native Rust runtime (`ptts`).
   - Characteristics: Lightweight, ultra-fast synthesis, real-time streaming to
     Ubuntu PipeWire or ALSA, document input parsing, and speed/pacing controls.
   - Best for: Production on-device text-to-speech and interactive voice apps.

2. [hf_speak.py](hf_speak.py):
   - Backend: Hugging Face Transformers and PyTorch CPU.
   - Characteristics: Standard Python ML pipeline using `AutoProcessor` and
     `GradiumPhononTTSForConditionalGeneration`. Uses `float32` for ARM CPU.
   - Best for: Machine learning experimentation and Hugging Face integration.

3. [ptts_cli_demo.sh](ptts_cli_demo.sh):
   - Backend: Standalone `ptts` CLI utility (or `uvx ptts`).
   - Characteristics: Simple Bash shell wrapper showing command-line synthesis
     and playback without writing any Python code.
   - Best for: Quick shell scripts, automation, and testing.

## Summary Comparison

| Script | Runtime Backend | PyTorch Required | Real-Time Streaming |
|---|---|---|---|
| `ptts_speak.py` | Native Rust (`ptts`) | No | Yes (`pw-play` / `aplay`) |
| `hf_speak.py` | PyTorch / Transformers | Yes | No (file generation) |
| `ptts_cli_demo.sh` | CLI executable / `uvx` | No | No (file generation) |

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
