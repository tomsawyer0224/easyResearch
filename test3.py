import streamlit as st
import asyncio

async def f():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"# {i}"

st.markdown(st.write_stream(f()))
