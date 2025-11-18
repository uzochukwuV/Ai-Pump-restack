"""
Voice Preview Script - Test all available voices

This script generates audio previews for all available voices
so you can hear what each voice sounds like before creating a podcast.
"""

import asyncio
import os
import sys
import base64
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client import client
from src.functions.audio_generator import generate_voice_preview
from src.utils.voice_config import VOICE_LIBRARY
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def preview_voice(voice_id: str, voice_name: str, style: str = "casual"):
    """
    Generate and save a voice preview.

    Args:
        voice_id: ElevenLabs voice ID
        voice_name: Descriptive name for the voice
        style: Podcast style for sample text
    """
    print(f"  Generating preview for {voice_name}...")

    try:
        # Call the preview function via Restack
        result = await client.execute_function(
            function_name="generate_voice_preview",
            input={
                "voice_id": voice_id,
                "style": style,
                "api_key": os.getenv("ELEVEN_LABS_API_KEY")
            }
        )

        # Decode base64 audio
        audio_bytes = base64.b64decode(result["audio_base64"])

        # Save to file
        output_dir = Path(os.getcwd()) / "output" / "voice_previews"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{voice_name.replace(' ', '_').lower()}_{style}.mp3"
        output_path = output_dir / filename

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        print(f"    ✅ Saved: {output_path}")
        print(f"    📝 Text: {result['text'][:50]}...")

        return output_path

    except Exception as e:
        print(f"    ❌ Failed: {str(e)}")
        return None


async def preview_all_voices(style: str = "casual"):
    """
    Generate previews for all available voices.

    Args:
        style: Podcast style to use for all previews
    """
    print(f"\n🎙️ Generating Voice Previews (Style: {style})")
    print("=" * 60)

    # Get unique voice IDs from the voice library
    voice_map = {}
    for voice_name, voice_id in VOICE_LIBRARY.items():
        if voice_id not in voice_map.values():
            voice_map[voice_name] = voice_id

    total = len(voice_map)
    print(f"\nFound {total} unique voices to preview\n")

    successful = 0
    failed = 0

    for i, (voice_name, voice_id) in enumerate(voice_map.items(), 1):
        print(f"[{i}/{total}] {voice_name}")
        result = await preview_voice(voice_id, voice_name, style)
        if result:
            successful += 1
        else:
            failed += 1
        print()

    print("=" * 60)
    print(f"\n📊 Results:")
    print(f"  ✅ Successful: {successful}")
    print(f"  ❌ Failed: {failed}")
    print(f"\nPreviews saved to: output/voice_previews/")


async def preview_specific_voice(voice_key: str, style: str = "casual"):
    """
    Preview a specific voice by its key name.

    Args:
        voice_key: Voice key from VOICE_LIBRARY
        style: Podcast style
    """
    if voice_key not in VOICE_LIBRARY:
        print(f"❌ Voice '{voice_key}' not found!")
        print(f"\nAvailable voices:")
        for key in VOICE_LIBRARY.keys():
            print(f"  - {key}")
        return

    voice_id = VOICE_LIBRARY[voice_key]

    print(f"\n🎙️ Previewing: {voice_key}")
    print(f"Style: {style}")
    print(f"Voice ID: {voice_id}")
    print()

    await preview_voice(voice_id, voice_key, style)


async def interactive_preview():
    """
    Interactive mode - let user choose what to preview.
    """
    print("\n" + "=" * 60)
    print("🎙️  Voice Preview Tool")
    print("=" * 60)

    # Check API key
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        print("\n❌ ELEVEN_LABS_API_KEY not found in environment!")
        print("Please set it in your .env file and try again.")
        return

    print("\n✅ ElevenLabs API Key found")

    print("\nWhat would you like to do?")
    print("1) Preview ALL voices (casual style)")
    print("2) Preview ALL voices (professional style)")
    print("3) Preview ALL voices (energetic style)")
    print("4) Preview a specific voice")
    print("5) Exit")

    choice = input("\nEnter choice [1-5]: ").strip()

    if choice == "1":
        await preview_all_voices("casual")
    elif choice == "2":
        await preview_all_voices("professional")
    elif choice == "3":
        await preview_all_voices("energetic")
    elif choice == "4":
        print("\nAvailable voices:")
        for i, key in enumerate(VOICE_LIBRARY.keys(), 1):
            print(f"  {i}. {key}")

        voice_key = input("\nEnter voice name: ").strip()
        style = input("Enter style (casual/professional/educational/energetic) [casual]: ").strip() or "casual"
        await preview_specific_voice(voice_key, style)
    elif choice == "5":
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Preview ElevenLabs voices")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Preview all voices"
    )
    parser.add_argument(
        "--voice",
        type=str,
        help="Preview specific voice by key name"
    )
    parser.add_argument(
        "--style",
        type=str,
        default="casual",
        choices=["casual", "professional", "educational", "energetic"],
        help="Podcast style for preview text"
    )

    args = parser.parse_args()

    if args.all:
        await preview_all_voices(args.style)
    elif args.voice:
        await preview_specific_voice(args.voice, args.style)
    else:
        # Interactive mode
        await interactive_preview()


if __name__ == "__main__":
    asyncio.run(main())
