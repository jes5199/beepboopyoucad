"""
Game engine for "Eat Poop You Cat" / "Picture Sentence Picture"
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json

from .claude_client import ClaudeClient
from .google_client import NanoBananaClient


class GameRound:
    """Represents a single round in the game"""

    def __init__(self, round_num: int, content_type: str, content: str, timestamp: str | None = None):
        self.round_num = round_num
        self.content_type = content_type  # "text" or "image"
        self.content = content  # sentence or image path
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "round": self.round_num,
            "type": self.content_type,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "GameRound":
        return cls(
            round_num=data["round"],
            content_type=data["type"],
            content=data["content"],
            timestamp=data.get("timestamp")
        )


class Game:
    """Main game controller for Picture Sentence Picture"""

    def __init__(self, output_dir: str = "output", game_id: str | None = None, style: str | None = None, describe: str | None = None, cmd_prefix: str = ""):
        """
        Initialize the game

        Args:
            output_dir: Directory to save game outputs
            game_id: Existing game ID (for continuing a game)
            style: Art style for image generation
            describe: Prompt for Claude when describing images
            cmd_prefix: Command prefix for continue instructions (e.g., "uv run ")
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.claude = ClaudeClient()
        self.banana = NanoBananaClient()

        self.rounds: List[GameRound] = []
        self.game_id = game_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.style = style
        self.describe = describe
        self.cmd_prefix = cmd_prefix

    @classmethod
    def load(cls, game_file: str, cmd_prefix: str = "") -> "Game":
        """
        Load a game from a JSON file

        Args:
            game_file: Path to the game JSON file
            cmd_prefix: Command prefix for continue instructions

        Returns:
            Game instance with loaded state
        """
        game_path = Path(game_file)
        with open(game_path) as f:
            data = json.load(f)

        game = cls(
            output_dir=str(game_path.parent),
            game_id=data["game_id"],
            style=data.get("style"),
            describe=data.get("describe"),
            cmd_prefix=cmd_prefix
        )
        game.rounds = [GameRound.from_dict(r) for r in data["rounds"]]
        return game

    def start(self, sentence: str):
        """
        Start a new game with the given sentence

        Args:
            sentence: The initial sentence to start the game
        """
        self.rounds.append(GameRound(1, "text", sentence))
        self._save_game_history()

    def play_round(self) -> bool:
        """
        Play a single round of the game

        Returns:
            True if game can continue, False if game is complete
        """
        if len(self.rounds) == 0:
            print("❌ Error: Game not started. Call start() first.")
            return False

        last_round = self.rounds[-1]
        round_num = len(self.rounds) + 1

        print(f"🎮 Round {round_num}")
        print("=" * 60)

        if last_round.content_type == "text":
            # Text -> Image
            print("Nano Banana draws the sentence...")
            image_path = self.output_dir / f"round_{round_num}_{self.game_id}.png"

            self.banana.generate_image(last_round.content, str(image_path), style=self.style)
            print(f"🎨 Image saved: {image_path}")
            self.rounds.append(GameRound(round_num, "image", str(image_path)))

        else:
            # Image -> Text
            print("Claude describes the image...")
            description = self.claude.describe_image(last_round.content, prompt=self.describe)
            print(f"📝 Description: {description}")
            self.rounds.append(GameRound(round_num, "text", description))

        # Save after each round
        self._save_game_history()

        return True

    def _save_game_history(self):
        """Save the game history to a JSON file"""
        history_file = self.output_dir / f"game_{self.game_id}.json"
        history = {
            "game_id": self.game_id,
            "style": self.style,
            "describe": self.describe,
            "rounds": [r.to_dict() for r in self.rounds]
        }

        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)

        print(f"💾 Game saved: {history_file}")

    def print_summary(self):
        """Print a summary of the game progression"""
        print("\n📊 Game Summary:")
        if self.style:
            print(f"🎨 Style: {self.style}")
        print("-" * 60)

        for round_data in self.rounds:
            if round_data.content_type == "text":
                print(f"\nRound {round_data.round_num} (Text):")
                print(f"  {round_data.content}")
            else:
                print(f"\nRound {round_data.round_num} (Image):")
                print(f"  {round_data.content}")

        print("\n" + "-" * 60)

        if len(self.rounds) >= 2:
            print("\n🔄 Transformation:")
            print(f"  Started with: {self.rounds[0].content}")
            print(f"  Ended with:   {self.rounds[-1].content}")

    def print_continue_command(self):
        """Print the command to continue this game"""
        history_file = self.output_dir / f"game_{self.game_id}.json"
        print(f"\n▶️  Continue: {self.cmd_prefix}beepboopyoucad --continue {history_file}")

    def save_html(self):
        """Save an HTML file showing the game conversation"""
        import base64

        html_file = self.output_dir / f"game_{self.game_id}.html"

        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<title>Beep Boop You CAD - Game {self.game_id}</title>",
            "<style>",
            "body { font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }",
            "h1 { text-align: center; color: #333; }",
            ".round { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }",
            ".round-num { color: #666; font-size: 0.9em; margin-bottom: 10px; }",
            ".text { font-size: 1.4em; font-style: italic; color: #333; }",
            ".image { text-align: center; }",
            ".image img { max-width: 100%; border-radius: 4px; }",
            ".meta { color: #999; font-size: 0.8em; margin-top: 20px; text-align: center; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>Beep Boop You CAD</h1>",
        ]

        if self.style:
            html_parts.append(f"<p style='text-align:center;color:#666;'>Style: {self.style}</p>")

        for round_data in self.rounds:
            html_parts.append("<div class='round'>")
            html_parts.append(f"<div class='round-num'>Round {round_data.round_num}</div>")

            if round_data.content_type == "text":
                html_parts.append(f"<div class='text'>\"{round_data.content}\"</div>")
            else:
                # Embed image as base64
                try:
                    image_path = Path(round_data.content)
                    if image_path.exists():
                        image_data = image_path.read_bytes()
                        b64 = base64.b64encode(image_data).decode('utf-8')
                        ext = image_path.suffix.lower()
                        mime = "image/png" if ext == ".png" else "image/jpeg"
                        html_parts.append(f"<div class='image'><img src='data:{mime};base64,{b64}'></div>")
                    else:
                        html_parts.append(f"<div class='image'>[Image: {round_data.content}]</div>")
                except Exception:
                    html_parts.append(f"<div class='image'>[Image: {round_data.content}]</div>")

            html_parts.append("</div>")

        html_parts.extend([
            f"<div class='meta'>Game ID: {self.game_id}</div>",
            "</body>",
            "</html>"
        ])

        html_file.write_text("\n".join(html_parts))
        print(f"🌐 HTML saved: {html_file}")
