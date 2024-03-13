import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import pathlib
import textwrap

import google.generativeai as genai
from PIL import Image
from IPython.display import display_pdf, Markdown

###     this is one of two approaches the project could take:
###     we ask GPT if the webpage is time-wasting based on some inputs we collect with the web extension.


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "***API_KEY***"  
os.environ["GEMENI_API_KEY"] = "***API_KEY***"    # use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

def determine_timewasting_percentage(title, parsed_data, url):
    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", streaming=True)

    # Tool
    grade_tool_oai = convert_to_openai_tool(grade)

    # LLM with tool and enforce invocation
    llm_with_tool = model.bind(
        tools=[grade_tool_oai],
        tool_choice={"type": "function", "function": {"name": "grade"}},
    )

    # Parser
    parser_tool = PydanticToolsParser(tools=[grade])

    # Prompt
    prompt = PromptTemplate(
        template="""Based on information given to you of a webpage, please determine if the webpage is productive. \n
        The only resources you are given to determine if a student is being productive are a few items. Here they are: \n
        web page title:  {title}, a hashtag parsed from the web page: {parsed_data}, and the url: {url}\n
        If the student is wasting their time on the webpage please respond 'yes' and if the student is not please respond 'no'.""",
        input_variables=["title", "parsed_data", "url"]
    )

    # Chain
    chain = prompt | llm_with_tool | parser_tool

    score = chain.invoke({"title": title, "parsed_data": parsed_data, "url": url})
    return score[0].binary_score


def image_classification(image_filename):

    genai.configure(api_key="AIzaSyAke1uPmzMR3dpXSE--PXdfEsNUFaMOvsQ")

    model = genai.GenerativeModel("gemini-pro-vision")

    #img = Image.open(image_filename)

    response = model.generate_content(["""this is a screenshot of a webpage a student is on, they should be studying or being productive. \n
                                       Determine the purpose of the webpage and if the student is likely wasting their time on it.\n
                                       if the webpage is wasting time please respond with 'yes', if not respond 'no'.""",
                                        image_filename], stream=True)
    response.resolve()

    return response.text


def main():
    print(determine_timewasting_percentage("funny memes compilation", "#funnymemes", "https://youtube.com/video/37958274985"))
    print(determine_timewasting_percentage("how to take the derivative of a function", "#calculushelp", "https://calculus.com"))

    #print(image_classification("test.png"))   test.png doesnt exist right now

if __name__ == "__main__":
    main()
