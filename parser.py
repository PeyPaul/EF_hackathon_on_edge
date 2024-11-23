import sys
sys.path.append("OmniParser")
from omniparser import Omniparser
import cv2

class Element:
    def __init__(self, x, y, w, h, text):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.text = text

def get_elements(image, ignore_nones=True):
    parsed = omniparser.parse(image)
    parsed = parsed[1]
    elements = []

    for elem in parsed:
        x, y, w, h = elem['shape']['x'], elem['shape']['y'], elem['shape']['width'], elem['shape']['height']
        text = elem['text']
        if ignore_nones and text == "None":
            continue
        elements.append(Element(x, y, w, h, text))
    return elements

def show_frame_with_elements(image, elements):
    frame = cv2.imread(image)
    for elem in elements:
        cv2.rectangle(frame, (elem.x, elem.y), (elem.x + elem.w, elem.y + elem.h), (0, 255, 0), 2)
        cv2.putText(frame, elem.text, (elem.x, elem.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame


# Initialize Omniparser with the configuration
omniparser_config = {
    'som_model_path': 'OmniParser/weights/icon_detect/best.pt',
    'device': 'cpu',
    'caption_model_path': 'OmniParser/weights/icon_caption_blip2/blip2-opt-2.7b',
    'draw_bbox_config': {
        'text_scale': 0.8,
        'text_thickness': 2,
        'text_padding': 3,
        'thickness': 3,
    },
    'BOX_TRESHOLD': 0.05
}
omniparser = Omniparser(omniparser_config)

if __name__ == "__main__":
    image = "flights_test.png"
    elements = get_elements(image)
    cv2.imshow("elements", show_frame_with_elements(image, elements))
    cv2.waitKey(0)
