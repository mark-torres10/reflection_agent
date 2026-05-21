"""Hello-world Streamlit entrypoint."""

import streamlit as st

st.set_page_config(page_title="Reflection Agent", page_icon="👋")
st.title("Hello, Reflection Agent!")
st.write("Streamlit is running. LangChain is installed and ready for the next step.")

name = st.text_input("Your name", placeholder="World")
if name:
    st.success(f"Hello, {name}!")
