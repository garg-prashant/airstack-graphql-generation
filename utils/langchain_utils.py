from langchain_community.llms import AmazonAPIGateway
from langchain.prompts import PromptTemplate
from graphql import graphql_sync, build_schema
from utils.utility import fetch_airstack_complete_sdl
from langchain_core.runnables import RunnableLambda
from config.configuration import GRAPHQL_SYNTAX_RECTIFIER


complete_sdl = fetch_airstack_complete_sdl()


LLM = None


def get_llm(endpoint_url: str, model_kwargs: dict = None):
    return AmazonAPIGateway(api_url=endpoint_url, model_kwargs=model_kwargs)


def update_llm(new_value):
    global LLM
    LLM = new_value


def validate_graphql_query(gql_query:str):
    try:
        schema_obj = build_schema(complete_sdl)
        result = graphql_sync(schema_obj, gql_query)
        if result.errors:
            return {"graphql_query": gql_query, "validation_errors": str(result.errors)}
        return {"graphql_query": gql_query, "validation_errors": ""} 
    except Exception as e:
        return {"graphql_query": gql_query, "validation_errors": str(e)}  
    

def output_fetcher(info_metadata):
    if info_metadata.get("validation_errors"):
        return info_metadata
    else:
        return info_metadata.get("graphql_query")


def get_graphql_generator_template(formatted_template: str):
    graphql_generator_template: PromptTemplate = PromptTemplate(
        input_variables=["human_query"],
        template=formatted_template,
        output_key="graphql_query"
    ) 
    return graphql_generator_template


def get_rectifier_generator_template():
    rectifier_generator_template: PromptTemplate = PromptTemplate(
        input_variables=["graphql_query", "validation_errors"], 
        template=GRAPHQL_SYNTAX_RECTIFIER
    )
    return rectifier_generator_template


def graphql_generator_route(info_metadata):
    if info_metadata.get("graphql_query") and not info_metadata.get("validation_errors"):
        return info_metadata.get("graphql_query")
    else:
        return get_rectifier_generator_template() | LLM 
    

def generate_graphql(formatted_template: str, human_query: str, llm: AmazonAPIGateway = None):
    update_llm(llm)
    runnable = get_graphql_generator_template(formatted_template) | LLM | validate_graphql_query | RunnableLambda(graphql_generator_route)
    return runnable.invoke({"human_query": human_query})