# 🎙️ AI Podcast Creator

An AI-powered podcast creator that transforms any topic into professional, multi-voice conversational podcasts using OpenAI GPT-4 and ElevenLabs voices.

## ✨ Features

- **AI Script Generation**: Automatically creates engaging conversational scripts from any topic
- **Multi-Voice Support**: 2-4 different AI voices for natural conversations
- **Multiple Styles**: Choose from casual, professional, educational, or energetic tones
- **Custom Scripts**: Bring your own script or let AI create one
- **Web Interface**: Beautiful Streamlit UI for easy podcast creation
- **Instant Preview**: Listen to your podcast immediately after generation
- **Downloadable**: Get MP3 audio and text script files

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker (for running Restack)
- OpenAI API key
- ElevenLabs API key

### 1. Start Restack Engine

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

The Restack UI will be available at http://localhost:5233

### 2. Set Up Environment

Navigate to the project directory:

```bash
cd ai_podcast_creator
```

Create a virtual environment using `uv`:

```bash
uv venv && source .venv/bin/activate
```

Or using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

### 3. Install Dependencies

Using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

### 4. Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
```

### 5. Run the Services

Start the Restack workflow services:

Using uv:

```bash
uv run dev
```

Or using pip:

```bash
python -c "from src.services import watch_services; watch_services()"
```

This will start the workflow engine and open the Restack UI.

### 6. Launch the Web UI

In a new terminal (keep the services running), activate the virtual environment and run:

```bash
streamlit run frontend/app.py
```

The Streamlit UI will open at http://localhost:8501

## 📖 Usage

### Creating a Podcast from a Topic

1. Open the Streamlit UI at http://localhost:8501
2. Select "Generate from Topic"
3. Enter your topic (e.g., "The future of AI in healthcare")
4. Choose your podcast style (casual, professional, educational, energetic)
5. Set the number of speakers (2-4)
6. Set target duration (1-10 minutes)
7. Click "Generate Podcast"
8. Wait 1-3 minutes for generation
9. Listen and download!

### Using a Custom Script

1. Select "Use Custom Script"
2. Enter your script using this format:

```
SPEAKER_1 (Host): Welcome to our podcast about AI!
SPEAKER_2 (Guest): Thanks for having me!
SPEAKER_1 (Host): Let's dive into the topic...
```

3. Configure speakers and style
4. Generate and download!

## 🎨 Podcast Styles

- **Casual**: Friendly, conversational tone with humor and anecdotes
- **Professional**: Formal, clear language focused on facts and insights
- **Educational**: Clear explanations with examples and analogies
- **Energetic**: Enthusiastic, dynamic language with high energy

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  ← User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Restack Workflow Engine       │
│  ┌──────────────────────────┐  │
│  │ PodcastCreatorWorkflow   │  │
│  │                          │  │
│  │  1. Generate Script      │  │ ← OpenAI GPT-4
│  │  2. Parse Speakers       │  │
│  │  3. Assign Voices        │  │
│  │  4. Generate Audio       │  │ ← ElevenLabs TTS
│  │  5. Merge Audio Chunks   │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Output Files   │
│  - podcast.mp3  │
│  - script.txt   │
└─────────────────┘
```

## 📁 Project Structure

```
ai_podcast_creator/
├── src/
│   ├── client.py                 # Restack client
│   ├── services.py               # Service runner
│   ├── functions/
│   │   ├── script_generator.py  # OpenAI script generation
│   │   ├── audio_generator.py   # ElevenLabs TTS
│   ├── workflows/
│   │   └── podcast_workflow.py  # Main orchestration
│   └── utils/
│       ├── script_parser.py     # Parse dialogue
│       └── voice_config.py      # Voice mappings
├── frontend/
│   └── app.py                    # Streamlit UI
├── output/                       # Generated podcasts
├── .env.example
├── pyproject.toml
└── README.md
```

## 🔧 Advanced Usage

### Running Workflows via API

You can also schedule workflows programmatically:

```python
import asyncio
from src.client import client
from src.workflows.podcast_workflow import PodcastCreatorWorkflow

async def create_podcast():
    result = await client.schedule_workflow(
        workflow_name=PodcastCreatorWorkflow.__name__,
        workflow_id="my-podcast-1",
        input={
            "topic": "The future of AI",
            "style": "casual",
            "duration": 5,
            "num_speakers": 2,
            "custom_script": False,
            "output_filename": "ai_future.mp3"
        }
    )
    return result

asyncio.run(create_podcast())
```

### Viewing Workflows in Restack UI

Visit http://localhost:5233 to:
- See all running workflows
- Monitor execution progress
- View logs and errors
- Replay workflows

## 💰 Cost Estimation

Approximate costs per podcast:

- **ElevenLabs**: ~$0.30 per 1000 characters
- **OpenAI GPT-4**: ~$0.03 per 1000 tokens

Example 10-minute podcast:
- ~2000 words = ~$0.60 (ElevenLabs) + ~$0.10 (OpenAI) = **~$0.70 total**

## 🎯 Roadmap

- [ ] Background music integration
- [ ] Voice cloning support
- [ ] RSS feed generation
- [ ] Multi-language support
- [ ] Audio editing tools
- [ ] Batch podcast creation
- [ ] API endpoint for external apps

## 🐛 Troubleshooting

### "API key is missing" error
Make sure your `.env` file is in the project root and contains valid API keys.

### "Connection refused" error
Ensure Restack is running: `docker ps` should show the restack container.

### "No module named 'pydub'" error
Install ffmpeg: `brew install ffmpeg` (Mac) or `sudo apt-get install ffmpeg` (Linux)

### Workflow not appearing in UI
Restart the services: Stop (Ctrl+C) and run `uv run dev` again.

## 📝 License

MIT License - feel free to use this for commercial or personal projects!

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 🔗 Links

- [Restack Documentation](https://docs.restack.io)
- [OpenAI API](https://platform.openai.com)
- [ElevenLabs API](https://elevenlabs.io/docs)
- [Streamlit Docs](https://docs.streamlit.io)

## 💬 Support

For issues or questions:
- Open an issue on GitHub
- Check existing examples in the community folder
- Visit Restack documentation

---

**Built with ❤️ using Restack AI, OpenAI, and ElevenLabs**

*Transform your ideas into engaging podcasts in minutes!* 🎙️
