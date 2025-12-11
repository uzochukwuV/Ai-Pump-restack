"""
Test script for the Podcast Creator workflow.
Run this to test the podcast generation end-to-end.
"""

import asyncio
import os
from dotenv import load_dotenv
from src.client import client
from src.workflows.podcast_workflow import PodcastCreatorWorkflow

# Load environment variables
load_dotenv()

async def test_podcast_creation():
    """
    Test the podcast creation workflow with a sample topic.
    """
    print("🎙️ Testing AI Podcast Creator Workflow")
    print("=" * 50)

    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_key = os.getenv("ELEVEN_LABS_API_KEY")

    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment!")
        return

    if not elevenlabs_key:
        print("❌ ELEVEN_LABS_API_KEY not found in environment!")
        return

    print("✅ API keys found")
    print()

    # Test configuration
    test_input = {
        "topic": "The benefits of meditation and mindfulness in reducing stress and improving mental health",
        "style": "casual",
        "duration": 2,  # Short duration for testing
        "num_speakers": 2,
        "custom_script": False,
        "output_filename": "test_meditation_podcast.mp3"
    }

    print("📋 Test Configuration:")
    print(f"  Topic: {test_input['topic']}")
    print(f"  Style: {test_input['style']}")
    print(f"  Duration: {test_input['duration']} minutes")
    print(f"  Speakers: {test_input['num_speakers']}")
    print()

    try:
        # Schedule the workflow
        print("🚀 Scheduling workflow...")
        workflow_id = "test-podcast-workflow"
        run_id = await client.schedule_workflow(
            workflow_name=PodcastCreatorWorkflow.__name__,
            workflow_id=workflow_id,
            input=test_input
        )

        print(f"✅ Workflow scheduled!")
        print(f"  Workflow ID: {workflow_id}")
        print(f"  Run ID: {run_id}")
        print()
        print("⏳ Generating podcast... This may take 1-3 minutes.")
        print("   You can monitor progress at http://localhost:5233")
        print()

        # Wait for result
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )

        print("=" * 50)
        print("🎉 SUCCESS! Podcast created!")
        print("=" * 50)
        print()
        print("📊 Results:")
        print(f"  Output Path: {result['output_path']}")
        print(f"  Script Path: {result['script_path']}")
        print(f"  Duration: {result['duration_minutes']:.2f} minutes")
        print(f"  Segments: {result['segment_count']}")
        print()
        print("📄 Script Preview:")
        print("-" * 50)
        script_preview = result['script'][:500]
        print(script_preview)
        if len(result['script']) > 500:
            print("...")
            print(f"(Showing first 500 characters of {len(result['script'])} total)")
        print("-" * 50)
        print()
        print(f"✅ Test completed successfully!")
        print(f"🎧 Listen to your podcast: {result['output_path']}")

    except Exception as e:
        print("=" * 50)
        print("❌ ERROR!")
        print("=" * 50)
        print(f"  {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure Restack is running (docker ps)")
        print("  2. Make sure services are running (uv run dev)")
        print("  3. Check API keys in .env file")
        print("  4. Check Restack UI at http://localhost:5233")

async def test_custom_script():
    """
    Test with a custom pre-written script.
    """
    print("\n" + "=" * 50)
    print("🎙️ Testing with Custom Script")
    print("=" * 50)

    custom_script_text = """SPEAKER_1 (Host): Welcome to Tech Talk! Today we're discussing AI.

SPEAKER_2 (Expert): Thanks for having me! AI is transforming everything.

SPEAKER_1 (Host): What's the most exciting development you've seen recently?

SPEAKER_2 (Expert): Large language models like GPT-4 are incredible. They can understand and generate human-like text with remarkable accuracy.

SPEAKER_1 (Host): That's fascinating! What about the concerns around AI safety?

SPEAKER_2 (Expert): It's crucial to develop AI responsibly. We need proper guidelines and ethical frameworks."""

    test_input = {
        "topic": custom_script_text,
        "style": "professional",
        "duration": 2,
        "num_speakers": 2,
        "custom_script": True,
        "output_filename": "test_custom_script_podcast.mp3"
    }

    try:
        workflow_id = "test-custom-script-workflow"
        run_id = await client.schedule_workflow(
            workflow_name=PodcastCreatorWorkflow.__name__,
            workflow_id=workflow_id,
            input=test_input
        )

        print(f"✅ Custom script workflow scheduled!")
        print("⏳ Generating audio from custom script...")

        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )

        print("🎉 Custom script podcast created!")
        print(f"  Output: {result['output_path']}")
        print(f"  Duration: {result['duration_minutes']:.2f} minutes")

    except Exception as e:
        print(f"❌ Custom script test failed: {str(e)}")

async def main():
    """Run all tests."""
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║     AI Podcast Creator - Test Suite           ║")
    print("╚════════════════════════════════════════════════╝")
    print()

    # Test 1: Topic-based generation
    await test_podcast_creation()

    # Test 2: Custom script (optional, comment out if you want faster testing)
    # await test_custom_script()

    print()
    print("╔════════════════════════════════════════════════╗")
    print("║     All Tests Completed!                       ║")
    print("╚════════════════════════════════════════════════╝")
    print()

if __name__ == "__main__":
    asyncio.run(main())
