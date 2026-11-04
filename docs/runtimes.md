# Runtimes Comparison and Usage

This document explains the two execution runtimes supported for Gradium Phonon
on the Orange Pi 5: Gradium's native standalone runtime (`ptts`) and Hugging
Face Transformers with PyTorch.

## Runtime 1: Gradium Native Runtime (ptts)

The `ptts` package is built in Rust (`xn-ptts`) and delivers an optimized,
low-overhead inference engine tailored for local on-device deployment.

### Key Characteristics

- Dependencies: Minimal. Contains compiled Rust binaries and numpy; does not
  require PyTorch.
- Quantization: Native support for quantized weights including `q8_0`, `q8k`,
  `q6k`, `q5_0`, `q4_0`, and `f32`.
- Latency: Generates audio at speeds significantly faster than real-time on
  the Orange Pi 5 Cortex-A76 cores.
- Streaming: Generates 24 kHz float32 PCM chunks sequentially, allowing
  sub-second time-to-first-audio (TTFA).

### Command Line Usage

Generate a WAV file directly using the CLI:

```bash
~/venv/phonon/bin/ptts \
  --lang en \
  --quant q8_0 \
  --voice Easton \
  -o speech.wav \
  "Hello from Gradium Phonon."
```

Alternatively, run without persistent installation via `uvx`:

```bash
uvx ptts --lang en --quant q8_0 --voice Easton -o speech.wav "Testing uvx execution."
```

### Python Streaming Usage

```python
import ptts

tts = ptts.TTS("hf://gradium/phonon-31m-en", lang="en", quant="q8_0")

# Stream audio chunks directly
with tts.stream("Streaming speech on single board computer.", voice="Easton") as audio:
    for chunk in audio:
        # chunk is a float32 numpy array at 24000 Hz
        pass
```

### Reading Files and Markdown Documents

The runner script `src/ptts_speak.py` supports synthesizing documents (such
as `README.md`) directly using several input methods:

```bash
# Method 1: Pass the file path as the argument
~/venv/phonon/bin/python src/ptts_speak.py --stream README.md

# Method 2: Use the -f / --file option
~/venv/phonon/bin/python src/ptts_speak.py --stream -f README.md

# Method 3: Pipe file content via standard input
cat README.md | ~/venv/phonon/bin/python src/ptts_speak.py --stream

# Method 4: Bash command substitution
~/venv/phonon/bin/python src/ptts_speak.py --stream "$(cat README.md)"
```

By default, markdown files are automatically cleaned to strip code fences,
link brackets, and header hashes before speaking. Pass `--raw-text` to disable
markdown cleaning.

### Adjusting Speech Rate and Pacing

Phonon incorporates a native model conditioner called `duration_delta` to
adjust speech pacing and articulation speed without altering audio pitch:

- **Slower Speech**: Set positive values (e.g. `0.5` to `2.0`).
- **Faster Speech**: Set negative values (e.g. `-0.5`).

Using `src/ptts_speak.py`:

```bash
# Using intuitive --speed multiplier (e.g. 0.8 for slower rate)
~/venv/phonon/bin/python src/ptts_speak.py --stream --speed 0.8 samples/a_tale_of_two_cities.txt

# Or directly specifying the duration_delta conditioner
~/venv/phonon/bin/python src/ptts_speak.py --stream --duration-delta 1.0 samples/a_tale_of_two_cities.txt
```

Using the `ptts` CLI:

```bash
~/venv/phonon/bin/ptts -c duration_delta=1.0 -o slower_output.wav "Speaking more slowly and deliberately."
```

In Python:

```python
tts = ptts.TTS("hf://gradium/phonon-31m-en", lang="en")
tts.set_conditions({"duration_delta": "1.0"})  # Slower pacing
```

## Runtime 2: Hugging Face Transformers / PyTorch

Phonon models are supported in Hugging Face Transformers via the
`GradiumPhononTTSForConditionalGeneration` architecture.

### Key Characteristics

- Pipeline: Standard Hugging Face `AutoProcessor` and chat template workflow.
- Hardware Considerations: The Orange Pi 5 Cortex-A76 cores do not support
  hardware bfloat16 matrix multiplication instructions. Explicitly instantiate
  the model with `torch_dtype=torch.float32` to avoid BLAS fallback warnings
  and maximize CPU execution speed.
- Latency: Inference takes approximately 4 to 5 seconds for short sentences on
  CPU, compared to sub-second speeds with `ptts`.

### Python Transformers Workflow

```python
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from transformers import AutoProcessor, GradiumPhononTTSForConditionalGeneration

model_id = "gradium/phonon-31m-en"

# Load processor and model with float32 for ARM CPU
processor = AutoProcessor.from_pretrained(model_id)
model = GradiumPhononTTSForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
)

# Load speaker voice embedding
voice_file = hf_hub_download(
    repo_id="gradium/phonon-voices",
    filename="voices/LMDIYE0Oa377Qh6Z.safetensors",
)
voice = load_file(voice_file)["speaker_wavs"][0].T.float()

conversation = [
    {
        "role": "user",
        "content": [
            {"type": "audio"},
            {"type": "text", "text": "Hello from Hugging Face Transformers."},
        ],
    }
]

inputs = processor.apply_chat_template(
    conversation,
    tokenize=True,
    return_dict=True,
    add_generation_prompt=True,
    processor_kwargs={"audio_prompt_latents": [voice]},
)

outputs = model.generate(**inputs)
audio = processor.decode(outputs.audio_latents, outputs.audio_latents_mask)
processor.save_audio(audio, "speech.wav")
```

## Runtime Summary Table

| Metric | ptts Runtime | Hugging Face Transformers |
|---|---|---|
| Primary Language | Rust (wheel wrapper) | Python / PyTorch |
| Heavy Dependencies | None | PyTorch, Transformers, Accelerate |
| Quantization | q8, q6, q5, q4, f32 | float32, bfloat16 |
| Synthesis Latency (3s audio) | ~0.5 to 1.1 seconds | ~4.8 to 5.5 seconds |
| Recommended Use | Production on SBC | Research / Pipeline Integration |

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
