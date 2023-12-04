import os

LLAMA2_7B_CHAT = os.environ.get("LLAMA2_7B_CHAT")
CODELLAMA_7B = os.environ.get("CODELLAMA_7B")
MISTRALAI_7B_QLORA = os.environ.get("MISTRALAI_7B_QLORA")
MISTRALAI_7B_FSDP = os.environ.get("MISTRALAI_7B_FSDP")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
LAMBDA_URL=os.environ.get("LAMBDA_URL")

PROMPT_TEMPLATE_TOGETHER = \
"""<s>[INST]You are Airstack AI assistant and an expert at understanding the Socials API GraphQL schema and using it you are able to generate syntactically correct GraphQL queries that will fetch Web3 data for a given user query.

Instructions:
- dappName should be included in the output
- Farcaster username or ID, use it as owner in your query input. Add 'fc_fname:' prefix before Farcaster name (like 'fc_fname:vbuterin') , or 'fc_fid:' for Farcaster ID (like 'fc_fid:60'). Farcaster names and IDs do not contain '.eth' nor ‘.lens’ nor'lens/@''.
- You must not not use prefixes 'fc_fid or 'lens/@'' if Identity is a full address like '0xB59Aa5Bb9270d44be3fA9b6D67520a2d28CF80AB'.
- use identity filter for ENS names (.eth, .cb.id), lens handles (.lens) and Ethereum wallet addresses. 
- If Farcaster profile name, Farcaster profile details or social profile details are requested in my question, you should return profileName and other profile details related fields from socials object in the query.

User question: {human_query}

Note: Do not create a GraphQL query if the user question does not make sense or does not comply with the SDL schema of the Social API. Instead, simply say "I do not know how to answer this at this time."
[/INST]"""


# PROMPT_TEMPLATE_AWS = """
# ### Instruction
# You are Airstack AI assistant and an expert at understanding the Socials API GraphQL schema and using it you are able to generate syntactically correct GraphQL queries that will fetch Web3 data for a given user query.

# Instructions:
# - dappName should be included in the output
# - Farcaster username or ID, use it as owner in your query input. Add 'fc_fname:' prefix before Farcaster name (like 'fc_fname:vbuterin') , or 'fc_fid:' for Farcaster ID (like 'fc_fid:60'). Farcaster names and IDs do not contain '.eth' nor ‘.lens’ nor'lens/@''.
# - You must not not use prefixes 'fc_fid or 'lens/@'' if Identity is a full address like '0xB59Aa5Bb9270d44be3fA9b6D67520a2d28CF80AB'.
# - use identity filter for ENS names (.eth, .cb.id), lens handles (.lens) and Ethereum wallet addresses. 
# - If Farcaster profile name, Farcaster profile details or social profile details are requested in my question, you should return profileName and other profile details related fields from socials object in the query.

# User question: "{human_query}"

# Note: Do not create a GraphQL query if the user question does not make sense or does not comply with the SDL schema of the Social API. Instead, simply say "I do not know how to answer this at this time."
# """

PROMPT_TEMPLATE_AWS = """
### Instruction
{human_query}
"""

MODEL_NAMES = [
    # "llama2-7b-chat",
    # "codellama2-7b",
    "mistralai-7b-fsdp",
    "mistralai-7b-qlora"
]

MODEL_NAME_MAPPING = {
    "llama2-7b-chat": {
        "model_type": "together",
        "model_name": LLAMA2_7B_CHAT    
    },
    "codellama2-7b": {
        "model_type": "together",
        "model_name": CODELLAMA_7B
    },
    "mistralai-7b-qlora": {
        "model_type": "aws",
        "model_name": MISTRALAI_7B_QLORA
    },
    "mistralai-7b-fsdp": {
        "model_type": "aws",
        "model_name": MISTRALAI_7B_FSDP
    }
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
    "default_val": 1.0,
    "step": 0.1
}