"""
Voice configuration for ElevenLabs voices.
Map different speaker personas to ElevenLabs voice IDs.
"""

# ElevenLabs pre-made voices (these are example IDs - replace with actual voice IDs from your account)
VOICE_LIBRARY = {
    # Professional voices
    "professional_male_1": "pNInz6obpgDQGcFmaJgB",      # Adam - Deep, professional
    "professional_female_1": "EXAVITQu4vr4xnSDxMaL",    # Bella - Professional, clear

    # Casual/Conversational voices
    "casual_male_1": "VR6AewLTigWG4xSOukaG",           # Arnold - Casual, friendly
    "casual_female_1": "21m00Tcm4TlvDq8ikWAM",         # Rachel - Warm, conversational

    # Energetic voices
    "energetic_male_1": "TxGEqnHWrfWFTfGW9XjX",        # Josh - Energetic, young
    "energetic_female_1": "jsCqWAovK2LkecY7zXl4",      # Freya - Energetic, enthusiastic

    # Default fallbacks
    "default_male": "pNInz6obpgDQGcFmaJgB",            # Adam
    "default_female": "21m00Tcm4TlvDq8ikWAM",          # Rachel
}

# Voice style presets for different podcast styles
STYLE_VOICE_MAPPINGS = {
    "professional": {
        "speaker_1": VOICE_LIBRARY["professional_male_1"],
        "speaker_2": VOICE_LIBRARY["professional_female_1"],
        "speaker_3": VOICE_LIBRARY["casual_male_1"],
        "speaker_4": VOICE_LIBRARY["casual_female_1"],
    },
    "casual": {
        "speaker_1": VOICE_LIBRARY["casual_male_1"],
        "speaker_2": VOICE_LIBRARY["casual_female_1"],
        "speaker_3": VOICE_LIBRARY["energetic_male_1"],
        "speaker_4": VOICE_LIBRARY["energetic_female_1"],
    },
    "educational": {
        "speaker_1": VOICE_LIBRARY["professional_female_1"],
        "speaker_2": VOICE_LIBRARY["casual_male_1"],
        "speaker_3": VOICE_LIBRARY["professional_male_1"],
        "speaker_4": VOICE_LIBRARY["casual_female_1"],
    },
    "energetic": {
        "speaker_1": VOICE_LIBRARY["energetic_male_1"],
        "speaker_2": VOICE_LIBRARY["energetic_female_1"],
        "speaker_3": VOICE_LIBRARY["casual_male_1"],
        "speaker_4": VOICE_LIBRARY["casual_female_1"],
    }
}

def get_voice_for_speaker(speaker_index: int, style: str = "casual") -> str:
    """
    Get the appropriate voice ID for a speaker based on index and style.

    Args:
        speaker_index: 0-based index of the speaker (0, 1, 2, 3)
        style: Podcast style (professional, casual, educational, energetic)

    Returns:
        ElevenLabs voice ID string
    """
    speaker_key = f"speaker_{speaker_index + 1}"
    style_mapping = STYLE_VOICE_MAPPINGS.get(style, STYLE_VOICE_MAPPINGS["casual"])

    # If speaker index exceeds available voices, cycle through them
    if speaker_key not in style_mapping:
        speaker_key = f"speaker_{(speaker_index % 4) + 1}"

    return style_mapping.get(speaker_key, VOICE_LIBRARY["default_male"])
