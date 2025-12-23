"""
Utility functions for personality boundary enforcement
"""

import re
from typing import Dict, Any


def is_math_expression(user_input: str) -> bool:
    """Check if input contains math expressions or operators"""
    math_pattern = r'[\d\+\-\*/\(\)\^=]+'
    return bool(re.search(math_pattern, user_input))


def enforce_personality_boundary(user_input: str, personality: str, personalities_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if user input is within the personality's domain.

    Args:
        user_input: The user's message
        personality: The selected personality
        personalities_dict: Dictionary of all personalities

    Returns:
        Dictionary with 'allowed' (bool) and 'response' (str) keys
    """

    if personality not in personalities_dict:
        return {
            "allowed": False,
            "response": "Unknown personality selected."
        }

    personality_info = personalities_dict[personality]
    keywords = personality_info.get("keywords", [])
    refuse_message = personality_info.get("refuse_message", "I can't answer that question.")

    # Convert input to lowercase for comparison
    user_input_lower = user_input.lower()

    # Keep original for math detection
    original_input = user_input

    # Remove common punctuation for better matching (but keep math operators)
    cleaned_input = re.sub(r'[?!.,;:\'"()]', '', user_input_lower)

    # Split into words
    words = cleaned_input.split()

    # Check if any keyword is present in the user input
    keyword_found = False
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Check both whole words and partial word matches
        if keyword_lower in cleaned_input or any(keyword_lower in word for word in words):
            keyword_found = True
            break

    # If keywords found, allow the question
    if keyword_found:
        return {
            "allowed": True,
            "response": ""
        }

    # Special handling for Math Teacher - check for math expressions
    if personality == "Math Teacher":
        if is_math_expression(original_input):
            return {
                "allowed": True,
                "response": ""
            }

    # Additional semantic check using common phrases
    common_phrases = {
        "Math Teacher": ["how do i", "solve", "calculate", "what is", "explain", "problem",
                        "simplify", "factor", "expand", "derivative", "integral", "equals",
                        "plus", "minus", "times", "divided", "formula", "equation"],
        "Doctor": ["i have", "symptoms", "feeling", "health", "should i", "do i have",
                  "pain", "fever", "sick", "disease", "medical", "treatment", "medicine",
                  "doctor", "illness", "condition", "cure"],
        "Travel Guide": ["where should", "best place", "how to get", "visit", "trip", "vacation",
                        "travel", "destination", "hotel", "flight", "tour", "sightseeing",
                        "country", "city", "airport", "recommend"],
        "Chef": ["recipe", "how to make", "cooking", "ingredients", "prepare", "cook", "bake",
                "dish", "food", "meal", "sauce", "ingredient", "seasoning", "taste", "flavor"],
        "Tech Support": ["error", "not working", "how to fix", "install", "setup", "problem",
                        "crash", "bug", "computer", "software", "hardware", "debug", "troubleshoot",
                        "code", "program", "network", "connection"]
    }

    if personality in common_phrases:
        for phrase in common_phrases[personality]:
            if phrase in cleaned_input:
                return {
                    "allowed": True,
                    "response": ""
                }

    # If no keywords or common phrases found, refuse the question
    return {
        "allowed": False,
        "response": refuse_message
    }


def format_chat_message(role: str, content: str) -> Dict[str, str]:
    """
    Format a chat message.

    Args:
        role: 'user' or 'assistant'
        content: Message content

    Returns:
        Formatted message dictionary
    """
    return {
        "role": role,
        "content": content
    }


def truncate_messages(messages: list, max_messages: int = 20) -> list:
    """
    Truncate messages to keep only the most recent ones to avoid context overflow.

    Args:
        messages: List of messages
        max_messages: Maximum number of messages to keep

    Returns:
        Truncated messages list
    """
    if len(messages) > max_messages:
        return messages[-max_messages:]
    return messages


def validate_groq_response(response: str) -> bool:
    """
    Validate that a Groq response is not empty and contains text.

    Args:
        response: Response from Groq API

    Returns:
        True if valid, False otherwise
    """
    return bool(response and response.strip())
