#!/usr/bin/env python3
"""Synthesize speech using Hugging Face Transformers and Kyutai/Phonon pipelines."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time

import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from transformers import AutoProcessor, GradiumPhononTTSForConditionalGeneration

DEFAULT_MODEL = "gradium/phonon-31m-en"
VOICE_MAP = {
    "easton": "voices/LMDIYE0Oa377Qh6Z.safetensors",
    "zoey": "voices/NbpkqMVS3CJeq2j8.safetensors",
    "juniper": "voices/NIWIOv5vTi5eRMj8.safetensors",
    "harper": "voices/4SZHfMpw-p46Ywgs.safetensors",
}


def play_wav(wav_path: str) -> None:
    """Play generated WAV file using Ubuntu default audio device."""
    if shutil.which("pw-play"):
        subprocess.run(["pw-play", wav_path], check=True)
    elif shutil.which("aplay"):
        subprocess.run(["aplay", "-q", wav_path], check=True)
    else:
        print("Warning: Neither pw-play nor aplay was found for audio playback.", file=sys.stderr)


def resolve_text_input(text_arg: str | None, file_arg: str | None, clean_md: bool = True) -> str:
    """Resolve input text from string argument, file path, or stdin."""
    raw = None

    if file_arg:
        with open(file_arg, "r", encoding="utf-8") as f:
            raw = f.read()
    elif text_arg == "-" or (not text_arg and not sys.stdin.isatty()):
        raw = sys.stdin.read()
    elif text_arg and os.path.isfile(text_arg):
        with open(text_arg, "r", encoding="utf-8") as f:
            raw = f.read()
    elif text_arg:
        raw = text_arg
    else:
        raw = "Hello from Hugging Face Transformers on Orange Pi 5."

    if clean_md:
        raw = re.sub(r"```[\s\S]*?```", "", raw)
        raw = re.sub(r"`([^`]+)`", r"\1", raw)
        raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
        raw = re.sub(r"^#+\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"^\s*[-*+]\s+", "", raw, flags=re.MULTILINE)

    return raw.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synthesize speech with Hugging Face Transformers on Orange Pi 5."
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text string or file path to synthesize (reads from stdin if '-' or piped)",
    )
    parser.add_argument(
        "-f",
        "--file",
        default=None,
        help="Path to a text or markdown file to synthesize",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        help=f"Hugging Face model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-v",
        "--voice",
        default="easton",
        help="Voice name (easton, zoey, juniper, harper) or safetensors path (default: easton)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="hf_out.wav",
        help="Output WAV path (default: hf_out.wav)",
    )
    parser.add_argument(
        "--no-play",
        action="store_true",
        help="Do not play audio to Ubuntu default device after generation",
    )
    parser.add_argument(
        "--raw-text",
        action="store_true",
        help="Do not clean markdown formatting from file input",
    )
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token and os.path.exists(os.path.expanduser("~/.cache/huggingface/token")):
        with open(os.path.expanduser("~/.cache/huggingface/token"), "r", encoding="utf-8") as f:
            token = f.read().strip()

    text_to_speak = resolve_text_input(args.text, args.file, clean_md=not args.raw_text)
    if not text_to_speak:
        print("Error: No input text provided.", file=sys.stderr)
        sys.exit(1)

    preview = text_to_speak[:80] + ("..." if len(text_to_speak) > 80 else "")
    print(f"Text to speak ({len(text_to_speak)} characters): \"{preview}\"")

    print(f"Loading processor: {args.model} ...")
    processor = AutoProcessor.from_pretrained(args.model, token=token)

    print(f"Loading model: {args.model} (float32 for ARM CPU) ...")
    model = GradiumPhononTTSForConditionalGeneration.from_pretrained(
        args.model,
        torch_dtype=torch.float32,
        token=token,
    )

    voice_target = args.voice.lower()
    voice_file = VOICE_MAP.get(voice_target, args.voice)

    print(f"Loading voice latent: {voice_file} ...")
    if os.path.exists(voice_file):
        voice_local_path = voice_file
    else:
        voice_local_path = hf_hub_download(
            repo_id="gradium/phonon-voices",
            filename=voice_file,
            token=token,
        )

    voice_latents = load_file(voice_local_path)["speaker_wavs"][0].T.float()

    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "audio"},
                {"type": "text", "text": text_to_speak},
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        conversation,
        tokenize=True,
        return_dict=True,
        add_generation_prompt=True,
        processor_kwargs={"audio_prompt_latents": [voice_latents]},
    )

    print("Synthesizing audio...")
    start_time = time.time()
    outputs = model.generate(**inputs)
    gen_duration = time.time() - start_time
    print(f"Synthesis completed in {gen_duration:.2f} seconds.")

    audio = processor.decode(outputs.audio_latents, outputs.audio_latents_mask)
    processor.save_audio(audio, args.output)
    print(f"Saved audio to {args.output}")

    if not args.no_play:
        print("Playing audio via Ubuntu default audio output...")
        play_wav(args.output)


if __name__ == "__main__":
    main()
