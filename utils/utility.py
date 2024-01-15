import os
import streamlit as st
from config.configuration import (
    ACCESS_PASSWORD
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