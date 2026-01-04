"""
Game engine for "Eat Poop You Cat" / "Picture Sentence Picture"
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json

from .claude_client import ClaudeClient
from .banana_client import NanoBananaClient


class GameRound:
    """Represents a single round in the game"""
    
    def __init__(self, round_num: int, content_type: str, content: str):
        self.round_num = round_num
        self.content_type = content_type  # "text" or "image"
        self.content = content  # sentence or image path
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "round": self.round_num,
            "type": self.content_type,
            "content": self.content,
            "timestamp": self.timestamp
        }


class Game:
    """Main game controller for Picture Sentence Picture"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the game
        
        Args:
            output_dir: Directory to save game outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.claude = ClaudeClient()
        self.banana = NanoBananaClient()
        
        self.rounds: List[GameRound] = []
        self.game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def play(self, num_rounds: int = 5):
        """
        Play the game for a specified number of rounds
        
        Args:
            num_rounds: Number of rounds to play (must be odd to end on text)
        """
        print("🎮 Starting 'Beep Boop You CAD' game!")
        print("=" * 60)
        
        # Round 1: Claude generates initial sentence
        print("\n[Round 1] Claude generates initial sentence...")
        sentence = self.claude.generate_initial_sentence()
        print(f"📝 Sentence: {sentence}")
        self.rounds.append(GameRound(1, "text", sentence))
        
        # Alternate between image and text
        for round_num in range(2, num_rounds + 1):
            print(f"\n[Round {round_num}] ", end="")
            
            if round_num % 2 == 0:  # Even rounds: text -> image
                print("Nano Banana draws the sentence...")
                previous_text = self.rounds[-1].content
                image_path = self.output_dir / f"round_{round_num}_{self.game_id}.png"
                
                self.banana.generate_image(previous_text, str(image_path))
                print(f"🎨 Image saved: {image_path}")
                self.rounds.append(GameRound(round_num, "image", str(image_path)))
                
            else:  # Odd rounds: image -> text
                print("Claude describes the image...")
                previous_image = self.rounds[-1].content
                description = self.claude.describe_image(previous_image)
                print(f"📝 Description: {description}")
                self.rounds.append(GameRound(round_num, "text", description))
        
        # Save game history
        self._save_game_history()
        
        print("\n" + "=" * 60)
        print("🎉 Game complete!")
        self._print_summary()
    
    def _save_game_history(self):
        """Save the game history to a JSON file"""
        history_file = self.output_dir / f"game_{self.game_id}.json"
        history = {
            "game_id": self.game_id,
            "rounds": [r.to_dict() for r in self.rounds]
        }
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
        
        print(f"\n💾 Game history saved: {history_file}")
    
    def _print_summary(self):
        """Print a summary of the game progression"""
        print("\n📊 Game Summary:")
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
