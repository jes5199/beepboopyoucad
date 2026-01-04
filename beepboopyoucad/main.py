"""
Main entry point for Beep Boop You CAD game
"""
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_command_prefix() -> str:
    """Detect if we're running via 'uv run' and return appropriate prefix"""
    # Check if running inside a uv-managed venv in the current project
    venv = os.environ.get("VIRTUAL_ENV", "")
    cwd = os.getcwd()
    if venv and Path(venv).parent == Path(cwd):
        return "uv run "
    return ""

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
  %(prog)s "A robot dancing in the rain"
  %(prog)s "A cat wearing a top hat" --style "watercolor painting"
  %(prog)s --continue output/game_xxx.json

Environment Variables:
  ANTHROPIC_API_KEY - Required: Your Anthropic API key for Claude
  GOOGLE_API_KEY    - Required: Your Google API key for Gemini
        """
    )

    parser.add_argument(
        "sentence",
        nargs="?",
        type=str,
        help="Starting sentence for a new game"
    )

    parser.add_argument(
        "--style",
        type=str,
        default="a very hasty and sloppy pencil sketch",
        help="Art style for image generation (default: 'a very hasty and sloppy pencil sketch')"
    )

    parser.add_argument(
        "--describe",
        type=str,
        default="Caption this. Keep it terse, like a New Yorker cartoon, but more creative. Avoid cliches.",
        help="Prompt for Claude when describing images"
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

    default_describe = "Caption this. Keep it terse, like a New Yorker cartoon, but more creative. Avoid cliches."

    # Validate arguments
    if args.continue_game:
        if args.sentence:
            print("❌ Error: Cannot provide a sentence when using --continue")
            return 1
        if args.style != "a very hasty and sloppy pencil sketch":
            print("❌ Error: Cannot specify --style when using --continue (style is saved in the game file)")
            return 1
        if args.describe != default_describe:
            print("❌ Error: Cannot specify --describe when using --continue (describe is saved in the game file)")
            return 1

    if not args.continue_game and not args.sentence:
        print("❌ Error: Must provide a sentence to start a new game, or --continue to resume")
        parser.print_help()
        return 1

    # Check for required API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Please set it in your .env file or environment")
        return 1

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set")
        print("   Image generation will use placeholder images")

    try:
        cmd_prefix = get_command_prefix()

        if args.continue_game:
            # Continue existing game
            game_file = Path(args.continue_game)
            if not game_file.exists():
                print(f"❌ Error: Game file not found: {game_file}")
                return 1
            game = Game.load(str(game_file), cmd_prefix=cmd_prefix)
            print(f"📂 Loaded game: {game.game_id} ({len(game.rounds)} rounds played)")
        else:
            # Start new game with user's sentence
            game = Game(output_dir=args.output, style=args.style, describe=args.describe, cmd_prefix=cmd_prefix)
            game.start(args.sentence)
            print(f"🎮 Started new game: {game.game_id}")

        print()
        game.play_round()
        game.print_summary()
        game.print_continue_command()
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
