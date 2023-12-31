import os

LLAMA2_7B_CHAT = os.environ.get("LLAMA2_7B_CHAT")
CODELLAMA_7B = os.environ.get("CODELLAMA_7B")
MISTRALAI_7B_QLORA = os.environ.get("MISTRALAI_7B_QLORA")
MISTRALAI_7B_FSDP = os.environ.get("MISTRALAI_7B_FSDP")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
MIXTRAL_MODEL = os.environ.get("MIXTRAL_MODEL") 
LAMBDA_URL=os.environ.get("LAMBDA_URL")
ACCESS_PASSWORD = os.environ.get("ACCESS_PASSWORD")
FINETUNED_LLAMA2_7B_CHAT = os.environ.get("FINETUNED_LLAMA2_7B_CHAT")

# PROMPT_TEMPLATE_TOGETHER = \
# """<s>[INST]You are Airstack AI assistant and an expert at understanding the Socials API GraphQL schema and using it you are able to generate syntactically correct GraphQL queries that will fetch Web3 data for a given user query.

# Instructions:
# - dappName should be included in the output
# - Farcaster username or ID, use it as owner in your query input. Add 'fc_fname:' prefix before Farcaster name (like 'fc_fname:vbuterin') , or 'fc_fid:' for Farcaster ID (like 'fc_fid:60'). Farcaster names and IDs do not contain '.eth' nor ‘.lens’ nor'lens/@''.
# - You must not not use prefixes 'fc_fid or 'lens/@'' if Identity is a full address like '0xB59Aa5Bb9270d44be3fA9b6D67520a2d28CF80AB'.
# - use identity filter for ENS names (.eth, .cb.id), lens handles (.lens) and Ethereum wallet addresses. 
# - If Farcaster profile name, Farcaster profile details or social profile details are requested in my question, you should return profileName and other profile details related fields from socials object in the query.

# User question: {human_query}

# Note: Do not create a GraphQL query if the user question does not make sense or does not comply with the SDL schema of the Social API. Instead, simply say "I do not know how to answer this at this time."
# [/INST]"""


PROMPT_TEMPLATE_TOGETHER = """
<s>[INST] {human_query} [/INST]
"""

FT_PROMPT_TEMPLATE_TOGETHER = """
<s>[INST]<<SYS>>{system_prompt}<</SYS>>

Here's user question: "{human_query}"

SDL schema of {api} API is as follows:
{sdl}

Generate the GraphQL query for the user question in strict alignment to the SDL schema provided.
[/INST]
"""


PROMPT_TEMPLATE_AWS = """
### Instruction
{system_prompt}

Following is the SDL schema for {api} API:
{sdl}

Based on the above API SDL schema and following user question: "{human_query}"

Generate the GraphQL query for the user question in strict alignment to the SDL schema provided.
"""

MODEL_NAMES = [
    "mixtral_model_8*7B",
    "ft_tog_llama2_7b_chat",
    "ft_aws_llama2_7b_chat",
]

MODEL_NAME_MAPPING = {
    "mixtral_model_8*7B": {
        "model_type": "together",
        "model_name": MIXTRAL_MODEL,
        "prompt_template": PROMPT_TEMPLATE_TOGETHER
    },
    "ft_tog_llama2_7b_chat": {
        "model_type": "together",
        "model_name": FINETUNED_LLAMA2_7B_CHAT,
        "prompt_template": FT_PROMPT_TEMPLATE_TOGETHER
    },
    # "ft_aws_llama2_7b_chat": {
    #     "model_type": "aws",
    #     "model_name": "",
    #     "prompt_template": FT_PROMPT_TEMPLATE_TOGETHER
    # }
}

OUTPUT_LENGTH = {
    "min_length": 0,
    "max_length": 4096,
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