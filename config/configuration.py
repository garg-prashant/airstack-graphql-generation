import os

LLAMA2_7B_CHAT = os.environ.get("LLAMA2_7B_CHAT")
CODELLAMA_7B = os.environ.get("CODELLAMA_7B")
MISTRALAI_7B = os.environ.get("MISTRALAI_7B")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

PROMPT_TEMPLATE = \
"""<s>[INST]You are Airstack AI assistant and an expert at understanding the Socials API GraphQL schema and using it you are able to generate syntactically correct GraphQL queries that will fetch Web3 data for a given user query.

Instructions:
- Use the SDL for Socials API.
- ENS (.eth, .cb.id) and Lens(.lens) name do not need a prefix.
- Farcaster username or ID, use it as owner in your query input. Add the 'fc_fname:' prefix before Farcaster name (like 'fc_fname:vbuterin') , or 'fc_fid:' for Farcaster ID (like 'fc_fid:60'). Farcaster names and IDs do not contain '.eth' nor ‘.lens’ nor'lens/@'.
- Lens profileName is lens/@examplename, profileHandle is @examplename either can be used as Identity without any modfication. 
- Do not use the prefix 'fc_fid' if it is the '0x' address.

User query: {human_query}
[/INST]"""


MODEL_NAMES = [
    "llama2-7b-chat",
    "codellama2-7b",
    "mistralai-7b",
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
     "mistralai-7b": {
        "model_type": "aws",
        "model_name": MISTRALAI_7B
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