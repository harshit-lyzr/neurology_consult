import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os
from prompt import prompt

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Neurology Consultant",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Neurology Consultant")
st.markdown("This app uses lyzr automata to generate Medical note.")
st.sidebar.markdown("## Welcome to the Lyzr Neurology Consultant!")
st.sidebar.markdown("This app uses lyzr automata to generate medical note. User give a transcript of the doctor-patient encounter and based on conversation It generates Medical.")

query=st.sidebar.text_area("Enter your conversation: ")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def neurology_consult(query):

    neurology_agent = Agent(
            role="Neurology expert",
            prompt_persona=f"You are an Expert neurologist.your task is to create medical note from {query}."
        )

    neurology_task = Task(
        name="Neurology Consult",
        model=open_ai_text_completion_model,
        agent=neurology_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="Neurology Consult Pipline",
        completion_message="pipeline completed",
        tasks=[
              neurology_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


if st.sidebar.button("Consult"):
    solution = neurology_consult(query)
    st.markdown(solution)

with st.sidebar.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses lyzr automata to generate medical note. User give a transcript of the doctor-patient encounter and based on conversation It generates Medical. For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)

