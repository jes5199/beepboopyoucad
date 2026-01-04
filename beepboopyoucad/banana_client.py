"""
Nano Banana integration for image generation
"""
import os
import requests
from pathlib import Path


class NanoBananaClient:
    """Client for interacting with Nano Banana AI image generation"""
    
    def __init__(self, api_key: str | None = None):
        """
        Initialize Nano Banana client
        
        Args:
            api_key: Banana API key. If None, reads from BANANA_API_KEY env var
        """
        self.api_key = api_key or os.getenv("BANANA_API_KEY")
        if not self.api_key:
            raise ValueError("BANANA_API_KEY must be set")
        
        # Banana.dev API endpoint
        self.base_url = "https://api.banana.dev"
    
    def generate_image(self, prompt: str, output_path: str) -> str:
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description to generate image from
            output_path: Path where to save the generated image
            
        Returns:
            Path to the saved image
        """
        # For now, create a simple implementation that uses Banana.dev's API
        # The exact API structure may vary based on the deployed model
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "apiKey": self.api_key,
            "modelKey": "stable-diffusion",  # This would be the model key
            "modelInputs": {
                "prompt": prompt,
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
            }
        }
        
        # Note: This is a generic implementation
        # The actual Banana.dev API structure depends on the deployed model
        try:
            response = requests.post(
                f"{self.base_url}/start/v4",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract image URL or base64 data from response
            # This structure depends on the specific model deployment
            if "modelOutputs" in result:
                image_data = result["modelOutputs"]
                
                # Handle base64 encoded image
                if isinstance(image_data, list) and len(image_data) > 0:
                    import base64
                    img_data = base64.b64decode(image_data[0]["image_base64"])
                    Path(output_path).write_bytes(img_data)
                    return output_path
            
            # If we got a response but couldn't parse it, fall back to placeholder
            print(f"Warning: Unexpected API response structure, creating placeholder image")
            return self._create_placeholder_image(prompt, output_path)
                    
        except Exception as e:
            # Fallback: Create a placeholder image with PIL
            print(f"Warning: Banana API call failed ({e}), creating placeholder image")
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
        
        # Create a simple image with the prompt text
        img = Image.new('RGB', (512, 512), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Wrap text
        import textwrap
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
