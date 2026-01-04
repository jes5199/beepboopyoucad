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
  %(prog)s --rounds 5
  %(prog)s --rounds 7 --output my_game
  
Environment Variables:
  ANTHROPIC_API_KEY - Required: Your Anthropic API key for Claude
  GOOGLE_API_KEY    - Required: Your Google API key for Gemini
        """
    )
    
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of rounds to play (default: 5, should be odd to end on text)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for game results (default: output)"
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
        # Create and run the game
        game = Game(output_dir=args.output)
        game.play(num_rounds=args.rounds)
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
