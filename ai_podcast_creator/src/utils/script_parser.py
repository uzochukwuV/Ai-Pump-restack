"""
Script parser utilities for extracting speaker dialogue from generated scripts.
"""

import re
from typing import List, Dict

def parse_script_to_segments(script: str) -> List[Dict[str, str]]:
    """
    Parse a script into speaker segments.

    Expected format:
        SPEAKER_1: Hello, welcome to the show!
        SPEAKER_2: Thanks for having me!

    Or:
        SPEAKER_1 (Host): Hello, welcome to the show!
        SPEAKER_2 (Guest): Thanks for having me!

    Args:
        script: The full script text

    Returns:
        List of dictionaries with 'speaker' and 'text' keys
    """
    segments = []

    # Pattern to match: SPEAKER_N (optional role): text
    pattern = r'(SPEAKER_\d+)(?:\s*\([^)]+\))?\s*:\s*(.+?)(?=\n(?:SPEAKER_\d+|$))'

    matches = re.finditer(pattern, script, re.DOTALL | re.MULTILINE)

    for match in matches:
        speaker = match.group(1).strip()
        text = match.group(2).strip()

        # Clean up the text - remove extra whitespace and newlines within the segment
        text = ' '.join(text.split())

        if text:  # Only add non-empty segments
            segments.append({
                'speaker': speaker,
                'text': text
            })

    return segments

def extract_speaker_count(script: str) -> int:
    """
    Extract the number of unique speakers from a script.

    Args:
        script: The full script text

    Returns:
        Number of unique speakers
    """
    pattern = r'SPEAKER_(\d+)'
    matches = re.findall(pattern, script)

    if not matches:
        return 0

    unique_speakers = set(int(num) for num in matches)
    return len(unique_speakers)

def format_script_for_display(script: str) -> str:
    """
    Format script for better readability in UI.

    Args:
        script: The raw script text

    Returns:
        Formatted script with proper line breaks
    """
    # Add double line breaks between speaker changes for readability
    formatted = re.sub(
        r'(SPEAKER_\d+(?:\s*\([^)]+\))?\s*:)',
        r'\n\n\1',
        script
    )

    return formatted.strip()

def validate_script(script: str) -> tuple[bool, str]:
    """
    Validate that a script is properly formatted.

    Args:
        script: The script to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not script or not script.strip():
        return False, "Script is empty"

    speaker_count = extract_speaker_count(script)

    if speaker_count == 0:
        return False, "No speakers found in script. Expected format: SPEAKER_1: text"

    if speaker_count > 10:
        return False, f"Too many speakers ({speaker_count}). Maximum is 10."

    segments = parse_script_to_segments(script)

    if len(segments) == 0:
        return False, "Could not parse any dialogue from script"

    if len(segments) < 2:
        return False, "Script must have at least 2 dialogue segments"

    return True, ""
