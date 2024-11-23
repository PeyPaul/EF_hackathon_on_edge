import os
import torch
from PIL import Image
from huggingface_hub import login
from transformers import PaliGemmaProcessor, PaliGemmaForConditionalGeneration,
from PIL import Image

login(token=os.environ.get("HUGGINGFACE_TOKEN"))
model_id = "google/paligemma-3b-pt-448"
processor = PaliGemmaProcessor.from_pretrained(model_id)
device = "cuda"
image_token = processor.tokenizer.convert_tokens_to_ids("<image>")
def collate_fn(examples):
  texts = ["<image>" + example["prefixes"] + "<bos>" for example in examples]
  labels= [example['suffixes'] for example in examples]
  images = [Image.open(f"runs/{example['images']}").convert("RGB") for example in examples]
  tokens = processor(text=texts, images=images, suffix=labels,
                    return_tensors="pt", padding="longest")
  tokens = tokens.to(torch.bfloat16).to(device)
  return tokens

model_id = "axel-darmouni/paligemma_dataset2"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to(device)

prompt = """INSTRUCTIONS
You are a virtual agent navigating a website to fulfill a specified TASK. Based on the current image that represents your progress, and the list of interactive elements below, select exactly ONE ACTION from the list of ACTIONS to move one step closer to completing the TASK.

DO NOT provide any explanations or descriptions. Respond only with an ACTION. Your choice should reflect the current state of the TASK as shown in the image.

#ACTIONS
click(element) - Perform a click on element
click_and_type(element, text) - Insert text into element
type(element, text) - Insert text into element
scroll(i) - Scroll down i units
end() - Finish action, when the task is completed

# TASK
Your task to complete is:
Order the cheapest flight from Paris to New York leaving on 2024-12-01 and arriving 2024-12-08

# ELEMENTS
{'x': 419, 'y': 21, 'w': 34, 'h': 18, 'text': 'Sign'}
{'x': 191, 'y': 156, 'w': 118, 'h': 50, 'text': 'Flights'}
{'x': 51, 'y': 215, 'w': 44, 'h': 16, 'text': 'Round'}
{'x': 248, 'y': 214, 'w': 63, 'h': 19, 'text': 'Economy'}
{'x': 65, 'y': 259, 'w': 63, 'h': 26, 'text': 'Perugia'}
{'x': 315, 'y': 265, 'w': 48, 'h': 16, 'text': 'Where'}
{'x': 77, 'y': 321, 'w': 78, 'h': 24, 'text': 'Departure'}
{'x': 331, 'y': 323, 'w': 50, 'h': 18, 'text': 'Return'}
{'x': 237, 'y': 379, 'w': 54, 'h': 16, 'text': 'Explore'}
{'x': 13, 'y': 439, 'w': 390, 'h': 29, 'text': 'Find cheap flights from Paris to anywhere'}"""
image_file = "example_images/dataset2/test_image.jpg"
raw_image = Image.open(image_file)
paligemma_prompt = "<image>" + prompt + "<bos>"
inputs = processor(paligemma_prompt, raw_image.convert("RGB"), return_tensors="pt").to(device)
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True)[len(prompt):])

