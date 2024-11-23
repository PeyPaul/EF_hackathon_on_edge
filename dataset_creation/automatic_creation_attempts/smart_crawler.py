"""Failed methods but kept for consignation purposes."""

import os
import re
import base64
from PIL import Image
from openai import OpenAI
from parser import Parser


class SmartCrawler:
    def __init__(self, prompt=None):
        self.parser = Parser()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.prompt = """
Given this image, output a selenium python code that performs an action and moves us forward in completing one and only one step of the following task: Select the lowest cost flight from Paris to New York from 10th December to 12th December.

Output your code in <selenium></selenium> brackets.
Assume all imports are already done, we only want ONE line of python code of what to do next.
""" if prompt is None else prompt
        
    
    def parse_response(self, response):
        # we want to get the code from the response between <selenium></selenium> brackets
        try:
            return re.search(r'<selenium>(.*?)</selenium>', response.choices[0].message.content).group(1)
        except:
            print("No code found in response: ", response.choices[0].message.content)
            return None
    
    def send_image_with_text(self, image, text, resize_factor=15, use_parser=True):
        image = Image.fromarray(image) if use_parser else Image.open(image)
        image = image.resize((image.width // resize_factor, image.height // resize_factor))
        image_data = base64.b64encode(image.tobytes()).decode("utf-8")
        messages = [
            {"role": "system", "content": text},
            {"role": "user", "content": image_data}
        ]
        response = self.client.chat.completions.create(model="gpt-4o", messages=messages)
        return response

    def get_next_step(self, image, fails=3, resize_factor=16, use_parser=True):
        if use_parser:
            _, image_with_elements = self.parser.parse(image)
        else:
            image_with_elements = image
        for _ in range(fails):
            response = self.send_image_with_text(image_with_elements, self.prompt, resize_factor, use_parser)
            code = self.parse_response(response)
            if code:
                return code
            else:
                print("Trying again...")
        return None


if __name__ == "__main__":
    smart_crawler = SmartCrawler()
    print(smart_crawler.get_next_step("flights_test.png", use_parser=False))