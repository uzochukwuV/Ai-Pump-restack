# Background Music Assets

This directory contains royalty-free background music tracks for podcasts.

## How to Add Music

Since actual music files are large and under various licenses, you'll need to download them separately.

### Recommended Free Music Sources:

1. **Free Music Archive** (https://freemusicarchive.org)
   - Filter by: CC BY (Commercial use allowed)
   - Download instrumental tracks
   - Suggested genres: Ambient, Jazz, Corporate, Electronic

2. **YouTube Audio Library** (https://www.youtube.com/audiolibrary)
   - Royalty-free
   - Commercial use allowed
   - Great variety

3. **Incompetech** (https://incompetech.com)
   - Kevin MacLeod's royalty-free music
   - Attribution required
   - High quality

4. **Bensound** (https://www.bensound.com)
   - Free with attribution
   - Professional quality

### Required Music Files:

Place these files in this directory:

```
music/
├── upbeat_corporate.mp3
├── calm_ambient.mp3
├── jazz_smooth.mp3
├── tech_modern.mp3
└── acoustic_gentle.mp3
```

### Music Specifications:

- **Format**: MP3
- **Bitrate**: 128kbps or higher
- **Length**: 2-3 minutes minimum
- **Type**: Instrumental only (no vocals)
- **Volume**: Normalized to -20dB

### Quick Download Commands:

```bash
# Example: Download from Free Music Archive
cd ai_podcast_creator/assets/music

# Replace URLs with actual track URLs
wget -O upbeat_corporate.mp3 "https://freemusicarchive.org/track/..."
wget -O calm_ambient.mp3 "https://freemusicarchive.org/track/..."
wget -O jazz_smooth.mp3 "https://freemusicarchive.org/track/..."
wget -O tech_modern.mp3 "https://freemusicarchive.org/track/..."
wget -O acoustic_gentle.mp3 "https://freemusicarchive.org/track/..."
```

### Testing Without Music:

The application will work without music files. It will:
1. Check if music file exists
2. Skip background music if not found
3. Generate podcast with voice only

### License Compliance:

- Always check license terms
- Provide attribution if required
- Keep license info in `MUSIC_LICENSES.txt`

### Alternative: Use Silent/Placeholder:

```bash
# Create 3-minute silent MP3 for testing
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame placeholder_music.mp3
```
