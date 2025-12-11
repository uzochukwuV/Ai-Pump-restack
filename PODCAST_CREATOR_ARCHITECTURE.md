# AI Podcast Creator - Architecture Design

## Project Overview

An AI-powered podcast creator that converts written scripts or topics into multi-voice conversational podcasts using ElevenLabs and OpenAI.

## Core Features

### MVP (v1.0)
1. **Script Input**: Users can provide raw text or topic for AI to create a conversation
2. **AI Script Generation**: OpenAI generates conversational dialogue between multiple speakers
3. **Voice Assignment**: Automatically assigns different ElevenLabs voices to speakers
4. **Audio Generation**: Converts the script to multi-voice audio using ElevenLabs API
5. **Download**: Users can download the generated podcast MP3
6. **Streamlit UI**: Simple web interface for creation

### Future Features (v2.0+)
- Background music integration
- Voice cloning for custom voices
- Episode series management
- RSS feed generation for podcast distribution
- Multi-language support
- Audio editing tools (trim, merge segments)
- Transcription export

## Technical Architecture

### Tech Stack
- **Orchestration**: Restack AI workflows
- **LLM**: OpenAI GPT-4 (script generation)
- **Voice**: ElevenLabs API (text-to-speech)
- **UI**: Streamlit
- **Backend**: FastAPI (optional for production)
- **Language**: Python 3.12+

### System Components

```
┌─────────────────┐
│  Streamlit UI   │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Restack Workflow Engine       │
│                                 │
│  ┌──────────────────────────┐  │
│  │ PodcastCreatorWorkflow   │  │
│  │                          │  │
│  │  1. Generate Script      │  │
│  │     (OpenAI)             │  │
│  │                          │  │
│  │  2. Parse Speakers       │  │
│  │     (Python)             │  │
│  │                          │  │
│  │  3. Assign Voices        │  │
│  │     (Config)             │  │
│  │                          │  │
│  │  4. Generate Audio       │  │
│  │     (ElevenLabs)         │  │
│  │                          │  │
│  │  5. Merge Audio Chunks   │  │
│  │     (Pydub)              │  │
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

### Data Flow

1. **User Input** → Topic/Script + Podcast Style
2. **Script Generation** → OpenAI creates conversational dialogue
3. **Speaker Parsing** → Extract speakers from script (SPEAKER_1:, SPEAKER_2:)
4. **Voice Mapping** → Map speakers to ElevenLabs voice IDs
5. **Audio Generation** → Convert each line to speech with assigned voice
6. **Audio Merging** → Combine all segments into final podcast
7. **Output** → Return downloadable MP3 file

## Implementation Details

### 1. Workflow Definition

**PodcastCreatorWorkflow** - Main orchestration workflow

Steps:
- `generate_script()` - Creates conversational script using OpenAI
- `parse_speakers()` - Extracts speaker dialogue from script
- `assign_voices()` - Maps speakers to ElevenLabs voices
- `generate_audio_segments()` - Converts each line to audio
- `merge_audio()` - Combines segments into final podcast

### 2. Functions

**generate_script(input)**
```python
Input: {
    "topic": str,           # Topic or raw script
    "style": str,           # casual, professional, educational
    "duration": int,        # Target minutes
    "num_speakers": int     # 2-4 speakers
}
Output: {
    "script": str,          # Formatted dialogue
    "speakers": List[str]   # List of speaker names
}
```

**generate_multi_voice_audio(input)**
```python
Input: {
    "segments": List[{
        "speaker": str,
        "text": str,
        "voice_id": str
    }],
    "api_key": str
}
Output: {
    "audio_base64": str,    # Final podcast audio
    "duration": float       # Length in seconds
}
```

### 3. Voice Configuration

Pre-configured ElevenLabs voices for different personas:

```python
VOICE_LIBRARY = {
    "professional_male": "voice_id_1",
    "professional_female": "voice_id_2",
    "casual_male": "voice_id_3",
    "casual_female": "voice_id_4",
    "energetic_male": "voice_id_5",
    "energetic_female": "voice_id_6"
}
```

### 4. Script Format

Generated scripts follow this format:

```
SPEAKER_1 (Host): Welcome to the AI Insights podcast! Today we're discussing machine learning.

