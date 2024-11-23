import json
import random

with open("../big_dataset/metadata_parsed.json", "r") as f:
    metadata = json.load(f)

prompts = [
    """INSTRUCTIONS
You are a virtual agent navigating a website to fulfill a specified TASK. Based on the current image that represents your progress, and the list of interactive elements below, select exactly ONE ACTION from the list of ACTIONS to move one step closer to completing the TASK.

DO NOT provide any explanations or descriptions. Respond only with an ACTION. Your choice should reflect the current state of the TASK as shown in the image.
""",
"""INSTRUCTIONS
You are tasked to act as an automated agent completing a TASK on a website. Analyze the provided image, which reflects the current progress, and use the list of ACTIONS to determine the next step to advance the TASK.

Provide exactly ONE ACTION from the list below. No explanation or description is needed—just the ACTION.
""",
"""INSTRUCTIONS
Assume the role of an agent completing a specific TASK by interacting with a website. Based on the provided image, determine the most appropriate ACTION from the list to progress the TASK.

DO NOT explain or elaborate—respond with ONE and ONLY ONE ACTION.
""",
"""INSTRUCTIONS
Imagine yourself as a system agent navigating a website. You are given a current snapshot of your state in the form of an image. Use this visual state to choose a single ACTION from the list below to advance one step toward completing the TASK.

Only answer with an ACTION. Avoid explanations.
""",
"""INSTRUCTIONS
You are a web navigation agent performing a TASK. Based on the visual state provided in the form of an image, select exactly ONE ACTION from the list below that best progresses the TASK.

Your response should only include the ACTION, no explanations.
""",
"""INSTRUCTIONS
You are operating as an automated agent solving a web-based TASK. From the provided image of the current state, select ONE ACTION from the list below to move forward.

Your response must be concise: provide only the ACTION, no further elaboration.
""",
"""INSTRUCTIONS
Act as a virtual assistant completing a web task. Using the provided image that depicts your current state, choose ONE ACTION from the list below to progress further.

Provide the ACTION only—no additional details.
""",
"""INSTRUCTIONS
You are a task-oriented agent navigating a web interface. Given the current state as displayed in the image, identify and execute exactly ONE ACTION from the list below to advance.

Respond solely with the ACTION. No explanation is required.
"""
]

task = """# TASK
Your task to complete is:
Order the cheapest flight from {from_city} to {to_city} leaving on {from_date} and arriving {to_date}"""

elements = """# ELEMENTS
{elements}"""

actions = """#ACTIONS
click(x, y) - Perform a click at (x, y)
click_and_type(x, y, text) - Insert text into the field at (x, y)
type(text) - Insert text field
scroll(i) - Scroll down i units
end() - Finish action, when the task is completed
"""


def create_prompt(entry, index):
    prompt = random.choice(prompts)
    prompt += "\n\n" + actions
    prompt += "\n\n" + task.format(**entry)
    prompt += "\n\n" + elements.format(elements="\n".join(str(element) for element in entry["elements"][index]))
    return prompt

def create_action(entry, index):
    delta_x = random.randint(-10, 10)
    delta_y = random.randint(-10, 10)
    delta_i = random.randint(-10, 10)
    actions_dic = {
        0:f"clik_and_type({150 + delta_x},{150 + delta_y}, '{entry['from_city']}')",
        1:f"clik_and_type({350 + delta_x},{250 + delta_y}, '{entry['to_city']}')",
        2:f"clik_and_type({150 + delta_x},{350 + delta_y}, '{entry['from_date']}'" +"TAB)",
        3:f"type('{entry['to_date']}')",
        4:f"click({480 + delta_x},{480 + delta_y})",
        5:f"click({250 + delta_x},{400 + delta_y})",
        6:f"click({300 + delta_x},{300 + delta_y})",
        7:f"scroll({250 + delta_i})"
    }
    return actions_dic[index]

def create_input(entry, index):
    return create_prompt(entry, index), entry["timestamps"][index]

def create_output(entry, index):
    reward = 1 if entry["positive"] else -1
    return create_action(entry, index), reward

def create_datapoint(entry, index):
    input_prompt, input_timestamp = create_input(entry, index)
    output_action, reward = create_output(entry, index)
    return {
        "input_prompt": input_prompt,
        "input_timestamp": input_timestamp,
        "output_action": output_action,
        "reward": reward,
    }

def create_dataset(metadata):
    dataset = []
    for entry in metadata:
        for index in range(len(entry["timestamps"])):
            dataset.append(create_datapoint(entry, index))
    return dataset

