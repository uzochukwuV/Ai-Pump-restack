#!/bin/bash
# Helper script to download or create placeholder music for testing

set -e

MUSIC_DIR="$(cd "$(dirname "$0")/../assets/music" && pwd)"
echo "📁 Music directory: $MUSIC_DIR"

# Create music directory if it doesn't exist
mkdir -p "$MUSIC_DIR"

echo "🎵 Setting up background music..."
echo ""

# Check if ffmpeg is available (needed for creating test files)
if command -v ffmpeg &> /dev/null; then
    FFMPEG_AVAILABLE=true
    echo "✅ FFmpeg found - can create placeholder music"
else
    FFMPEG_AVAILABLE=false
    echo "⚠️  FFmpeg not found - cannot create placeholder music"
    echo "   Install: brew install ffmpeg (Mac) or apt-get install ffmpeg (Linux)"
fi

echo ""
echo "Choose an option:"
echo "1) Create silent placeholder music (for testing without real music)"
echo "2) Show instructions for downloading real royalty-free music"
echo "3) Exit"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        if [ "$FFMPEG_AVAILABLE" = false ]; then
            echo "❌ FFmpeg is required to create placeholder music"
            echo "   Install it and try again"
            exit 1
        fi

        echo ""
        echo "Creating silent placeholder music files..."
        echo "These files can be used for testing the feature."
        echo ""

        cd "$MUSIC_DIR"

        # Create 3-minute silent MP3 files for each track
        echo "Creating upbeat_corporate.mp3 (3 min silent)..."
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame upbeat_corporate.mp3 -y &> /dev/null

        echo "Creating calm_ambient.mp3 (3 min silent)..."
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame calm_ambient.mp3 -y &> /dev/null

        echo "Creating jazz_smooth.mp3 (3 min silent)..."
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame jazz_smooth.mp3 -y &> /dev/null

        echo "Creating tech_modern.mp3 (3 min silent)..."
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame tech_modern.mp3 -y &> /dev/null

        echo "Creating acoustic_gentle.mp3 (3 min silent)..."
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 180 -q:a 9 -acodec libmp3lame acoustic_gentle.mp3 -y &> /dev/null

        echo ""
        echo "✅ Created 5 placeholder music files in $MUSIC_DIR"
        echo ""
        echo "⚠️  NOTE: These are SILENT files for testing only!"
        echo "   For real music, see option 2 or download from:"
        echo "   - freemusicarchive.org"
        echo "   - youtube.com/audiolibrary"
        echo "   - incompetech.com"
        echo ""
        ;;

    2)
        echo ""
        echo "📥 How to Download Royalty-Free Music"
        echo "======================================"
        echo ""
        echo "1. Visit Free Music Archive:"
        echo "   https://freemusicarchive.org"
        echo ""
        echo "2. Filter by license: CC BY (Commercial use allowed)"
        echo ""
        echo "3. Search for instrumental tracks in these genres:"
        echo "   - Ambient (for calm_ambient.mp3)"
        echo "   - Jazz (for jazz_smooth.mp3)"
        echo "   - Corporate/Upbeat (for upbeat_corporate.mp3)"
        echo "   - Electronic/Tech (for tech_modern.mp3)"
        echo "   - Acoustic (for acoustic_gentle.mp3)"
        echo ""
        echo "4. Download MP3 files and rename them to match:"
        echo "   $MUSIC_DIR/upbeat_corporate.mp3"
        echo "   $MUSIC_DIR/calm_ambient.mp3"
        echo "   $MUSIC_DIR/jazz_smooth.mp3"
        echo "   $MUSIC_DIR/tech_modern.mp3"
        echo "   $MUSIC_DIR/acoustic_gentle.mp3"
        echo ""
        echo "Alternative Sources:"
        echo "   - YouTube Audio Library: youtube.com/audiolibrary"
        echo "   - Incompetech: incompetech.com"
        echo "   - Bensound: bensound.com"
        echo ""
        echo "Specifications:"
        echo "   - Format: MP3"
        echo "   - Length: 2-3 minutes minimum"
        echo "   - Type: Instrumental only (no vocals)"
        echo "   - Bitrate: 128kbps or higher"
        echo ""
        ;;

    3)
        echo "Exiting..."
        exit 0
        ;;

    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo "Done! 🎉"
