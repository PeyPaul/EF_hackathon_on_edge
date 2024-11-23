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

model_id = "axel-darmouni/paligemma_saving"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to(device)

prompt = "Task: Je cherche un vol de Paris \u00e0 Palermo du dimanche 29 d\u00e9cembre 2024 au lundi 30 d\u00e9cembre 2024 \n Action:"
for i in range(1):
  for j in range(4):
    image_file = f"example_images/dataset1/run{i}_image{j+1}.png"
    print(image_file)
    raw_image = Image.open(image_file)
    paligemma_prompt = "<image>" + prompt + "<bos>"
    inputs = processor(paligemma_prompt, raw_image.convert("RGB"), return_tensors="pt").to(device)
    output = model.generate(**inputs, max_new_tokens=200)

    print(processor.decode(output[0], skip_special_tokens=True)[len(prompt):])