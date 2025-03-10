import os
import yaml


def get_prompts_dir() -> str:
    """ Get prompts directory. """

    current_directory = os.path.dirname(__file__)
    prompt_dir = os.path.join(current_directory, 'prompts')
    return os.path.abspath(prompt_dir)

def load_prompt_file(prompt_file_name: str) -> dict:
    """ Load prompt file. """

    prompt_dir = get_prompts_dir()
    path_to_file = os.path.join(prompt_dir, prompt_file_name)

    with open(path_to_file, "r") as file:
        config = yaml.safe_load(file)

    return config

def construct_prompt_from_yaml(config: dict, course_description: str) -> str:
    """ Construct prompt from yaml. """

    raw_prompt_template = config["open_ai_prompt"]
    return raw_prompt_template.format(course_description=course_description)
        