"""
Background music library configuration.
Defines available music tracks and their metadata.
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class MusicTrack:
    """Represents a background music track."""
    id: str
    name: str
    filename: str
    mood: str
    energy: str  # low, medium, high
    duration_seconds: int
    description: str
    license: str
    url: str  # URL to download the track

# Music library - Royalty-free tracks from Free Music Archive
# These are placeholder references - you'll need to download actual files
MUSIC_LIBRARY: Dict[str, MusicTrack] = {
    "upbeat_corporate": MusicTrack(
        id="upbeat_corporate",
        name="Upbeat Corporate",
        filename="upbeat_corporate.mp3",
        mood="professional",
        energy="medium",
        duration_seconds=180,
        description="Energetic corporate background music",
        license="CC BY 4.0",
        url="https://freemusicarchive.org/static/media/tracks/upbeat_corporate.mp3"
    ),

    "calm_ambient": MusicTrack(
        id="calm_ambient",
        name="Calm Ambient",
        filename="calm_ambient.mp3",
        mood="relaxed",
        energy="low",
        duration_seconds=200,
        description="Peaceful ambient background",
        license="CC BY 4.0",
        url="https://freemusicarchive.org/static/media/tracks/calm_ambient.mp3"
    ),

    "jazz_smooth": MusicTrack(
        id="jazz_smooth",
        name="Smooth Jazz",
        filename="jazz_smooth.mp3",
        mood="casual",
        energy="medium",
        duration_seconds=190,
        description="Smooth jazz for casual conversations",
        license="CC BY 4.0",
        url="https://freemusicarchive.org/static/media/tracks/jazz_smooth.mp3"
    ),

    "tech_modern": MusicTrack(
        id="tech_modern",
        name="Modern Tech",
        filename="tech_modern.mp3",
        mood="energetic",
        energy="high",
        duration_seconds=170,
        description="Modern tech-inspired background",
        license="CC BY 4.0",
        url="https://freemusicarchive.org/static/media/tracks/tech_modern.mp3"
    ),

    "acoustic_gentle": MusicTrack(
        id="acoustic_gentle",
        name="Gentle Acoustic",
        filename="acoustic_gentle.mp3",
        mood="warm",
        energy="low",
        duration_seconds=210,
        description="Warm acoustic guitar background",
        license="CC BY 4.0",
        url="https://freemusicarchive.org/static/media/tracks/acoustic_gentle.mp3"
    ),
}

# Style-based music recommendations
STYLE_MUSIC_MAPPING = {
    "casual": ["jazz_smooth", "acoustic_gentle", "calm_ambient"],
    "professional": ["upbeat_corporate", "calm_ambient"],
    "educational": ["calm_ambient", "acoustic_gentle"],
    "energetic": ["tech_modern", "upbeat_corporate"],
}

def get_recommended_music(style: str) -> List[str]:
    """
    Get recommended music tracks for a podcast style.

    Args:
        style: Podcast style (casual, professional, educational, energetic)

    Returns:
        List of recommended music track IDs
    """
    return STYLE_MUSIC_MAPPING.get(style, ["calm_ambient"])

def get_music_track(track_id: str) -> MusicTrack:
    """
    Get music track metadata by ID.

    Args:
        track_id: Music track ID

    Returns:
        MusicTrack object or None if not found
    """
    return MUSIC_LIBRARY.get(track_id)

def list_all_tracks() -> List[MusicTrack]:
    """
    Get all available music tracks.

    Returns:
        List of all MusicTrack objects
    """
    return list(MUSIC_LIBRARY.values())
