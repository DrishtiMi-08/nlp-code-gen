import re

# Supported languages and their canonical names
LANGUAGE_ALIASES = {
    "c++": "C++",
    "cpp": "C++",
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "c": "C",
    "go": "Go",
    "rust": "Rust",
    "kotlin": "Kotlin",
    "swift": "Swift",
}

DEFAULT_LANGUAGE = "Python"


def detect_language(raw_input: str) -> tuple[str, str]:
    """
    Detects the programming language from the raw user input.

    Returns:
        (canonical_language, cleaned_input_without_language_mention)
    """
    lower = raw_input.lower()

    for alias, canonical in LANGUAGE_ALIASES.items():
        # Match whole word only (e.g. "c" shouldn't match "c++")
        pattern = r'\b' + re.escape(alias) + r'\b'
        if re.search(pattern, lower):
            # Remove the language mention from the input
            cleaned = re.sub(pattern, "", lower, flags=re.IGNORECASE).strip()
            cleaned = re.sub(r'\s+', ' ', cleaned)  # collapse extra spaces
            return canonical, cleaned

    return DEFAULT_LANGUAGE, raw_input.strip()


def build_prompt(raw_input: str) -> dict:
    """
    Takes raw user intent (after stripping @gen) and builds a
    structured prompt for CodeT5.

    Args:
        raw_input: e.g. "reverse an array in C++"

    Returns:
        dict with keys:
            - prompt     : the final string sent to the model
            - language   : detected language
            - intent     : cleaned intent without language mention
    """
    language, intent = detect_language(raw_input)

    # CodeT5 performs best with this instruction style
    prompt = (
        f"Generate a complete {language} program with comments "
        f"to: {intent}"
    )

    return {
        "prompt": prompt,
        "language": language,
        "intent": intent,
    }