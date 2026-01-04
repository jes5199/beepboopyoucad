"""
Main entry point for Beep Boop You CAD game
"""
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

from .game import Game


def main():
    """Main CLI entry point"""
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Play 'Beep Boop You CAD' - a picture sentence picture game with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s                           # Start a new game (round 1)
  %(prog)s --continue output/game_xxx.json  # Continue an existing game

Environment Variables:
  ANTHROPIC_API_KEY - Required: Your Anthropic API key for Claude
  GOOGLE_API_KEY    - Required: Your Google API key for Gemini
        """
    )

    parser.add_argument(
        "--continue",
        dest="continue_game",
        type=str,
        metavar="FILE",
        help="Continue a game from a JSON file"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for new games (default: output)"
    )

    args = parser.parse_args()

    # Check for required API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Please set it in your .env file or environment")
        return 1

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set")
        print("   Image generation will use placeholder images")

    try:
        if args.continue_game:
            # Continue existing game
            game_file = Path(args.continue_game)
            if not game_file.exists():
                print(f"❌ Error: Game file not found: {game_file}")
                return 1
            game = Game.load(str(game_file))
            print(f"📂 Loaded game: {game.game_id} ({len(game.rounds)} rounds played)")
        else:
            # Start new game
            game = Game(output_dir=args.output)
            print(f"🎮 Starting new game: {game.game_id}")

        print()
        game.play_round()
        game.print_summary()
        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Game interrupted by user")
        return 130

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
