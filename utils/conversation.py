from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Set your OpenAI API key (or Groq API key if supported by LangChain)
os.environ["OPENAI_API_KEY"] = "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"

def generate_response(prompt):
    """Generate a response using LangChain."""
    # Define the prompt template
    template = """
    You are a helpful assistant. Respond to the following prompt:
    {prompt}
    """
    prompt_template = PromptTemplate(input_variables=["prompt"], template=template)

    # Initialize the LLM (OpenAI or Groq if supported)
    llm = OpenAI(temperature=0.7)

    # Create the LLM chain
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Generate the response
    response = chain.run(prompt)
    return response