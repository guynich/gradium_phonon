#!/usr/bin/env python3
"""Synthesize speech using Gradium's native ptts standalone runtime."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time

import ptts

DEFAULT_MODEL = "hf://gradium/phonon-31m-en"


def play_wav(wav_path: str) -> None:
    """Play generated WAV file using Ubuntu default audio device."""
    if shutil.which("pw-play"):
        subprocess.run(["pw-play", wav_path], check=True)
    elif shutil.which("aplay"):
        subprocess.run(["aplay", "-q", wav_path], check=True)
    else:
        print("Warning: Neither pw-play nor aplay was found for audio playback.", file=sys.stderr)


def stream_audio(tts: ptts.TTS, text: str, voice: str) -> None:
    """Stream PCM float32 chunks in real-time to Ubuntu PipeWire or ALSA."""
    pw_play = shutil.which("pw-play")
    aplay = shutil.which("aplay")

    if pw_play:
        cmd = ["pw-play", "--rate=24000", "--channels=1", "--format=f32", "-"]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        write_chunk = lambda chunk: proc.stdin.write(chunk.tobytes())  # noqa: E731
    elif aplay:
        cmd = ["aplay", "-q", "-r", "24000", "-c", "1", "-f", "S16_LE", "-"]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        import numpy as np
        write_chunk = lambda chunk: proc.stdin.write((chunk * 32767.0).astype(np.int16).tobytes())  # noqa: E731
    else:
        print("Error: Neither pw-play nor aplay was found for audio playback.", file=sys.stderr)
        return

    print("Streaming speech to default Ubuntu audio device...")
    start_time = time.time()
    first_chunk_time = None
    chunk_count = 0

    with tts.stream(text, voice=voice) as audio:
        for chunk in audio:
            if first_chunk_time is None:
                first_chunk_time = time.time()
                print(f"Time to first audio (TTFA): {(first_chunk_time - start_time) * 1000.0:.1f} ms")
            write_chunk(chunk)
            chunk_count += 1

    proc.stdin.close()
    proc.wait()
    total_time = time.time() - start_time
    print(f"Streaming complete: {chunk_count} chunks in {total_time:.2f} seconds.")


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
        raw = "Hello from Gradium Phonon running natively on the Orange Pi 5."

    if clean_md:
        # Strip code blocks
        raw = re.sub(r"```[\s\S]*?```", "", raw)
        # Strip inline code formatting
        raw = re.sub(r"`([^`]+)`", r"\1", raw)
        # Convert markdown links [text](url) -> text
        raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
        # Strip header markers (# Header -> Header)
        raw = re.sub(r"^#+\s*", "", raw, flags=re.MULTILINE)
        # Strip bullet points
        raw = re.sub(r"^\s*[-*+]\s+", "", raw, flags=re.MULTILINE)

    return raw.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synthesize speech with ptts native runtime on Orange Pi 5."
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
        help=f"Model repository (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="en",
        help="Text normalization language (en, fr, de, es, pt, etc.)",
    )
    parser.add_argument(
        "-v",
        "--voice",
        default="Easton",
        help="Voice name from catalog or checkpoint (default: Easton)",
    )
    parser.add_argument(
        "-q",
        "--quant",
        default="q8_0",
        help="Quantization format: f32, q8_0, q6k, q5_0, q4_0, etc. (default: q8_0)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="ptts_out.wav",
        help="Output WAV path (default: ptts_out.wav)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream audio in real-time instead of writing to disk first",
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
    parser.add_argument(
        "--duration-delta",
        type=float,
        default=None,
        help="Model pacing conditioner (e.g. 0.5 to 2.0 for slower, -0.5 for faster)",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=None,
        help="Speech speed multiplier (e.g. 0.8 for slower rate, 1.2 for faster rate)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=None,
        help="Number of CPU threads for tensor operations",
    )
    args = parser.parse_args()

    # Pass HF_TOKEN to environment if cached token exists and not already set
    if "HF_TOKEN" not in os.environ and os.path.exists(os.path.expanduser("~/.cache/huggingface/token")):
        with open(os.path.expanduser("~/.cache/huggingface/token"), "r", encoding="utf-8") as f:
            os.environ["HF_TOKEN"] = f.read().strip()

    if args.threads:
        ptts.set_num_threads(args.threads)

    text_to_speak = resolve_text_input(args.text, args.file, clean_md=not args.raw_text)
    if not text_to_speak:
        print("Error: No input text provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing ptts runtime with model {args.model} ({args.quant})...")
    init_start = time.time()
    tts = ptts.TTS(args.model, lang=args.lang, quant=args.quant)
    init_duration = time.time() - init_start
    print(f"Runtime initialized in {init_duration:.2f} seconds.")

    duration_delta = args.duration_delta
    if duration_delta is None and args.speed is not None:
        if args.speed <= 0:
            print("Error: --speed must be greater than 0.", file=sys.stderr)
            sys.exit(1)
        duration_delta = (1.0 / args.speed - 1.0) * 3.0

    if duration_delta is not None:
        print(f"Setting duration_delta pacing condition: {duration_delta:.2f}")
        tts.set_conditions({"duration_delta": str(duration_delta)})

    preview = text_to_speak[:80] + ("..." if len(text_to_speak) > 80 else "")
    print(f"Text to speak ({len(text_to_speak)} characters): \"{preview}\"")

    if args.stream:
        stream_audio(tts, text_to_speak, args.voice)
    else:
        print(f"Synthesizing to {args.output}...")
        synth_start = time.time()
        tts.save(args.output, text_to_speak, voice=args.voice)
        synth_duration = time.time() - synth_start
        print(f"Wrote {args.output} in {synth_duration:.2f} seconds.")

        if not args.no_play:
            print("Playing audio via Ubuntu default audio output...")
            play_wav(args.output)


if __name__ == "__main__":
    main()
