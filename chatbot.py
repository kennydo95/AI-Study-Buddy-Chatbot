"""
chatbot.py — OpenAI API wrapper with conversation history and study modes.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── System prompts per mode ───────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "Explain It": (
        "You are a friendly and patient study tutor. When the student gives you a topic or concept, "
        "explain it clearly using simple language, real-world analogies, and examples. "
        "Break down complex ideas into easy steps. End each explanation by asking if they'd like to go deeper on any part."
    ),
    "Quiz Me": (
        "You are a study quiz master. When the student gives you a topic, generate 3 to 5 multiple-choice "
        "questions (A/B/C/D) one at a time. Wait for the student's answer before revealing if it's correct "
        "and explaining why. Keep a running score and encourage the student throughout."
    ),
    "Summarise": (
        "You are an expert at summarising study material. When the student pastes notes or describes a topic, "
        "produce a clean, structured summary with: a 2-sentence overview, key points as bullet points, "
        "and a 'Remember This' section with the 3 most important takeaways."
    ),
}


def get_response(messages: list[dict], mode: str) -> str:
    """
    Send conversation history to OpenAI and return the assistant reply.

    Args:
        messages: List of {"role": "user"/"assistant", "content": str}
        mode:     One of "Explain It", "Quiz Me", "Summarise"

    Returns:
        Assistant reply as a string.
    """
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["Explain It"])

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",      # swap to "gpt-4o" for better answers
        messages=full_messages,
        temperature=0.7,
        max_tokens=800,
    )
    return response.choices[0].message.content


def build_starter_message(mode: str) -> str:
    """Return a helpful opening message depending on the selected mode."""
    starters = {
        "Explain It": "👋 Hi! I'm your Study Buddy. Tell me any topic or concept you want me to explain — like *'photosynthesis'*, *'Newton's laws'*, or *'how recursion works in Python'*.",
        "Quiz Me":    "🧠 Quiz mode activated! Give me a topic and I'll test your knowledge with multiple-choice questions. What subject should we tackle?",
        "Summarise":  "📝 Paste your notes or describe a topic and I'll turn it into a clean, structured summary. What would you like to summarise?",
    }
    return starters.get(mode, "Hello! How can I help you study today?")
