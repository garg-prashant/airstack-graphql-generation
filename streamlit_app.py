import streamlit as st
from config.configuration import (
    MODEL_NAMES,
    MODEL_NAME_MAPPING,
    OUTPUT_LENGTH,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    REPETITION_PENALTY
)
from dotenv import load_dotenv, find_dotenv
import traceback
from utils.inference_utils import (
    generate_airstack_graphql_by_together,
    generate_airstack_graphql_by_aws
)
from utils.utility import check_password


def main():

    if not check_password():
        return

    with st.sidebar:
        st.header("Model")
        model = st.selectbox(
            "Choose a model:",
            MODEL_NAMES
        )

        st.header("Modifications")
        # You can add components here that allow users to specify modifications
        
        st.header("Parameters")
        output_length = st.slider("Output Length", min_value=OUTPUT_LENGTH.get("min_length"), max_value=OUTPUT_LENGTH.get("max_length"), value=OUTPUT_LENGTH.get("default_length"))
        temperature = st.slider("Temperature", min_value=TEMPERATURE.get("min_temperature"), max_value=TEMPERATURE.get("max_temperature"), value=TEMPERATURE.get("default_temperature"), step=TEMPERATURE.get("step"))
        top_p = st.slider("Top-P", min_value=TOP_P.get("min_val"), max_value=TOP_P.get("max_val"), value=TOP_P.get("default_val"), step=TOP_P.get("step"))
        top_k = st.slider("Top-K", min_value=TOP_K.get("min_val"), max_value=TOP_K.get("max_val"), value=TOP_K.get("default_val"))
        repetition_penalty = st.slider("Repetition Penalty", min_value=REPETITION_PENALTY.get("min_val"), max_value=REPETITION_PENALTY.get("max_val"), value=REPETITION_PENALTY.get("default_val"), step=REPETITION_PENALTY.get("step"))

        
    st.title("Airstack LLM Inferences")

    input_prompt = st.text_area(
        "Insert a prompt below", 
        placeholder="What is 1+1?",
        max_chars=5000, height=500)

    generate_graphql = st.button("Get Response")

    model_metadata = MODEL_NAME_MAPPING.get(
        model
    )
    model_type = model_metadata.get("model_type")
    model_name = model_metadata.get("model_name")

    try:
        if generate_graphql and input_prompt:
            with st.spinner("Hold tight! Generating response for you..."):
                if model_type == "together":
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
                elif model_type == "aws":
                    response = generate_airstack_graphql_by_aws(
                        model=model_name,
                        output_length=output_length,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k,
                        repetition_penalty=repetition_penalty,
                        prompt=input_prompt
                    )
            if response and model_type == "together":
                st.header("Generated Response")
                st.text_area(f"Model used: {model}", value=response.replace("```", ""), height=400, disabled=True, key="ct")
            elif response and model_type == "aws":
                response = response.json()
                if response and isinstance(response, list):
                    response = response[0]
                response = response.get("generated_text")
                response = response.strip()
                st.header("Generated Response")
                st.text_area(f"Model used: {model}", value=response.replace("### Answer", " "), height=400, disabled=True, key="ct")
        elif generate_graphql and not input_prompt:
            st.error("Enter a question for which the GraphQL is to be generated!")
    except Exception:
        error_trace = str(traceback.format_exc())
        if "Not Found for url" in error_trace:
            st.error(f"Model {model} is not running currently. Contact Airstack (info@airstack.xyz) to activate it.")
        else:
            st.error(f"Error: {traceback.format_exc()}")

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    main()
