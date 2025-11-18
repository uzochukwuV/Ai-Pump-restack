import asyncio
import os
from src.client import client
from src.workflows.podcast_workflow import PodcastCreatorWorkflow
from src.functions.script_generator import generate_script
from src.functions.audio_generator import generate_audio_segment, merge_audio_segments
from watchfiles import run_process
import webbrowser

async def main():
    await client.start_service(
        workflows=[PodcastCreatorWorkflow],
        functions=[
            generate_script,
            generate_audio_segment,
            merge_audio_segments,
        ],
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    print("Opening Restack UI at http://localhost:5233")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
    run_services()
