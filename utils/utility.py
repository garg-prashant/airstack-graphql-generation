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