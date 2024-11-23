#!/bin/bash

git lfs install
cd omniparser_weights
echo "Downloading OmniParser model..."
if [ ! -d "OmniParser" ]; then
    git clone https://huggingface.co/microsoft/OmniParser
fi
echo "Converting model to PyTorch..."
if [ ! -z "$(ls -A OmniParser/icon_*)" ]; then
    cp -r OmniParser/icon_* ../OmniParser/weights/
fi
cd ../OmniParser
python weights/convert_safetensor_to_pt.py
echo "Done!"