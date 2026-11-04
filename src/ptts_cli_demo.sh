#!/usr/bin/env bash
# Demonstration script for ptts CLI commands on Orange Pi 5
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_BIN="${HOME}/venv/phonon/bin"

if [ -x "${VENV_BIN}/ptts" ]; then
    PTTS_CMD="${VENV_BIN}/ptts"
elif command -v uvx >/dev/null 2>&1; then
    PTTS_CMD="uvx ptts"
else
    echo "Error: Neither ${VENV_BIN}/ptts nor uvx was found." >&2
    exit 1
fi

echo "Using ptts command: ${PTTS_CMD}"
echo "Synthesizing test speech..."

${PTTS_CMD} \
    --lang en \
    --quant q8_0 \
    --voice Easton \
    -o "ptts_cli_demo.wav" \
    "Hello from the ptts command line interface on Orange Pi 5."

echo "Playback via Ubuntu default audio output..."
if command -v pw-play >/dev/null 2>&1; then
    pw-play "ptts_cli_demo.wav"
elif command -v aplay >/dev/null 2>&1; then
    aplay -q "ptts_cli_demo.wav"
fi
