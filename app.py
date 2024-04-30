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
st.markdown("### Welcome to the Lyzr Neurology Consultant!")

query=st.text_area("Enter your conversation: ")

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


if st.button("Consult"):
    solution = neurology_consult(query)
    st.markdown(solution)

