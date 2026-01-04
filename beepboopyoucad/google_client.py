"""
Nano Banana integration for image generation using Google Gemini
"""
import os
from pathlib import Path

from google import genai


class NanoBananaClient:
    """Client for interacting with Gemini image generation"""

    def __init__(self, api_key: str | None = None):
        """
        Initialize Gemini client

        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY env var
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set")

        self.client = genai.Client(api_key=self.api_key)

    def generate_image(self, prompt: str, output_path: str, style: str | None = None) -> str:
        """
        Generate an image from a text prompt

        Args:
            prompt: Text description to generate image from
            output_path: Path where to save the generated image
            style: Optional art style for the image

        Returns:
            Path to the saved image
        """
        # Format prompt with XML tags
        if style:
            formatted_prompt = f"<style>{style}</style><prompt>{prompt}</prompt>"
        else:
            formatted_prompt = f"<prompt>{prompt}</prompt>"

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[formatted_prompt],
            )

            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    image.save(output_path)
                    return output_path

            # If no image was returned, fall back to placeholder
            print("Warning: No image in API response, creating placeholder image")
            return self._create_placeholder_image(prompt, output_path)

        except Exception as e:
            # Fallback: Create a placeholder image with PIL
            print(f"Warning: Gemini API call failed ({e}), creating placeholder image")
            return self._create_placeholder_image(prompt, output_path)

    def _create_placeholder_image(self, prompt: str, output_path: str) -> str:
        """
        Create a placeholder image when API is unavailable

        Args:
            prompt: The prompt text to display
            output_path: Where to save the image

        Returns:
            Path to the saved image
        """
        from PIL import Image, ImageDraw
        import textwrap

        # Create a simple image with the prompt text
        img = Image.new('RGB', (512, 512), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)

        # Wrap text
        lines = textwrap.wrap(prompt, width=40)

        # Draw text
        y_text = 200
        for line in lines[:5]:  # Max 5 lines
            bbox = draw.textbbox((0, 0), line)
            width = bbox[2] - bbox[0]
            draw.text(((512 - width) / 2, y_text), line, fill=(0, 0, 0))
            y_text += 30

        # Save the image
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        return output_path
