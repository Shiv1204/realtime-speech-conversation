from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from utils.text_to_speech import google_cloud_text_to_speech

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\santa\Downloads\gpt-voice-assistant-385505-8f3e6a7a7a0b.json"

def generate_response(history, user_input):
    """Generate a conversational response using LangChain and play it as voice."""
    conversation = ""
    for speaker, text in history:
        conversation += f"{speaker}: {text}\n"
    conversation += f"User: {user_input}\nAssistant:"

    template = (
        "You are a helpful, friendly assistant. Respond in a natural, conversational way.\n"
        "{conversation}"
    )
    prompt_template = PromptTemplate(input_variables=["conversation"], template=template)
    llm = ChatOpenAI(temperature=0.7, model_name="llama3-70b-8192")

    chain = prompt_template | llm

    response = chain.invoke({"conversation": conversation})
    response_text = response.content.strip()
    google_cloud_text_to_speech(response_text)  # Use Google Cloud TTS
    return response_text