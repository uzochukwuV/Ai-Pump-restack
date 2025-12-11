# 🚀 Quick Start Guide - AI Podcast Creator

## Get Your First Podcast in 5 Minutes!

### Step 1: Start Restack (30 seconds)

```bash
docker run -d --pull always --name restack \
  -p 5233:5233 -p 6233:6233 -p 7233:7233 \
  ghcr.io/restackio/restack:main
```

✅ Restack UI will be at http://localhost:5233

### Step 2: Set Up API Keys (1 minute)

```bash
cd ai_podcast_creator
cp .env.example .env
```

Edit `.env` and add your keys:
```env
OPENAI_API_KEY=sk-proj-...your-key-here
ELEVEN_LABS_API_KEY=...your-key-here
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs: https://elevenlabs.io/app/settings/api-keys

### Step 3: Install Dependencies (1 minute)

```bash
# Using uv (recommended)
uv venv && source .venv/bin/activate
uv sync

# OR using pip
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### Step 4: Start Services (30 seconds)

```bash
# Using uv
uv run dev

# OR using pip
python -c "from src.services import watch_services; watch_services()"
```

This opens the Restack UI and starts the workflow engine.

### Step 5: Launch the Web UI (30 seconds)

**In a new terminal:**

```bash
cd ai_podcast_creator
source .venv/bin/activate  # Activate venv
streamlit run frontend/app.py
```

Opens at http://localhost:8501

### Step 6: Create Your First Podcast! (2 minutes)

1. Enter a topic:
   ```
   The benefits of exercise for mental health
   ```

2. Choose settings:
   - Style: **Casual**
   - Speakers: **2**
   - Duration: **3 minutes**

3. Click **"Generate Podcast"**

4. Wait 1-2 minutes

5. **Listen and Download!**

---

## Alternative: Test via Command Line

```bash
python test_workflow.py
```

This creates a test podcast about meditation.

---

## Troubleshooting

### "Connection refused"
```bash
docker ps  # Check if restack is running
```

### "API key missing"
```bash
cat .env  # Verify keys are set
```

### "Module not found"
```bash
pip install -e .  # Reinstall dependencies
```

---

## What's Next?

- Try different podcast styles (professional, educational, energetic)
- Use custom scripts with SPEAKER_1:, SPEAKER_2: format
- Check out `/output` folder for generated files
- Monitor workflows at http://localhost:5233
- Read full docs in README.md

---

**Need Help?**
- Check README.md for detailed documentation
- View PROJECT_SUMMARY.md for architecture details
- See PODCAST_CREATOR_ARCHITECTURE.md for design

**Ready to build a business?**
- Cost: ~$0.70 per 10-minute podcast
- Potential: $19-99/month SaaS
- Market: Growing rapidly in 2025

Happy podcasting! 🎙️
