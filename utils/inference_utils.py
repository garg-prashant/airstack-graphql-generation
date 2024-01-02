import together
import requests

from config.configuration import (
    TOGETHER_API_KEY,
    LAMBDA_URL,
    PROMPT_TEMPLATE_AWS
)

together.api_key = TOGETHER_API_KEY
SYSTEM_PROMPT="""You are an Airstack AI assistant who can generate GraphQL queries for various Airstack APIs (e.g. Poaps, TokenBalances, Socials, TokenNfts, etc.) based on the instructions provided and the SDL schema of the API in response to the user's question."""


def format_prompt(template, **args):
    prompt = None

    args['system_prompt'] = SYSTEM_PROMPT
    if template:
        prompt = template.format(**args)

    return prompt


def generate_airstack_graphql_by_together(
    model,
    output_length,
    temperature,
    top_p,
    top_k,
    repetition_penalty,
    prompt
): 
    return together.Complete.create(
        model=model,
        prompt=prompt,
        max_tokens=output_length,
        stop="</s>",
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition_penalty
    )


def generate_airstack_graphql_by_aws(
    model,
    output_length,
    temperature,
    top_p,
    top_k,
    repetition_penalty,
    prompt
): 
    prompt = PROMPT_TEMPLATE_AWS.format(
        human_query=prompt
    )

    response = requests.post(
        url=LAMBDA_URL,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": output_length, 
                "top_p": top_p, 
                "temperature": temperature,
                "do_sample": True
            }
        }
    )

    if response.status_code!=200:
        raise Exception(f"Inference error {response.text}")
    return response