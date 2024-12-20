# Robust Datasets for Vision-Language Web Agents

![Hackathon Overview](hackathon.png)

## Overview
This project focuses on creating robust datasets for training vision-language models (VLMs) to perform web-based tasks, with a particular emphasis on flight booking as a proof of concept. Our work demonstrates that smaller models (3B parameters) can effectively handle web navigation tasks when properly trained on specialized datasets.

## Background
Recent developments, such as H Runner, have shown that intelligence on the edge is possible with smaller models. While larger models like GPT-4 can handle web navigation tasks, smaller models like PaliGemma (3B) typically struggle. Our project aims to bridge this gap through specialized dataset creation and training.

## Project Goals
- Create a task and website-agnostic dataset creation pipeline
- Prove that smaller models (like PaliGemma) can learn specific web navigation tasks
- Generate robust datasets for vision-language web agents
- Develop automated methods for creating web navigation training data

## Methodology

### Dataset Creation Pipeline
1. Generate Playwright code using VLM
2. Extract both positive and negative trajectories for DPO (Direct Preference Optimization)
3. Create instruction tuning datasets from successful trajectories

### Two Dataset Approaches

You can find the datasets [here](https://huggingface.co/datasets/anonx3247/web_agents_google_flight_trajectories/tree/main)

#### Dataset 1: Screenshot to Playwright Code
- Input: Screenshot of web interface
- Output: Complete Playwright code for navigation
- Features: More comprehensive but less robust
- Can be automated using Large Language Models

#### Dataset 2: Simplified Action Prediction
- Input: Screenshot of web interface
- Output: Basic actions ("click", "click_and_type", "type", "scroll", "end")
- Features: More robust but less detailed
- Requires manual verification for better quality

## Implementation Details
The project utilizes several key components:
- Microsoft/OmniParser for trajectory parsing
- Playwright for web automation
- Vision-Language Models for code generation
- Custom pipeline for screenshot capture and trajectory evaluation

## Results
Our experiments show that:
- PaliGemma can successfully overfit to specific tasks like flight booking
- The simplified action prediction approach (Dataset 2) shows more robust performance
- Automated generation using large models is possible but with varying degrees of reliability

You can find our finetuned model [here](https://huggingface.co/axel-darmouni/paligemma_dataset2)

## Next Steps
- Expand the dataset to cover more web-based tasks
- Improve automation in the dataset creation pipeline
- Enhance model performance on complex web navigation scenarios
- Scale the approach to different websites and use cases

## Contributing
We welcome contributions to improve the dataset creation pipeline and model performance. Please see our contribution guidelines for more information.

## License
Project is MIT Licensed.

## Contact
Contact Axel Darmouni, Anas Lecaillon, or Paul Peytevin for more details if needed.

## Acknowledgments
- H Runner team for proving the concept of edge intelligence
- Microsoft for OmniParser
- [Add other acknowledgments as needed]

## Setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Using Omnivision

Get the weights for the model:

```bash
./setup_omnivision.sh
```
To test it out:

```bash
cd parser
python parser.py
```
