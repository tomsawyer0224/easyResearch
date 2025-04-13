import streamlit as st
import time
def plan_response(topic):
    time.sleep(5)
    return f"here is your plan on the topic: {topic}"

def feedback_response(feedback):
    time.sleep(5)
    return f"plan with feedback: {feedback}"

def generate_final_report():
    time.sleep(5)
    return f"final report of the topic"
st.title("Research Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "final" not in st.session_state:
    st.session_state.final = False
def on_generate_click():
    st.session_state.final = True
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
with st.sidebar:
    topic = st.chat_input(
    "type your topic",
    )
    st.button("Generate report", on_click=on_generate_click)
feedback = st.chat_input(
    "feedback on the plan"
)
if topic:
    st.chat_message("user").markdown(topic)
    st.session_state.messages.append({"role": "user", "content": topic})
    with st.spinner("Generating report plan...", show_time=True):
        plan = plan_response(topic)
        with st.chat_message("assistant"):
            st.markdown(plan)
        st.session_state.messages.append({"role": "assistant", "content": plan})
if feedback:
    st.chat_message("user").markdown(feedback)
    st.session_state.messages.append({"role": "user", "content": feedback})
    with st.spinner("Processing your feedback...", show_time=True):
        plan = feedback_response(feedback)
        with st.chat_message("assistant"):
            st.markdown(plan)
        st.session_state.messages.append({"role": "assistant", "content": plan})
if st.session_state.final:
    with st.spinner("Generating the final report...", show_time=True):
        final_report = generate_final_report()
        with st.chat_message("assistant"):
            st.markdown(final_report)
        st.session_state.messages.append({"role": "assistant", "content": final_report})
    st.session_state.final = False
