"""
Main podcast creator workflow.
Orchestrates the entire process from topic to final podcast audio.
"""

from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import functions
with import_functions():
    from src.functions.script_generator import generate_script
    from src.functions.audio_generator import generate_audio_segment, merge_audio_segments
    from src.utils.script_parser import parse_script_to_segments
    from src.utils.voice_config import get_voice_for_speaker

@workflow.defn()
class PodcastCreatorWorkflow:
    """
    Workflow to create a multi-voice podcast from a topic or script.

    Input:
        - topic: The topic or script content
        - style: Podcast style (casual, professional, educational, energetic)
        - duration: Target duration in minutes
        - num_speakers: Number of speakers (2-4)
        - custom_script: If True, topic is treated as a pre-written script

    Output:
        - output_path: Path to the generated podcast MP3
        - script: The generated or provided script
        - duration: Actual duration of the podcast
    """

    @workflow.run
    async def run(self, input: dict):
        log.info("PodcastCreatorWorkflow started", input=input)

        # Extract input parameters
        topic = input.get("topic", "")
        style = input.get("style", "casual")
        duration = input.get("duration", 5)
        num_speakers = input.get("num_speakers", 2)
        custom_script = input.get("custom_script", False)
        output_filename = input.get("output_filename", "podcast.mp3")

        # Get API keys from environment
        openai_key = os.getenv("OPENAI_API_KEY")
        elevenlabs_key = os.getenv("ELEVEN_LABS_API_KEY")

        # Step 1: Generate or use provided script
        if custom_script:
            log.info("Using custom script provided by user")
            script = topic
            script_result = {
                "script": script,
                "speaker_count": num_speakers,
                "estimated_duration": duration
            }
        else:
            log.info("Generating script using OpenAI")
            script_result = await workflow.step(
                generate_script,
                input={
                    "topic": topic,
                    "style": style,
                    "duration": duration,
                    "num_speakers": num_speakers,
                    "api_key": openai_key
                },
                start_to_close_timeout=timedelta(seconds=120)
            )

        script = script_result["script"]
        log.info("Script ready", word_count=script_result.get("word_count", 0))

        # Step 2: Parse script into speaker segments
        log.info("Parsing script into segments")
        segments = parse_script_to_segments(script)
        log.info(f"Parsed {len(segments)} dialogue segments")

        if len(segments) == 0:
            raise ValueError("Failed to parse any dialogue segments from script")

        # Step 3: Generate audio for each segment
        log.info("Generating audio segments")
        audio_segments = []

        # Track which speaker is which (SPEAKER_1 = index 0, etc.)
        speaker_to_index = {}
        current_speaker_index = 0

        for i, segment in enumerate(segments):
            speaker = segment['speaker']
            text = segment['text']

            # Assign speaker index if not seen before
            if speaker not in speaker_to_index:
                speaker_to_index[speaker] = current_speaker_index
                current_speaker_index += 1

            speaker_index = speaker_to_index[speaker]

            # Get appropriate voice for this speaker
            voice_id = get_voice_for_speaker(speaker_index, style)

            log.info(
                f"Generating audio for segment {i+1}/{len(segments)}",
                speaker=speaker,
                voice_id=voice_id
            )

            # Generate audio for this segment
            audio_result = await workflow.step(
                generate_audio_segment,
                input={
                    "text": text,
                    "voice_id": voice_id,
                    "api_key": elevenlabs_key
                },
                start_to_close_timeout=timedelta(seconds=60)
            )

            audio_segments.append(audio_result["audio_base64"])

        # Step 4: Merge all audio segments
        log.info("Merging audio segments")
        merge_result = await workflow.step(
            merge_audio_segments,
            input={
                "segments": audio_segments,
                "output_filename": output_filename
            },
            start_to_close_timeout=timedelta(seconds=120)
        )

        # Save script to file as well
        script_filename = output_filename.replace('.mp3', '_script.txt')
        script_path = os.path.join(os.getcwd(), "output", script_filename)
        with open(script_path, 'w') as f:
            f.write(script)

        log.info(
            "PodcastCreatorWorkflow completed successfully",
            output_path=merge_result["output_path"],
            duration_minutes=merge_result["duration_minutes"]
        )

        return {
            "output_path": merge_result["output_path"],
            "script_path": script_path,
            "script": script,
            "duration_seconds": merge_result["duration_seconds"],
            "duration_minutes": merge_result["duration_minutes"],
            "segment_count": len(segments),
            "audio_base64": merge_result["audio_base64"]
        }
