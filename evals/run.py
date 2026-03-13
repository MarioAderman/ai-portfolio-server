"""
Run prompt evaluation experiments.

Compares system prompt variants against the test dataset,
scoring with word count and LLM-judge evaluators.
Results are pushed to LangSmith.

Usage:
    uv run python -m evals.run              # run all variants
    uv run python -m evals.run --only b     # run only prompt_b_concise
    uv run python -m evals.run --only a     # run only prompt_a_current
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq
from langsmith import Client, evaluate

from evals.dataset import DATASET_NAME, TEST_INPUTS
from evals.evaluators import accuracy, completeness, under_50_words, word_count
from evals.prompts import PROMPTS

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"


def call_llm(system_prompt: str, user_query: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    ls = Client()

    # Create or reuse dataset
    try:
        dataset = ls.read_dataset(dataset_name=DATASET_NAME)
        print(f"Reusing existing dataset: {DATASET_NAME}")
    except Exception:
        dataset = ls.create_dataset(
            dataset_name=DATASET_NAME,
            description="Test prompts for portfolio agent prompt evaluation",
        )
        for inp in TEST_INPUTS:
            ls.create_example(inputs=inp, dataset_id=dataset.id)
        print(f"Created dataset: {DATASET_NAME} ({len(TEST_INPUTS)} examples)")

    # Filter variants if --only flag is passed
    variants = PROMPTS
    if "--only" in sys.argv:
        idx = sys.argv.index("--only") + 1
        if idx < len(sys.argv):
            key = sys.argv[idx].lower()
            variants = {k: v for k, v in PROMPTS.items() if key in k}

    # Run experiments for each prompt variant
    for variant_name, system_prompt in variants.items():
        print(f"\n{'='*60}")
        print(f"Running experiment: {variant_name}")
        print(f"{'='*60}")

        def make_target(sp):
            def target(inputs: dict) -> dict:
                response = call_llm(sp, inputs["query"])
                return {"response": response}
            return target

        evaluate(
            make_target(system_prompt),
            data=DATASET_NAME,
            evaluators=[word_count, under_50_words, accuracy, completeness],
            experiment_prefix=variant_name,
        )

    print("\nDone! Check LangSmith for results.")


if __name__ == "__main__":
    main()
