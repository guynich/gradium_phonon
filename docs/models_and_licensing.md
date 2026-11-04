# Models, Weights, and Licensing

This document outlines the Gradium Phonon model variants, licensing terms,
access requirements, and available voice embeddings.

## Phonon Model Variants

Gradium distributes Phonon in two primary parameter sizes:

1. `gradium/phonon-31m-en`
   - Parameters: 31 Million
   - Size: ~64.5 MB quantized (q8), ~41 MB safetensors
   - Language: English
   - License: Apache 2.0 (Permissive Open Source)
   - Access: Open / Ungated (no login or token required)

2. `gradium/phonon-40m-en` / `gradium/phonon-40m-multilingual`
   - Parameters: 40 Million
   - Size: ~74.6 MB quantized (q8)
   - Languages: English, French, German, Spanish, Portuguese
   - License: Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)
   - Access: Gated Repository (requires license agreement on Hugging Face)

## Accessing Gated 40M Checkpoints

Attempting to download `gradium/phonon-40m-en` or other 40M models without
accepting the license will produce an HTTP 403 Forbidden error:

`Cannot access gated repo for url ... Access to model gradium/phonon-40m-en is restricted.`

### How to Enable 40M Access

1. Open your browser and navigate to the Hugging Face model repository:
   https://huggingface.co/gradium/phonon-40m-en
2. Review the CC BY-NC 4.0 terms and click "Agree and access repository".
3. Authenticate locally on the Orange Pi 5:
   ```bash
   ~/venv/phonon/bin/huggingface-cli login
   ```
   Or export your Hugging Face access token:
   ```bash
   export HF_TOKEN="your_hf_token"
   ```
4. Once authorized, the `ptts` CLI and Hugging Face pipelines will authenticate
   automatically using the cached token at `~/.cache/huggingface/token`.

## Voice Embeddings (gradium/phonon-voices)

Phonon uses speaker latent representations rather than training separate
weights for each voice. The voice embeddings are distributed in safetensors
format under `gradium/phonon-voices`.

Catalog voices include:

- `Easton` (`voices/LMDIYE0Oa377Qh6Z.safetensors`): Punchy, crisp consonant attack.
- `Zoey` (`voices/NbpkqMVS3CJeq2j8.safetensors`): Upbeat American accent.
- `Juniper` (`voices/NIWIOv5vTi5eRMj8.safetensors`): Cheerful resonance, personable.
- `Harper` (`voices/4SZHfMpw-p46Ywgs.safetensors`): Modern and friendly American accent.

In the `ptts` runtime, voices can be referenced directly by name:

```bash
~/venv/phonon/bin/ptts --voice Easton "Speech synthesis test."
```

In Hugging Face Transformers, download the corresponding voice safetensors file
and supply it to `audio_prompt_latents`.

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
