import together
import requests
from graphql import graphql_sync, build_schema


from config.configuration import (
    TOGETHER_API_KEY,
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

    response = requests.post(
        url=model,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": output_length, 
                "top_p": top_p, 
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                "temperature": temperature,
                "do_sample": True,
                "return_full_text": False,
                "stop": ["</s>"]
            }
        }
    )

    if response.status_code!=200:
        raise Exception(f"Inference error {response.text}")
    return response


def validate_graphql_query(gql_query, sdl_schema):
    try:
        schema_obj = build_schema(sdl_schema)
        result = graphql_sync(schema_obj, gql_query)
        if result.errors:
            return {"error": str(result.errors)}
        return {"graphql_query": gql_query}
    except Exception as e:
        return {"error": str(e)}