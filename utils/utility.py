import os
import requests
import streamlit as st
import traceback
from config.configuration import (
    ACCESS_PASSWORD,
    AIRSTACK_API_KEY
)


def check_password():
    if 'password_entered' not in st.session_state:
        st.session_state['password_entered'] = False

    # Create placeholders for password input and proceed button
    pwd_placeholder = st.empty()
    proceed_placeholder = st.empty()

    # If the password has not been entered yet, show the input and button
    if not st.session_state['password_entered']:
        pwd = pwd_placeholder.text_input("Enter Password:", type="password")
        if proceed_placeholder.button("Proceed"):
            if pwd == ACCESS_PASSWORD:
                st.session_state['password_entered'] = True
                pwd_placeholder.empty()  # Remove the password input if correct
                proceed_placeholder.empty()  # Remove the proceed button
            else:
                st.error("Incorrect password, please try again.")

    return st.session_state['password_entered']


def read_file_contents(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return content


def create_sdl_map():
    sdl_map = {}
    try:
        for file in os.listdir("sdl"):
            sdl_map[file.split(".txt")[0]] = read_file_contents(os.path.join("sdl", file))
        return sdl_map
    except Exception as err:
        raise Exception(f"Error while creating SDL map: {err}") 


def create_enhanced_sdl_map():
    sdl_map = {}
    try:
        for file in os.listdir("enhanced_sdl"):
            sdl_map[file.split(".txt")[0]] = read_file_contents(os.path.join("enhanced_sdl", file))
        return sdl_map
    except Exception as err:
        raise Exception(f"Error while creating SDL map: {err}") 
    

def get_airstack_response(graphql_query):
    if not graphql_query:
        return None
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AIRSTACK_API_KEY}"
        }
        response = requests.post(
            url="https://api.airstack.xyz/graphql",
            json={
                "query": graphql_query
            },
            headers=headers
        )
        if response.status_code!=200:
            raise Exception(f"Inference error {response.text}")
        return response.json()
    except Exception as err:
        error_message = traceback.format_exc()
        return {
            "error": f"Error while fetching airstack response: {error_message}"
        }