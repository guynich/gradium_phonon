# Voice Options and Catalog Reference

Gradium Phonon includes a catalog of 102 preset voices across 5 languages:
English (37), Spanish (25), French (15), German (13), and Portuguese (12).

## Listing Available Voices

To list all available voices from the command line using the runtime:

```bash
~/venv/phonon/bin/ptts --list-voices
```

In Python:

```python
import ptts

voices = ptts.catalog_voices()
for voice in voices:
    print(f"{voice['name']} ({voice['language']}): {voice['voice_id']}")
```

## Selecting a Voice

In `ptts` (CLI and scripts), pass the voice by its catalog name:

```bash
~/venv/phonon/bin/python src/ptts_speak.py --stream --voice Zoey "Hello from Zoey."
```

In Hugging Face Transformers, voices are loaded from safetensors embeddings
stored in the `gradium/phonon-voices` repository using the voice ID:

```python
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

# Example: loading Easton (voice_id: LMDIYE0Oa377Qh6Z)
voice_path = hf_hub_download(
    repo_id="gradium/phonon-voices",
    filename="voices/LMDIYE0Oa377Qh6Z.safetensors",
)
voice_latents = load_file(voice_path)["speaker_wavs"][0].T.float()
```

## English Voice Catalog Ledger

The following ledger lists the 37 English catalog voices available for use:

| Voice Name | Voice ID | Description |
|---|---|---|
| Zoey | NbpkqMVS3CJeq2j8 | Playful, upbeat and Gen Z energy voice with a standard American accent. |
| Juniper | NIWIOv5vTi5eRMj8 | Cheerful presence with real resonance, personable and decisive. |
| Everly | vjFyp2BcCyTlUmYb | Rounded, soft-edged tone with gentle lift and relaxed delivery. |
| Harper | 4SZHfMpw-p46Ywgs | Modern, confident and friendly voice with a standard American accent. |
| Hadley | bXwrkHhURL1VFJdG | Settled, even-toned and genuinely kind, with crisp consonants. |
| Delia | nGzMHMPAWGaJFHOo | Low, grounded and quick to the point, with sincere delivery. |
| Easton | LMDIYE0Oa377Qh6Z | Punchy and close in, with crisp consonant attack. |
| Micah | 40QrMVgAxFiUnP9f | Buoyant and high in energy, with a playful lift at ends of phrases. |
| Trevor | 0zLApsZfVLLNaEGl | Buoyant energy over a resonant mid-low core. |
| Russell | _6Aslh2DxfmnRLmP | High-energy American adult voice, encouraging and intense. |
| Preston | qIxlZ7Ei8KvWlyQH | Trim, focused delivery with clean edges on every consonant. |
| Miles | d9XCyhjo4JhkHF1d | Resonant and decisive, with wide dynamic range. |
| Maeve | 6PWnV0Nq4wu7RVBT | Sparky, attentive British English adult voice with a smile. |
| Freya | GgfEkEJtxZR7gnpy | Young British voice, glossy and confident with fast chatter. |
| Pippa | uem82D50GRv2Dwma | Confident, upbeat British English adult voice with infectious energy. |
| Elodie-Rose | y9bQqIDnyxwqK01t | Young British voice with sharp, enthusiastic energy and crisp articulation. |
| Imogen | gDT1nz7Ie36ZhL-C | Bubbly, friendly British English adult voice that puts callers at ease. |
| Lottie | m9MxpY6IUGXtWp76 | Sparky and to the point, high forward energy with clean consonant edges. |
| Alfie | X6NceqF285Gr04gb | Punchy and forward British voice with crisp consonant attack. |
| Hugh | YyKcxPG7iIgS3jsK | Soft and close, airy in texture, with lively pitch movement. |
| Edwin | zUCxzrOrugTSis03 | Efficient and firm British voice with tidy articulation. |
| Spencer | JOW0vchyswkQUMDS | Light and airy, sitting higher, with crisp consonants and patient delivery. |
| Toby | dME3IWyZBvmh1n1q | Sparky, attentive British English adult voice for fast customer support. |
| Teddy | Zn7g6NxLqXlJb7Qi | Sparky and close in, quick off the mark, with firm consonants. |
| Bryony | gfP44RlHwr2kEwk7 | Full, rich mid-range tones, softly relaxed and spoken close to the mic. |
| Captain Silas Blackwater | xPDpsV3F592srkjA | Old British West Country pirate captain, deep, gravelly and booming. |
| Morwenna of the Deep | nOykTmcH9ydsGGIc | Low, husky alto, close to the microphone and whispered, intimate and slow. |
| Old Mortlake | lX3LavMNdlIbgEHH | Elderly Victorian gravedigger, low, raspy and half-whispered with pauses. |
| Azgorath | dGyGDKo2osj7h3s7 | Ancient demon, cavernous, impossibly deep bass voice with dry rasping edge. |
| Fennick the Young Elf | cXoIXJ2llS8S0WOW | Curious, kind-hearted elf boy, natural child voice in warm middle range. |
| The Thing Under the Stairs | GXaSqMEmOg12OIYb | Monstrous creature lurking in the dark, gravelly and low-pitched growl. |
| Vyrmathrax the Ancient | xO8xQo3BrB8FuI6J | Ancient dragon, very low and resonant, deep chest weight with gravel. |
| Grub the Ogre | cYtsRSxV5q9IMehn | Good-natured ogre under a bridge, gruff, grainy, rumbling low end. |
| Master Aldric | gSgG5Tor0GPEnqzC | Wise old British wizard, rich and resonant with an aged grain. |
| The Snow Queen | NIWoEurJHMJjyUTe | Regal, cold-hearted queen of ice, crystalline mezzo voice, poised and chill. |
| Sir Bramwell | y2eiKxtQo2B67deU | Pompous English knight, booming, plummy and theatrical with comic wobble. |
| Fairy Godmother | QXNr0SvkukLB4wPq | Kind fairy godmother, low, warm, velvety alto voice, grandmotherly. |

## Development

### Gradium Phonon Orange Pi 5 setup documentation
- `agy --conversation c4011eb4-8157-4348-a885-9dc03f20ff9f`
