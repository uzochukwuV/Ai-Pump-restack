"""
Streamlit UI for AI Podcast Creator.
Provides a web interface for creating multi-voice podcasts.
"""

import streamlit as st
import asyncio
import os
import sys
import base64
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client import client
from src.workflows.podcast_workflow import PodcastCreatorWorkflow
from src.utils.music_library import list_all_tracks, get_recommended_music, get_music_track
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Podcast Creator",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎙️ AI Podcast Creator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Transform any topic into a multi-voice conversational podcast in minutes!</div>',
    unsafe_allow_html=True
)

# Initialize session state
if "podcast_created" not in st.session_state:
    st.session_state.podcast_created = False
if "result" not in st.session_state:
    st.session_state.result = None
if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Podcast Configuration")

    # Input mode selection
    input_mode = st.radio(
        "Input Mode",
        ["Generate from Topic", "Use Custom Script"],
        help="Choose whether to let AI generate a script or provide your own"
    )

    if input_mode == "Generate from Topic":
        topic = st.text_area(
            "What should your podcast be about?",
            height=150,
            placeholder="Example: The future of artificial intelligence in healthcare, focusing on diagnosis and treatment automation.",
            help="Describe the topic you want the podcast to discuss"
        )
        custom_script = False
    else:
        topic = st.text_area(
            "Enter your script (use SPEAKER_1:, SPEAKER_2: format)",
            height=250,
            placeholder="""SPEAKER_1 (Host): Welcome to our podcast!
SPEAKER_2 (Guest): Thanks for having me!
SPEAKER_1 (Host): Let's dive into today's topic...""",
            help="Format: SPEAKER_1: dialogue text"
        )
        custom_script = True

    # Configuration options
    col_a, col_b = st.columns(2)

    with col_a:
        style = st.selectbox(
            "Podcast Style",
            ["casual", "professional", "educational", "energetic"],
            help="Choose the tone and style of the podcast"
        )

        duration = st.slider(
            "Target Duration (minutes)",
            min_value=1,
            max_value=10,
            value=5,
            help="Approximate length of the podcast"
        )

    with col_b:
        num_speakers = st.slider(
            "Number of Speakers",
            min_value=2,
            max_value=4,
            value=2,
            help="How many different voices in the conversation"
        )

        output_filename = st.text_input(
            "Output Filename",
            value="my_podcast.mp3",
            help="Name for the generated podcast file"
        )

    # Voice Preview Section
    st.markdown("---")
    st.subheader("👂 Voice Preview (NEW!)")

    preview_voices_section = st.expander("🎧 Preview Voices Before Generating", expanded=False)

    with preview_voices_section:
        st.info("Listen to sample audio for each voice that will be used in your podcast.")

        from src.utils.voice_config import get_voice_for_speaker
        from src.functions.audio_generator import PREVIEW_TEXTS

        # Generate preview for each speaker
        for speaker_num in range(num_speakers):
            voice_id = get_voice_for_speaker(speaker_num, style)

            st.markdown(f"**Speaker {speaker_num + 1}**")

            col_preview_a, col_preview_b = st.columns([3, 1])

            with col_preview_a:
                preview_text = PREVIEW_TEXTS.get(style, PREVIEW_TEXTS["casual"])
                st.caption(f'Sample: "{preview_text[:80]}..."')
                st.caption(f"Voice ID: `{voice_id}`")

            with col_preview_b:
                if st.button(f"🔊 Preview", key=f"preview_speaker_{speaker_num}"):
                    with st.spinner(f"Generating preview for Speaker {speaker_num + 1}..."):
                        try:
                            # Generate preview
                            preview_result = asyncio.run(
                                client.execute_function(
                                    function_name="generate_voice_preview",
                                    input={
                                        "voice_id": voice_id,
                                        "style": style,
                                        "api_key": os.getenv("ELEVEN_LABS_API_KEY")
                                    }
                                )
                            )

                            # Decode and play audio
                            audio_bytes = base64.b64decode(preview_result["audio_base64"])
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success(f"✅ Preview generated!")

                        except Exception as e:
                            st.error(f"Failed to generate preview: {str(e)}")

            st.markdown("---")

    # Background Music Section
    st.markdown("---")
    st.subheader("🎵 Background Music")

    add_music = st.checkbox(
        "Add Background Music",
        value=False,
        help="Add professional background music to your podcast"
    )

    background_music = None
    music_volume = 0.25

    if add_music:
        col_music_a, col_music_b = st.columns(2)

        with col_music_a:
            # Get all available music tracks
            all_tracks = list_all_tracks()
            music_options = {
                "None": None,
                **{track.name: track.id for track in all_tracks}
            }

            # Get recommended tracks based on style
            recommended = get_recommended_music(style)
            recommended_names = [
                get_music_track(track_id).name
                for track_id in recommended
                if get_music_track(track_id)
            ]

            # Show recommendations
            if recommended_names:
                st.caption(f"💡 Recommended for {style}: {', '.join(recommended_names)}")

            selected_music_name = st.selectbox(
                "Choose Music Track",
                options=list(music_options.keys()),
                index=1 if len(music_options) > 1 else 0,
                help="Select background music that matches your podcast style"
            )

            background_music = music_options[selected_music_name]

        with col_music_b:
            music_volume = st.slider(
                "Music Volume",
                min_value=0.1,
                max_value=0.5,
                value=0.25,
                step=0.05,
                help="Adjust background music volume (voice will always be louder)"
            )

            st.caption(f"Music at {int(music_volume * 100)}% volume")

        # Show music track details if selected
        if background_music:
            track = get_music_track(background_music)
            if track:
                st.info(f"**{track.name}**\n\n{track.description}\n\n*Mood:* {track.mood} | *Energy:* {track.energy}")

                # Check if music file exists
                music_path = os.path.join(os.getcwd(), "assets", "music", track.filename)
                if not os.path.exists(music_path):
                    st.warning(
                        f"⚠️ Music file not found: `{track.filename}`\n\n"
                        "See `assets/music/README.md` for download instructions."
                    )