SPEAKER_2 (Expert): Thanks for having me! Machine learning is revolutionizing every industry.

SPEAKER_1 (Host): That's fascinating! Can you tell us more about how it works?

SPEAKER_2 (Expert): Sure! At its core, machine learning allows computers to learn from data...
```

### 5. UI Components

**Streamlit Interface**:
- Topic/Script input (text area)
- Style selector (dropdown: casual, professional, educational)
- Number of speakers (slider: 2-4)
- Target duration (slider: 1-10 minutes)
- Generate button
- Progress indicator
- Audio player for preview
- Download button
- Script preview/export

## File Structure

```
ai_podcast_creator/
├── src/
│   ├── __init__.py
│   ├── client.py                 # Restack client
│   ├── services.py               # Service runner
│   ├── functions/
│   │   ├── __init__.py
│   │   ├── script_generator.py  # OpenAI script generation
│   │   ├── audio_generator.py   # ElevenLabs TTS
│   │   └── audio_processor.py   # Audio merging
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── podcast_workflow.py  # Main workflow
│   └── utils/
│       ├── __init__.py
│       ├── script_parser.py     # Parse speaker dialogue
│       └── voice_config.py      # Voice mappings
├── frontend/
│   └── app.py                    # Streamlit UI
├── output/                       # Generated podcasts
├── .env.example
├── pyproject.toml
└── README.md
```

## API Requirements

### ElevenLabs API
- **Endpoint**: `/v1/text-to-speech/{voice_id}`
- **Method**: POST
- **Rate Limit**: Consider LMNT example (1 req/sec with queue)
- **Quota**: Check account limits

### OpenAI API
- **Model**: GPT-4 or GPT-4-turbo
- **Endpoint**: `/v1/chat/completions`
- **Prompt Engineering**:
  - System: "You are a podcast script writer..."
  - User: "Create a {style} {duration}-minute conversation about {topic}"

## Deployment Strategy

### Phase 1: Local Development
- Run via `uv run dev`
- Streamlit on localhost:8501
- Restack UI on localhost:5233

### Phase 2: Production (Restack Cloud)
- Deploy workflows to Restack Cloud
- Streamlit on separate hosting (Streamlit Cloud/Heroku)
- Use environment variables for API keys
- Add authentication for users

## Monetization Model

### Pricing Tiers
1. **Free**: 1 podcast/day, 5 min max, 2 speakers
2. **Starter** ($19/mo): 10 podcasts/day, 15 min max, 4 speakers
3. **Pro** ($49/mo): Unlimited podcasts, 30 min max, custom voices
4. **Enterprise** (Custom): API access, white-label, RSS hosting

### Cost Calculation
- ElevenLabs: ~$0.30 per 1000 characters
- OpenAI GPT-4: ~$0.03 per 1000 tokens
- Example: 10-min podcast = ~2000 words = $0.60 + $0.10 = **$0.70 per podcast**
- At $19/mo (10 podcasts), **gross margin ~63%**

## Success Metrics

### MVP Launch (Week 4)
- [ ] Generate 5-minute 2-speaker podcast in < 2 minutes
- [ ] Audio quality: Clear, natural-sounding voices
- [ ] Script quality: Coherent, engaging conversation
- [ ] UI: Simple, intuitive, no crashes

### Post-Launch (Month 1)
- 100 users signed up
- 50 podcasts generated
- 10 paying customers ($190 MRR)
- NPS score > 40

## Risk Mitigation

### Technical Risks
1. **API Rate Limits**: Implement queuing system (see LMNT example)
2. **Audio Quality**: Allow voice re-selection before generation
3. **Script Quality**: Provide editing before audio generation
4. **Cost Overruns**: Set hard limits on podcast length

### Business Risks
1. **Competition**: Focus on ease-of-use and quality
2. **API Dependency**: Have fallback LLM/TTS options
3. **Scaling Costs**: Optimize prompts, cache common requests

## Next Steps

1. Set up project structure
2. Implement script generation function
3. Implement multi-voice audio generation
4. Create workflow orchestration
5. Build Streamlit UI
6. Test end-to-end
7. Deploy to Restack Cloud
8. Launch on Product Hunt

---

**Timeline**: 2-3 weeks to MVP
**Team**: 1 developer (you!)
**Budget**: $0 initial (use existing API credits)
