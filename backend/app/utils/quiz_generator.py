# backend/app/utils/quiz_generator.py

def generate_quiz(transcript_text: str) -> list:
    """
    Placeholder quiz generator.
    Returns a list of sample quiz questions.
    You can replace this with an AI-based question generator.
    """
    if not transcript_text:
        return []

    # Example: Generate 3 simple questions
    quiz = [
        {"question": "What is the main topic of the lecture?", "options": [], "answer": ""},
        {"question": "List one key point mentioned.", "options": [], "answer": ""},
        {"question": "What is the conclusion of the lecture?", "options": [], "answer": ""}
    ]

    return quiz
