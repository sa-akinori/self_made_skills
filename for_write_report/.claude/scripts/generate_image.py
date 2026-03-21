#!/usr/bin/env python3
"""
Generate conceptual/schematic images using Google Gemini API (Nano Banana 2).

Usage:
    python3 generate_image.py "your prompt" output_path.png

Requirements:
    pip install google-genai Pillow

    Set GEMINI_API_KEY environment variable:
    export GEMINI_API_KEY="your_key_here"

    Get a free key at: https://aistudio.google.com/apikey
"""

import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_image.py \"prompt\" output_path.png")
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = sys.argv[2]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print()
        print("Setup instructions:")
        print("  1. Get a free API key from: https://aistudio.google.com/apikey")
        print("  2. Set the environment variable:")
        print('     export GEMINI_API_KEY="your_key_here"')
        print()
        print("  To make it permanent, add to ~/.bashrc or ~/.zshrc:")
        print('     echo \'export GEMINI_API_KEY="your_key_here"\' >> ~/.bashrc')
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("Error: google-genai package is not installed.")
        print("  Run: pip install google-genai Pillow")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Generating image with Nano Banana 2 (gemini-3.1-flash-image-preview)...")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"  Output: {output_path}")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
    )

    saved = False
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(output_path)
            print(f"  Saved: {output_path}")
            saved = True
            break

    if not saved:
        print("Error: No image was returned by the API.")
        print("  The prompt may have been rejected by safety filters.")
        print("  Try rephrasing the prompt.")
        sys.exit(1)


if __name__ == "__main__":
    main()
