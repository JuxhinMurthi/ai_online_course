import openai
import os
from dotenv import load_dotenv
from dataclasses import field

from openai import OpenAI

from src.utils.helpers import construct_prompt_from_yaml, load_prompt_file

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class OpenAIService:
    """ OpenAI service. """

    def __init__(self):
        self.api_key: str = field(default=openai.api_key)
        self.open_api_prompt: dict = load_prompt_file("course_summary_prompt.yaml")

    def generate_summary(self, course_description: str) -> str:
        """ Generate course summary using OpenAI from course description. """

        self.open_api_prompt = construct_prompt_from_yaml(config=self.open_api_prompt, course_description=course_description)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": self.open_api_prompt,
                }
            ]
        )

        summary = response.choices[0].message.content
        return summary
