"""
Audio generation functions using ElevenLabs API.
Converts script segments to speech and merges them into a single podcast.
"""

from restack_ai.function import function, log
import requests
import base64
import io
import os

@function.defn()
async def generate_audio_segment(input: dict) -> dict:
    """
    Generate audio for a single script segment using ElevenLabs.

    Args:
        input (dict): A dictionary containing:
            - text (str): The text to convert to speech
            - voice_id (str): ElevenLabs voice ID to use
            - api_key (str, optional): ElevenLabs API key

    Returns:
        dict: A dictionary containing base64-encoded audio
    """
    try:
        log.info("generate_audio_segment started", text_preview=input.get("text", "")[:50])

        # Extract input parameters
        text = input.get("text", "")
        voice_id = input.get("voice_id", "")
        api_key = input.get("api_key") or os.getenv("ELEVEN_LABS_API_KEY")

        # Validate input
        if not text:
            raise ValueError("Text is empty")
        if not voice_id:
            raise ValueError("Voice ID is missing")
        if not api_key:
            raise ValueError("ElevenLabs API key is missing")

        # Prepare request
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }

        # Send the request
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        # Collect response and encode to base64
        content = b''.join(response.iter_content(chunk_size=1024))
        base64_audio = base64.b64encode(content).decode('utf-8')

        log.info("Audio segment generated successfully", audio_size=len(base64_audio))

        return {
            "audio_base64": base64_audio,
            "text": text,
            "voice_id": voice_id
        }

    except Exception as e:
        log.error("generate_audio_segment failed", error=str(e))
        raise e


@function.defn()
async def merge_audio_segments(input: dict) -> dict:
    """
    Merge multiple audio segments into a single podcast file.

    Args:
        input (dict): A dictionary containing:
            - segments (list): List of base64-encoded audio segments
            - output_filename (str, optional): Output filename

    Returns:
        dict: A dictionary containing the merged audio file path and base64
    """
    try:
        log.info("merge_audio_segments started", segment_count=len(input.get("segments", [])))

        segments = input.get("segments", [])
        output_filename = input.get("output_filename", "podcast.mp3")

        if not segments:
            raise ValueError("No segments to merge")

        # Import pydub here to avoid startup overhead
        from pydub import AudioSegment

        # Decode and combine all segments
        combined = AudioSegment.empty()

        for i, segment_data in enumerate(segments):
            # Decode base64 audio
            audio_bytes = base64.b64decode(segment_data)

            # Load audio segment
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))

            # Add a small pause between speakers (300ms)
            if i > 0:
                silence = AudioSegment.silent(duration=300)
                combined += silence

            # Add the audio segment
            combined += audio_segment

            log.info(f"Added segment {i+1}/{len(segments)}")

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        # Save to file
        output_path = os.path.join(output_dir, output_filename)
        combined.export(output_path, format="mp3", bitrate="192k")

        # Also encode to base64 for return
        with open(output_path, "rb") as f:
            final_audio_bytes = f.read()
            final_base64 = base64.b64encode(final_audio_bytes).decode('utf-8')

        duration_seconds = len(combined) / 1000.0  # pydub uses milliseconds

        log.info(
            "Audio merge successful",
            output_path=output_path,
            duration_seconds=duration_seconds
        )

        return {
            "output_path": output_path,
            "audio_base64": final_base64,
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_seconds / 60.0
        }

    except Exception as e:
        log.error("merge_audio_segments failed", error=str(e))
        raise e
