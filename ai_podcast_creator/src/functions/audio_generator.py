"""
Audio generation functions using ElevenLabs API.
Converts script segments to speech and merges them into a single podcast.
"""

from restack_ai.function import function, log
import requests
import base64
import io
import os
from typing import Dict

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
            - background_music (str, optional): Background music track ID
            - music_volume (float, optional): Music volume (0.0-1.0), default 0.25

    Returns:
        dict: A dictionary containing the merged audio file path and base64
    """
    try:
        log.info("merge_audio_segments started", segment_count=len(input.get("segments", [])))

        segments = input.get("segments", [])
        output_filename = input.get("output_filename", "podcast.mp3")
        background_music = input.get("background_music")
        music_volume = input.get("music_volume", 0.25)  # 25% volume by default

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

        # Add background music if requested
        if background_music:
            log.info(f"Adding background music: {background_music}")
            combined = await _add_background_music(
                voice_audio=combined,
                music_track_id=background_music,
                music_volume=music_volume
            )

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
            duration_seconds=duration_seconds,
            background_music=background_music
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


async def _add_background_music(voice_audio, music_track_id: str, music_volume: float):
    """
    Add background music to voice audio.

    Args:
        voice_audio: AudioSegment with voice content
        music_track_id: ID of the music track to use
        music_volume: Volume level for music (0.0-1.0)

    Returns:
        AudioSegment with background music mixed in
    """
    try:
        from pydub import AudioSegment
        from src.utils.music_library import get_music_track

        # Get music track info
        track = get_music_track(music_track_id)
        if not track:
            log.warning(f"Music track {music_track_id} not found, skipping background music")
            return voice_audio

        # Build path to music file
        music_path = os.path.join(os.getcwd(), "assets", "music", track.filename)

        # Check if music file exists
        if not os.path.exists(music_path):
            log.warning(
                f"Music file not found: {music_path}. "
                "Skipping background music. See assets/music/README.md for download instructions."
            )
            return voice_audio

        # Load background music
        log.info(f"Loading background music from {music_path}")
        background = AudioSegment.from_mp3(music_path)

        # Get duration of voice audio
        voice_duration_ms = len(voice_audio)

        # Loop music if voice is longer than music
        if len(background) < voice_duration_ms:
            # Calculate how many times to loop
            loops_needed = (voice_duration_ms // len(background)) + 1
            background = background * loops_needed
            log.info(f"Looped background music {loops_needed} times")

        # Trim music to match voice duration
        background = background[:voice_duration_ms]

        # Reduce music volume (make it quieter than voice)
        # Convert volume from 0-1 scale to dB reduction
        # music_volume=0.25 means reduce by ~12dB
        db_reduction = -20 * (1 - music_volume)  # Logarithmic scaling
        background = background + db_reduction

        log.info(f"Reduced music volume by {abs(db_reduction):.1f}dB")

        # Add fade in at the beginning (3 seconds)
        background = background.fade_in(3000)

        # Add fade out at the end (3 seconds)
        background = background.fade_out(3000)

        # Mix voice and music
        # Overlay keeps voice audio on top
        mixed = background.overlay(voice_audio)

        log.info("Successfully mixed background music with voice")
        return mixed

    except Exception as e:
        log.error(f"Failed to add background music: {str(e)}")
        log.warning("Returning voice audio without background music")
        return voice_audio


# Voice preview sample texts for different styles
PREVIEW_TEXTS: Dict[str, str] = {
    "casual": "Hey there! Welcome to our podcast. Today we're diving into an exciting topic that I think you'll really enjoy.",
    "professional": "Good morning and welcome to today's episode. We'll be discussing the key insights and developments in this important field.",
    "educational": "Hello and welcome! In this lesson, we'll explore the fundamental concepts and break them down into simple, easy-to-understand terms.",
    "energetic": "What's up everyone! We've got an amazing show lined up for you today, so buckle up and let's jump right into it!"
}


@function.defn()
async def generate_voice_preview(input: dict) -> dict:
    """
    Generate a short voice preview for testing different voices.

    Args:
        input (dict): A dictionary containing:
            - voice_id (str): ElevenLabs voice ID to preview
            - style (str, optional): Podcast style for sample text
            - custom_text (str, optional): Custom preview text
            - api_key (str, optional): ElevenLabs API key

    Returns:
        dict: A dictionary containing base64-encoded preview audio
    """
    try:
        log.info("generate_voice_preview started", voice_id=input.get("voice_id", ""))

        # Extract input parameters
        voice_id = input.get("voice_id", "")
        style = input.get("style", "casual")
        custom_text = input.get("custom_text")
        api_key = input.get("api_key") or os.getenv("ELEVEN_LABS_API_KEY")

        # Validate input
        if not voice_id:
            raise ValueError("Voice ID is missing")
        if not api_key:
            raise ValueError("ElevenLabs API key is missing")

        # Get preview text
        text = custom_text if custom_text else PREVIEW_TEXTS.get(style, PREVIEW_TEXTS["casual"])

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
        log.info(f"Generating preview with ElevenLabs API")
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        # Collect response and encode to base64
        content = b''.join(response.iter_content(chunk_size=1024))
        base64_audio = base64.b64encode(content).decode('utf-8')

        log.info("Voice preview generated successfully", audio_size=len(base64_audio))

        return {
            "audio_base64": base64_audio,
            "text": text,
            "voice_id": voice_id,
            "style": style
        }

    except Exception as e:
        log.error("generate_voice_preview failed", error=str(e))
        raise e
