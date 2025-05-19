from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Or your Groq key if supported

def generate_response(history, user_input):
    """Generate a conversational response using LangChain."""
    # Combine history into a single prompt
    conversation = ""
    for speaker, text in history:
        conversation += f"{speaker}: {text}\n"
    conversation += f"User: {user_input}\nAssistant:"

    template = "{conversation}"
    prompt_template = PromptTemplate(input_variables=["conversation"], template=template)
    llm = OpenAI(temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(conversation=conversation)
    return response.strip()