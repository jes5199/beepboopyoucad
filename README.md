# beepboopyoucad

**Beep Boop You CAD** - Robots play "picture sentence picture" / "paper telephone" / "eat poop you cat"!

A collaborative game where Claude (Anthropic AI) and Nano Banana (image generation AI) play a version of the classic game "Eat Poop You Cat" by alternating between text descriptions and images.

## How It Works

1. **Claude** generates an initial creative sentence
2. **Nano Banana** draws an image based on that sentence
3. **Claude** describes what it sees in the image
4. **Nano Banana** draws the new description
5. Continue alternating...

Watch as the message transforms through each AI's interpretation!

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites

- Python 3.12 or higher
- uv package manager
- Anthropic API key (for Claude)
- Banana.dev API key (for Nano Banana image generation)

### Install uv (if not already installed)

```bash
pip install uv
```

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
- **Banana.dev API**: https://www.banana.dev/

## Usage

Run the game with default settings (5 rounds):

```bash
uv run beepboopyoucad
```

Or specify the number of rounds:

```bash
uv run beepboopyoucad --rounds 7
```

Specify a custom output directory:

```bash
uv run beepboopyoucad --rounds 5 --output my_game_results
```

### Try the Demo

To see how the game works without API keys, run the demo:

```bash
uv run python demo.py
```

This will create a simulated game showing the flow from text to image and back.

## Output

The game creates:
- Images for each drawing round (`.png` files)
- A JSON file with the complete game history
- Console output showing the progression

All outputs are saved in the `output/` directory (or your specified directory).

## Example

```
🎮 Starting 'Beep Boop You CAD' game!
============================================================

[Round 1] Claude generates initial sentence...
📝 Sentence: A purple elephant wearing sunglasses rides a skateboard through a busy city street.

[Round 2] Nano Banana draws the sentence...
🎨 Image saved: output/round_2_20240104_120000.png

[Round 3] Claude describes the image...
📝 Description: A large gray mammal balancing on a wheeled board amid tall buildings.

[Round 4] Nano Banana draws the sentence...
🎨 Image saved: output/round_4_20240104_120030.png

[Round 5] Claude describes the image...
📝 Description: An abstract creature navigating an urban landscape.

============================================================
🎉 Game complete!
```

## Development

Run with Python directly:

```bash
uv run python -m beepboopyoucad.main --rounds 5
```

## License

MIT

## Credits

Inspired by the classic party game "Eat Poop You Cat" / "Paper Telephone" / "Picture Sentence Picture"

