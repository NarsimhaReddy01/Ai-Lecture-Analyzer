# backend/app/utils/summarizer.py

def summarize_text(text: str) -> str:
    """
    Simple summarization function.
    Currently returns first 3 sentences as summary.
    """
    if not text:
        return ""

    # Split text into sentences
    sentences = text.split(". ")
    summary_sentences = sentences[:3]  # take first 3 sentences
    summary = ". ".join(summary_sentences)

    # Ensure it ends with a period
    if not summary.endswith("."):
        summary += "."

    return summary
