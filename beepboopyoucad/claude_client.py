"""
Claude integration for text generation and image description
"""
import os
from anthropic import Anthropic


class ClaudeClient:
    """Client for interacting with Claude AI"""
    
    def __init__(self, api_key: str | None = None):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = Anthropic(api_key=self.api_key)
    
    def generate_initial_sentence(self) -> str:
        """
        Generate an initial sentence to start the game
        
        Returns:
            A creative sentence suitable for illustration
        """
        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Generate a single creative, visual sentence that would be fun to illustrate. It should be concrete and imaginative. Just output the sentence, nothing else."
            }]
        )
        return response.content[0].text.strip()
    
    def describe_image(self, image_path: str, prompt: str | None = None) -> str:
        """
        Describe what Claude sees in an image

        Args:
            image_path: Path to the image file
            prompt: Custom prompt for describing the image

        Returns:
            A sentence describing what Claude sees in the image
        """
        import base64
        from pathlib import Path

        if prompt is None:
            prompt = "Describe what you see in this image in a single sentence. Be concrete and specific. Just output the sentence, nothing else."

        # Read and encode the image
        image_data = Path(image_path).read_bytes()
        base64_image = base64.b64encode(image_data).decode("utf-8")

        # Determine media type
        extension = Path(image_path).suffix.lower()
        media_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        media_type = media_type_map.get(extension, "image/jpeg")

        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }]
        )
        return response.content[0].text.strip()
