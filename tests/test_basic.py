"""
Basic smoke tests for beepboopyoucad package
"""
import os
import sys
from pathlib import Path


def test_package_imports():
    """Test that all modules can be imported"""
    import beepboopyoucad
    from beepboopyoucad import claude_client
    from beepboopyoucad import google_client
    from beepboopyoucad import game
    from beepboopyoucad import main
    
    assert beepboopyoucad.__version__ == "0.1.0"
    print("✓ All modules imported successfully")


def test_client_initialization_without_keys():
    """Test that clients raise appropriate errors when API keys are missing"""
    from beepboopyoucad.claude_client import ClaudeClient
    from beepboopyoucad.google_client import NanoBananaClient
    
    # Save original env vars
    orig_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    orig_google_key = os.environ.get("GOOGLE_API_KEY")
    
    try:
        # Clear keys
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        
        # Test Claude client
        try:
            claude = ClaudeClient()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "ANTHROPIC_API_KEY" in str(e)
            print("✓ Claude client properly validates API key")
        
        # Test Banana client (now uses Gemini)
        try:
            banana = NanoBananaClient()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "GOOGLE_API_KEY" in str(e)
            print("✓ Banana client properly validates API key")
            
    finally:
        # Restore env vars
        if orig_anthropic_key:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic_key
        if orig_google_key:
            os.environ["GOOGLE_API_KEY"] = orig_google_key


def test_game_initialization():
    """Test that Game can be initialized with API keys"""
    from beepboopyoucad.game import Game, GameRound
    
    # Set dummy API keys
    os.environ["ANTHROPIC_API_KEY"] = "test_key_anthropic"
    os.environ["GOOGLE_API_KEY"] = "test_key_google"
    
    try:
        game = Game(output_dir="/tmp/test_game_output")
        assert game.output_dir.name == "test_game_output"
        assert len(game.rounds) == 0
        print("✓ Game initializes correctly")
        
        # Test GameRound
        round_data = GameRound(1, "text", "A test sentence")
        assert round_data.round_num == 1
        assert round_data.content_type == "text"
        assert round_data.content == "A test sentence"
        
        round_dict = round_data.to_dict()
        assert "round" in round_dict
        assert "type" in round_dict
        assert "content" in round_dict
        print("✓ GameRound works correctly")
        
    finally:
        # Clean up
        if "ANTHROPIC_API_KEY" in os.environ and os.environ["ANTHROPIC_API_KEY"] == "test_key_anthropic":
            del os.environ["ANTHROPIC_API_KEY"]
        if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"] == "test_key_google":
            del os.environ["GOOGLE_API_KEY"]


def test_placeholder_image_generation():
    """Test that placeholder image generation works"""
    from beepboopyoucad.google_client import NanoBananaClient
    import tempfile

    os.environ["GOOGLE_API_KEY"] = "test_key"

    try:
        client = NanoBananaClient()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_image.png"
            result = client._create_placeholder_image("Test prompt", str(output_path))

            assert Path(result).exists()
            assert Path(result).suffix == ".png"
            print("✓ Placeholder image generation works")

    finally:
        if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"] == "test_key":
            del os.environ["GOOGLE_API_KEY"]


if __name__ == "__main__":
    print("Running beepboopyoucad tests...\n")
    
    test_package_imports()
    test_client_initialization_without_keys()
    test_game_initialization()
    test_placeholder_image_generation()
    
    print("\n✅ All tests passed!")
