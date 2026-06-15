import streamlit as st
import asyncio

from main import run_agent

st.title("Travel Planning Agent")

query = st.text_input(
    "Where would you like to travel?"
)

if st.button("Plan Trip"):

    with st.spinner("Researching..."):

        result = asyncio.run(
            run_agent(query)
        )

    st.write(result)