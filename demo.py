"""
Demo script that shows the game flow without requiring API keys
"""
import sys
from pathlib import Path

# Add current directory to path so we can import beepboopyoucad
sys.path.insert(0, str(Path(__file__).parent))

from beepboopyoucad.game import GameRound


def demo_game():
    """Run a demo version of the game with mock data"""
    print("🎮 Starting 'Beep Boop You CAD' DEMO!")
    print("=" * 60)
    print("(This is a demo showing the game flow)")
    print("=" * 60)
    
    output_dir = Path("/tmp/beepboopyoucad_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Simulate game rounds
    rounds = []
    
    # Round 1: Initial sentence
    print("\n[Round 1] Claude generates initial sentence...")
    sentence1 = "A purple elephant wearing sunglasses rides a skateboard through a busy city street."
    print(f"📝 Sentence: {sentence1}")
    rounds.append(GameRound(1, "text", sentence1))
    
    # Round 2: Image generation
    print("\n[Round 2] Nano Banana draws the sentence...")
    image_path = output_dir / "round_2_demo.png"
    
    # Create a simple demo image
    from PIL import Image, ImageDraw
    import textwrap
    
    img = Image.new('RGB', (512, 512), color=(230, 230, 250))
    draw = ImageDraw.Draw(img)
    
    # Draw title
    draw.text((20, 20), "Round 2: Image", fill=(100, 100, 100))
    
    # Wrap and draw prompt
    lines = textwrap.wrap(sentence1, width=40)
    y_text = 200
    for line in lines:
        bbox = draw.textbbox((0, 0), line)
        width = bbox[2] - bbox[0]
        draw.text(((512 - width) / 2, y_text), line, fill=(0, 0, 0))
        y_text += 30
    
    img.save(image_path)
    print(f"🎨 Image saved: {image_path}")
    rounds.append(GameRound(2, "image", str(image_path)))
    
    # Round 3: Description
    print("\n[Round 3] Claude describes the image...")
    sentence2 = "A large gray mammal with accessories balances on a wheeled board amid tall buildings."
    print(f"📝 Description: {sentence2}")
    rounds.append(GameRound(3, "text", sentence2))
    
    # Round 4: Image generation
    print("\n[Round 4] Nano Banana draws the sentence...")
    image_path2 = output_dir / "round_4_demo.png"
    
    img2 = Image.new('RGB', (512, 512), color=(250, 240, 230))
    draw2 = ImageDraw.Draw(img2)
    draw2.text((20, 20), "Round 4: Image", fill=(100, 100, 100))
    
    lines2 = textwrap.wrap(sentence2, width=40)
    y_text = 200
    for line in lines2:
        bbox = draw2.textbbox((0, 0), line)
        width = bbox[2] - bbox[0]
        draw2.text(((512 - width) / 2, y_text), line, fill=(0, 0, 0))
        y_text += 30
    
    img2.save(image_path2)
    print(f"🎨 Image saved: {image_path2}")
    rounds.append(GameRound(4, "image", str(image_path2)))
    
    # Round 5: Final description
    print("\n[Round 5] Claude describes the image...")
    sentence3 = "An abstract creature with equipment navigates an urban landscape with geometric structures."
    print(f"📝 Description: {sentence3}")
    rounds.append(GameRound(5, "text", sentence3))
    
    print("\n" + "=" * 60)
    print("🎉 Demo complete!")
    
    # Print summary
    print("\n📊 Game Summary:")
    print("-" * 60)
    
    for round_data in rounds:
        if round_data.content_type == "text":
            print(f"\nRound {round_data.round_num} (Text):")
            print(f"  {round_data.content}")
        else:
            print(f"\nRound {round_data.round_num} (Image):")
            print(f"  {round_data.content}")
    
    print("\n" + "-" * 60)
    print("\n🔄 Transformation:")
    print(f"  Started with: {rounds[0].content}")
    print(f"  Ended with:   {rounds[-1].content}")
    
    print(f"\n💾 Demo outputs saved to: {output_dir}")
    print("\n✨ To play with real AI, set up your API keys in .env and run:")
    print("   uv run beepboopyoucad --rounds 5")


if __name__ == "__main__":
    demo_game()
