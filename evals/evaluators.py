"""Evaluators for portfolio agent responses."""

import json
import os
import re
import time

from groq import Groq

from evals.prompts import DATA_BLOCK

JUDGE_MODEL = "llama-3.3-70b-versatile"


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


def _judge(prompt: str, max_retries: int = 5) -> dict:
    """Call the judge model and parse JSON response. Retries on rate limits."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    for attempt in range(max_retries):
        try:
            result = client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0,
            )
            return json.loads(result.choices[0].message.content.strip())
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str:
                # Parse wait time from error message, default to 60s
                match = re.search(r"try again in (\d+)m([\d.]+)s", error_str)
                if match:
                    wait = int(match.group(1)) * 60 + float(match.group(2)) + 1
                else:
                    wait = 60
                print(f"  Rate limited. Waiting {wait:.0f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                return {"judgment": "fail", "critique": f"Judge error: {error_str[:100]}"}
    return {"judgment": "fail", "critique": "Max retries exceeded on rate limit."}


def accuracy(run, example) -> dict:
    """Binary: is the information in the response factually correct?"""
    query = example.inputs.get("query", "")
    response = run.outputs.get("response", "")

    prompt = f"""You are evaluating a portfolio agent's response for factual accuracy.
The agent answers questions about Mario Aderman using the reference data below.

=== REFERENCE DATA ===
{DATA_BLOCK}
=== END REFERENCE DATA ===

Judge whether ALL facts in the response are correct based on the reference data above.
Do not penalize for brevity — only for incorrect or fabricated information.

<example>
<question>Does Mario know LangChain?</question>
<response>Yes, Mario has intermediate-level LangChain skills, including multi-agent systems and RAG.</response>
<evaluation>{{"judgment": "pass", "critique": "All stated facts are accurate — skill level and specializations match his portfolio data."}}</evaluation>
</example>

<example>
<question>What services does Mario offer?</question>
<response>Mario offers web development, SEO optimization, and cloud migration services.</response>
<evaluation>{{"judgment": "fail", "critique": "Fabricated services. Mario offers AI Workflow Automation, AI Chatbots & Agents, and LLM Integration — none of the listed services are correct."}}</evaluation>
</example>

Now evaluate:
<question>{query}</question>
<response>{response}</response>

Reply with ONLY a JSON object: {{"judgment": "pass" or "fail", "critique": "your reasoning"}}"""

    result = _judge(prompt)
    score = 1 if result.get("judgment") == "pass" else 0
    return {"key": "accuracy", "score": score, "comment": result.get("critique", "")}


def completeness(run, example) -> dict:
    """Binary: does the response address what was actually asked?"""
    query = example.inputs.get("query", "")
    response = run.outputs.get("response", "")

    prompt = f"""You are evaluating a portfolio agent's response for completeness.
The agent answers questions about Mario Aderman using the reference data below.

=== REFERENCE DATA ===
{DATA_BLOCK}
=== END REFERENCE DATA ===

Judge whether the response addresses the core of what was asked.
A short answer that hits the key point is a PASS. Missing the question entirely is a FAIL.
Do not penalize brevity — penalize only if the main question goes unanswered.

<example>
<question>Is Mario available for a project?</question>
<response>Yes, Mario is available 20-30 hours per week.</response>
<evaluation>{{"judgment": "pass", "critique": "Directly answers availability with specific hours. Concise and complete."}}</evaluation>
</example>

<example>
<question>What makes Mario different from other freelancers?</question>
<response>Mario is an AI Automation Engineer.</response>
<evaluation>{{"judgment": "fail", "critique": "States his title but doesn't address what differentiates him. The question asks for a distinguishing factor — his mechatronics background, automotive experience, or unique skill combination."}}</evaluation>
</example>

Now evaluate:
<question>{query}</question>
<response>{response}</response>

Reply with ONLY a JSON object: {{"judgment": "pass" or "fail", "critique": "your reasoning"}}"""

    result = _judge(prompt)
    score = 1 if result.get("judgment") == "pass" else 0
    return {"key": "completeness", "score": score, "comment": result.get("critique", "")}