with col2:
    st.subheader("ℹ️ About")
    st.info(
        """
        **How it works:**

        1️⃣ Enter a topic or custom script

        2️⃣ Configure style and speakers

        3️⃣ Click Generate

        4️⃣ Download your podcast!

        **Powered by:**
        - OpenAI GPT-4 (script)
        - ElevenLabs (voices)
        - Restack AI (orchestration)
        """
    )

    # API key status
    st.subheader("🔑 API Status")
    openai_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_key = os.getenv("ELEVEN_LABS_API_KEY")

    if openai_key:
        st.success("✅ OpenAI API Key found")
    else:
        st.error("❌ OpenAI API Key missing")

    if elevenlabs_key:
        st.success("✅ ElevenLabs API Key found")
    else:
        st.error("❌ ElevenLabs API Key missing")

# Generate button
st.markdown("---")

async def generate_podcast():
    """Generate the podcast using Restack workflow."""
    try:
        # Schedule the workflow
        workflow_id = f"podcast-{os.urandom(4).hex()}"
        run_id = await client.schedule_workflow(
            workflow_name=PodcastCreatorWorkflow.__name__,
            workflow_id=workflow_id,
            input={
                "topic": topic,
                "style": style,
                "duration": duration,
                "num_speakers": num_speakers,
                "custom_script": custom_script,
                "output_filename": output_filename,
                "background_music": background_music,
                "music_volume": music_volume
            }
        )

        # Get the result
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )

        return result

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

if st.button("🎬 Generate Podcast", disabled=not (openai_key and elevenlabs_key)):
    if not topic or topic.strip() == "":
        st.warning("⚠️ Please enter a topic or script before generating!")
    else:
        with st.spinner("🎨 Creating your podcast... This may take 1-3 minutes."):
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("📝 Generating script...")
            progress_bar.progress(20)

            # Run the async workflow
            result = asyncio.run(generate_podcast())

            if result:
                progress_bar.progress(100)
                status_text.text("✅ Podcast created successfully!")

                st.session_state.podcast_created = True
                st.session_state.result = result
                st.session_state.generation_history.append({
                    "topic": topic[:50] + "..." if len(topic) > 50 else topic,
                    "filename": output_filename,
                    "duration": result.get("duration_minutes", 0)
                })

# Display results if podcast was created
if st.session_state.podcast_created and st.session_state.result:
    st.markdown("---")
    st.success("🎉 Your podcast is ready!")

    result = st.session_state.result

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🎧 Listen to Your Podcast")

        # Display audio player
        if "output_path" in result and os.path.exists(result["output_path"]):
            with open(result["output_path"], "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

            # Download button
            st.download_button(
                label="⬇️ Download Podcast (MP3)",
                data=audio_bytes,
                file_name=output_filename,
                mime="audio/mp3"
            )

        # Display script
        with st.expander("📄 View Script"):
            st.text_area(
                "Generated Script",
                value=result.get("script", ""),
                height=300,
                disabled=True
            )

            # Download script
            if "script_path" in result and os.path.exists(result["script_path"]):
                with open(result["script_path"], "r") as script_file:
                    script_text = script_file.read()
                    st.download_button(
                        label="⬇️ Download Script (TXT)",
                        data=script_text,
                        file_name=output_filename.replace('.mp3', '_script.txt'),
                        mime="text/plain"
                    )

    with col_right:
        st.subheader("📊 Podcast Details")
        st.metric("Duration", f"{result.get('duration_minutes', 0):.1f} minutes")
        st.metric("Segments", result.get('segment_count', 0))
        st.metric("Style", style.title())
        st.metric("Speakers", num_speakers)

        # Create another button
        if st.button("🔄 Create Another Podcast"):
            st.session_state.podcast_created = False
            st.session_state.result = None
            st.rerun()

# Generation history
if st.session_state.generation_history:
    st.markdown("---")
    st.subheader("📜 Generation History")
    for i, item in enumerate(reversed(st.session_state.generation_history), 1):
        st.text(f"{i}. {item['filename']} - {item['topic']} ({item['duration']:.1f} min)")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        Made with ❤️ using Restack AI |
        <a href="https://github.com/restackio/examples-python" target="_blank">View Examples</a>
    </div>
    """,
    unsafe_allow_html=True
)

def main():
    """Entry point for running the Streamlit app."""
    pass

if __name__ == "__main__":
    main()
