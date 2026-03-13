"""Evaluators for portfolio agent responses."""

import os

from groq import Groq

GROQ_MODEL = "llama-3.1-8b-instant"


def word_count(run, example) -> dict:
    """Raw word count of the response."""
    output = run.outputs.get("response", "")
    count = len(output.split())
    return {"key": "word_count", "score": count, "comment": f"{count} words"}


def under_50_words(run, example) -> dict:
    """Binary pass/fail: is the response 50 words or fewer?"""
    output = run.outputs.get("response", "")
    count = len(output.split())
    return {"key": "under_50_words", "score": 1 if count <= 50 else 0}


def relevance(run, example) -> dict:
    """LLM judge: is the response relevant and accurate? (1-5 scaled to 0-1)"""
    query = example.inputs.get("query", "")
    response = run.outputs.get("response", "")

    judge_prompt = f"""Rate the following response on relevance and accuracy (1-5).
The response should directly answer the question using only Mario's portfolio data.
5 = perfectly relevant and accurate
3 = partially relevant or includes unnecessary info
1 = irrelevant or incorrect

Question: {query}
Response: {response}

Reply with ONLY a single number 1-5."""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    result = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": judge_prompt}],
        max_tokens=5,
        temperature=0,
    )
    try:
        score = int(result.choices[0].message.content.strip()[0])
    except (ValueError, IndexError):
        score = 3
    return {"key": "relevance", "score": score / 5}
