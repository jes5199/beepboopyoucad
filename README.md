# beepboopyoucad

**Beep Boop You CAD** - Robots play "picture sentence picture" / "paper telephone" / "eat poop you cat"!

A collaborative game where Claude (Anthropic AI) and Gemini (Google AI) play a version of the classic game "Eat Poop You Cat" by alternating between text descriptions and images.

## How It Works

1. **You** provide an initial sentence
2. **Gemini** draws an image based on that sentence
3. **Claude** describes what it sees in the image
4. **Gemini** draws the new description
5. Continue alternating...

Watch as the message transforms through each AI's interpretation!

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites

- Python 3.12 or higher
- uv package manager
- Anthropic API key (for Claude)
- Google API key (for Gemini image generation)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jes5199/beepboopyoucad.git
cd beepboopyoucad
```

2. Install dependencies:
```bash
uv sync
```

3. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Get your API keys:
- **Anthropic API**: https://console.anthropic.com/
- **Google API**: https://aistudio.google.com/apikey

## Usage

Start a new game with your sentence:

```bash
uv run beepboopyoucad "A robot dancing in the rain"
```

Continue the game (each invocation plays one round):

```bash
uv run beepboopyoucad --continue output/game_20260104_120000.json
```

### Options

```
--style STYLE       Art style for images (default: "a very hasty and sloppy pencil sketch")
--describe PROMPT   Prompt for Claude when describing images
--output DIR        Output directory (default: output)
--continue FILE     Continue a game from a JSON file
```

### Examples

```bash
# Start with custom style
uv run beepboopyoucad "A cat wearing a top hat" --style "watercolor painting"

# Custom describe prompt
uv run beepboopyoucad "A mysterious door" --describe "What story does this image tell?"
```

## Output

The game creates:
- Images for each drawing round (`.png` files)
- A JSON file with the complete game history
- An HTML file showing the full conversation with embedded images
- Console output showing the progression

All outputs are saved in the `output/` directory (or your specified directory).

## Example Session

```
$ uv run beepboopyoucad "A purple elephant wearing sunglasses"
💾 Game saved: output/game_20260104_120000.json
🎮 Started new game: 20260104_120000

🎮 Round 2
============================================================
Nano Banana draws the sentence...
🎨 Image saved: output/round_2_20260104_120000.png
💾 Game saved: output/game_20260104_120000.json
🌐 HTML saved: output/game_20260104_120000.html

📊 Game Summary:
🎨 Style: a very hasty and sloppy pencil sketch
------------------------------------------------------------

Round 1 (Text):
  A purple elephant wearing sunglasses

Round 2 (Image):
  output/round_2_20260104_120000.png

------------------------------------------------------------

▶️  Continue: uv run beepboopyoucad --continue output/game_20260104_120000.json
```

## License

MIT

## Credits

Inspired by the classic party game "Eat Poop You Cat" / "Paper Telephone" / "Picture Sentence Picture"
