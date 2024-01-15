import os

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
ACCESS_PASSWORD = os.environ.get("ACCESS_PASSWORD")
LAMBDA_URL_MISTRAL_7B = os.environ.get("LAMBDA_URL_MISTRAL_7B")
LAMBDA_URL_LLAMA2_7B = os.environ.get("LAMBDA_URL_LLAMA2_7B")


DEFAULT_PROMPT_TEMPLATE_TOGETHER = """
<s>[INST] {human_query} [/INST]
"""

FINETUNED_PROMPT_TEMPLATE_TOGETHER = """
<s>[INST]<<SYS>>{system_prompt}<</SYS>>

Here's user question: "{human_query}"

SDL schema of {api} API is as follows:
{sdl}

Generate the GraphQL query for the user question in strict alignment to the SDL schema provided.
[/INST]
"""


FINETUNED_PROMPT_TEMPLATE_AWS = """
### Instruction
{system_prompt}

Following is the SDL schema for {api} API:
{sdl}

Based on the above API SDL schema and following user question: "{human_query}"

Generate the GraphQL query for the user question in strict alignment to the SDL schema provided.
"""


FINETUNED_PROMPT_TEMPLATE_AWS_ENHANCED = """
<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

{sdl}

User question: '{human_query}' [/INST]"
"""


MODEL_NAMES = [
    "mistral_7b_aws",
    "llama2_7b_aws",
]

MODEL_NAME_MAPPING = {
    "mistral_7b_aws": {
        "model_type": "aws",
        "model_name": LAMBDA_URL_MISTRAL_7B,
        "prompt_template": FINETUNED_PROMPT_TEMPLATE_AWS_ENHANCED,
        "sdl": "enhanced"
    },
    "llama2_7b_aws": {
        "model_type": "aws",
        "model_name": LAMBDA_URL_LLAMA2_7B,
        "prompt_template": FINETUNED_PROMPT_TEMPLATE_TOGETHER,
        "sdl": "normal"
    },
}

OUTPUT_LENGTH = {
    "min_length": 0,
    "max_length": 2048,
    "default_length": 512
}

TEMPERATURE = {
    "min_temperature": 0.0,
    "max_temperature": 1.0,
    "default_temperature": 0.01,
    "step": 0.01
}

TOP_P = {
    "min_val": 0.0,
    "max_val": 1.0,
    "default_val": 0.01,
    "step": 0.05
}

TOP_K = {
    "min_val": 0,
    "max_val": 100,
    "default_val": 20,
}

REPETITION_PENALTY = {
    "min_val": 1.0,
    "max_val": 2.0,
    "default_val": 1.3,
    "step": 0.1
}

API_SELECTION = [
    "--select--",
    "Poaps",
    "TokenBalances",
    "TokenNfts",
    "Socials"
]