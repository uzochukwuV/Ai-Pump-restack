"""
Script generation function using OpenAI GPT-4.
Generates conversational podcast scripts based on topic and style.
"""

from restack_ai.function import function, log
from openai import AsyncOpenAI
import os

@function.defn()
async def generate_script(input: dict) -> dict:
    """
    Generate a conversational podcast script using OpenAI.

    Args:
        input (dict): A dictionary containing:
            - topic (str): The topic or raw script to convert
            - style (str): Style of podcast (casual, professional, educational, energetic)
            - duration (int): Target duration in minutes
            - num_speakers (int): Number of speakers (2-4)
            - api_key (str, optional): OpenAI API key

    Returns:
        dict: A dictionary containing:
            - script (str): The generated script with speaker labels
            - speaker_count (int): Number of speakers in the script
            - estimated_duration (float): Estimated duration in minutes
    """
    try:
        log.info("generate_script function started", input=input)

        # Extract input parameters
        topic = input.get("topic", "")
        style = input.get("style", "casual")
        duration = input.get("duration", 5)
        num_speakers = input.get("num_speakers", 2)
        api_key = input.get("api_key") or os.getenv("OPENAI_API_KEY")

        # Validate input
        if not topic:
            raise ValueError("Topic is empty")
        if not api_key:
            raise ValueError("OpenAI API key is missing")
        if num_speakers < 2 or num_speakers > 4:
            raise ValueError("Number of speakers must be between 2 and 4")

        # Initialize OpenAI client
        client = AsyncOpenAI(api_key=api_key)

        # Build the prompt based on style
        system_prompt = f"""You are an expert podcast script writer. Create engaging, natural-sounding {style} podcast conversations.

IMPORTANT FORMATTING RULES:
1. Use SPEAKER_1, SPEAKER_2, etc. as speaker labels
2. Format each line as: SPEAKER_N: [dialogue text]
3. You can add role descriptions in parentheses like: SPEAKER_1 (Host): [text]
4. Make the conversation flow naturally with back-and-forth dialogue
5. Include natural speech patterns, questions, and reactions
6. Aim for approximately {duration} minutes of content (about {duration * 150} words)

Style Guidelines for {style}:
""" + {
            "casual": "- Use friendly, conversational tone\n- Include humor and personal anecdotes\n- Ask engaging questions\n- React naturally to what's being said",
            "professional": "- Use formal, clear language\n- Focus on facts and insights\n- Ask probing questions\n- Maintain professional tone throughout",
            "educational": "- Explain concepts clearly\n- Use examples and analogies\n- Ask clarifying questions\n- Build knowledge progressively",
            "energetic": "- Use enthusiastic, dynamic language\n- Show excitement and passion\n- Use exclamations appropriately\n- Keep the energy high"
        }.get(style, "Use a balanced, engaging tone")

        user_prompt = f"""Create a {duration}-minute podcast script with {num_speakers} speakers about:

{topic}

Remember to:
- Use exactly {num_speakers} speakers (SPEAKER_1, SPEAKER_2, etc.)
- Make it conversational and engaging
- Include natural transitions and reactions
- Format correctly: SPEAKER_N: dialogue
- Aim for approximately {duration * 150} words total"""

        # Generate the script
        log.info("Calling OpenAI API for script generation")

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,  # Higher temperature for more creative dialogue
            max_tokens=2000,  # Enough for a good conversation
        )

        script = response.choices[0].message.content.strip()

        # Calculate estimated duration (rough estimate: 150 words per minute)
        word_count = len(script.split())
        estimated_duration = word_count / 150.0

        log.info(
            "Script generation successful",
            word_count=word_count,
            estimated_duration=estimated_duration
        )

        return {
            "script": script,
            "speaker_count": num_speakers,
            "estimated_duration": estimated_duration,
            "word_count": word_count
        }

    except Exception as e:
        log.error("generate_script function failed", error=str(e))
        raise e
