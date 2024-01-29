import streamlit as st
from config.configuration import (
    MODEL_NAMES,
    MODEL_NAME_MAPPING,
    OUTPUT_LENGTH,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    REPETITION_PENALTY,
    API_SELECTION
)
from dotenv import load_dotenv, find_dotenv
import traceback
from utils.inference_utils import (
    generate_airstack_graphql_by_together,
    generate_airstack_graphql_by_aws,
    format_prompt,
)
from utils.utility import (
    check_password,
    create_sdl_map,
    create_enhanced_sdl_map,
    get_airstack_response,
    persist_response,
)
from utils.langchain_utils import (
    validate_graphql_query
)
from utils.database_utils import Base, engine
import time


def main(api_sdl_map, enhanced_api_sdl_map):

    if not check_password():
        return

    left_column, _, right_column = st.columns([0.55, 0.05,0.40])

    response = None
    generation_time = None
    miscellanous = {}

    with left_column:

        with st.sidebar:
            st.header("Model")
            model = st.selectbox(
                "Choose a model:",
                MODEL_NAMES
            )

            st.header("Modifications")
            # You can add components here that allow users to specify modifications
            
            st.header("Parameters")
            api_selection = st.selectbox(
                "Choose an API (**only for finetuned models**):",
                API_SELECTION
            )
            output_length = st.slider("Output Length", min_value=OUTPUT_LENGTH.get("min_length"), max_value=OUTPUT_LENGTH.get("max_length"), value=OUTPUT_LENGTH.get("default_length"))
            temperature = st.slider("Temperature", min_value=TEMPERATURE.get("min_temperature"), max_value=TEMPERATURE.get("max_temperature"), value=TEMPERATURE.get("default_temperature"), step=TEMPERATURE.get("step"))
            top_p = st.slider("Top-P", min_value=TOP_P.get("min_val"), max_value=TOP_P.get("max_val"), value=TOP_P.get("default_val"), step=TOP_P.get("step"))
            top_k = st.slider("Top-K", min_value=TOP_K.get("min_val"), max_value=TOP_K.get("max_val"), value=TOP_K.get("default_val"))
            repetition_penalty = st.slider("Repetition Penalty", min_value=REPETITION_PENALTY.get("min_val"), max_value=REPETITION_PENALTY.get("max_val"), value=REPETITION_PENALTY.get("default_val"), step=REPETITION_PENALTY.get("step"))
        
        st.title("Airstack LLM Inferences")

        input_prompt = st.text_area(
            "Insert your question here", 
            placeholder="Lens profile details of betashop.eth", height=50)
        human_query = input_prompt

        generate_graphql = st.button("Get Response")

        model_metadata = MODEL_NAME_MAPPING.get(
            model
        )
        model_type = model_metadata.get("model_type")
        model_name = model_metadata.get("model_name")
        model_prompt_template = model_metadata.get("prompt_template")
        sdl_type = model_metadata.get("sdl")

        try:
            response = None
            time_started = time.time()
            if generate_graphql and input_prompt and api_selection != "--select--":
                with st.spinner("Hold tight! Generating response for you..."):
                    template=model_prompt_template

                    if sdl_type == "enhanced":
                        api_sdl_map = enhanced_api_sdl_map

                    input_prompt = format_prompt(
                            template=template,
                            human_query='{human_query}',
                            api=api_selection,
                            sdl = api_sdl_map.get(api_selection).replace("{", "{{").replace("}", "}}"),
                        )
                    if model_type == "together":
                        if not input_prompt:
                            st.error("Please provide a valid input prompt.")
                        else:
                            response = generate_airstack_graphql_by_together(
                                model=model_name,
                                output_length=output_length,
                                temperature=temperature,
                                top_p=top_p,
                                top_k=top_k,
                                repetition_penalty=repetition_penalty,
                                prompt=input_prompt
                            )
                            response = response.get("output", {}).get("choices", [])[0].get("text")
                            if not response:
                                st.error("Could not generate the GraphQL query.")
                            generation_time = time.time() - time_started
                    elif model_type == "aws":
                        response = generate_airstack_graphql_by_aws(
                            model=model_name,
                            output_length=output_length,
                            temperature=temperature,
                            top_p=top_p,
                            top_k=top_k,
                            repetition_penalty=repetition_penalty,
                            formatted_template=input_prompt,
                            prompt=human_query
                        )
                        generation_time = time.time() - time_started
                if response and model_type == "together":
                    st.header("Generated Response")
                    response = response.replace("```", "")

                    validate_response = validate_graphql_query(response)
                    if validate_response.get("validation_errors"):
                        miscellanous = {
                            "response": response,
                            "error": validate_response.get("validation_errors")
                        }
                        response = f"Query '{human_query}' not supported by the SDL schema for '{api_selection}' API"
                    else:
                        response = validate_response.get("graphql_query")

                    st.text_area(f"Model used: {model}", value=response, height=400, disabled=True, key="ct")
                elif response and model_type == "aws":
                    
                    validate_response = validate_graphql_query(response)
                    if validate_response.get("validation_errors"):
                        miscellanous = {
                            "response": response,
                            "error": validate_response.get("validation_errors")
                        }
                        response = f"Query '{human_query}' not supported by the SDL schema for '{api_selection}' API"
                    else:
                        response = validate_response.get("graphql_query")
                    
                    st.text_area(f"Model used: {model}", value=response, height=400, disabled=True, key="ct")
            elif generate_graphql and not input_prompt:
                st.error("Enter a question for which the GraphQL is to be generated!")
            elif generate_graphql and api_selection == "--select--":
                st.error("Please select a valid API.")
        except Exception:
            error_trace = str(traceback.format_exc())
            if "Not Found for url" in error_trace:
                st.error(f"Model {model} is not running currently. Contact Airstack (info@airstack.xyz) to activate it.")
            else:
                st.error(f"Error: {traceback.format_exc()}")

    if response:
        with right_column:
            st.title("Results")

            data_response = ""
            if not miscellanous:
                data_response = get_airstack_response(response)
            st.text_area(f"Data response:", value=data_response, height=800, disabled=True, key="ct2")
            persist_response(
                model_name=model,
                selected_api=api_selection,
                human_query=human_query,
                graphql_query=response,
                response=str(data_response),
                generation_time=generation_time,
                miscellanous=miscellanous,
                model_parameters={
                    "output_length": output_length,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "repetition_penalty": repetition_penalty
                },
            )


if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    Base.metadata.create_all(bind=engine)
    api_sdl_map = create_sdl_map()
    enhanced_api_sdl_map = create_enhanced_sdl_map()
    main(
        api_sdl_map, 
        enhanced_api_sdl_map,
    )
