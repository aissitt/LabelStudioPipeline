from label_studio_ml.model import LabelStudioMLBase
import torch
from PIL import Image
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_image_size, get_single_tag_keys, is_skipped
from label_studio.core.utils.io import json_load, get_data_dir 
from label_studio.core.settings.base import DATA_UNDEFINED_NAME
from urllib.parse import urlparse
import os
import numpy as np
from tqdm import tqdm
import time
from label_studio.core.utils.io import get_data_dir

LABEL_STUDIO_HOST = os.getenv('LABEL_STUDIO_HOST', 'http://localhost:8082')
LABEL_STUDIO_API_KEY = os.getenv('LABEL_STUDIO_API_KEY', '1ae8c0130f0c2555ffb913391a5398bdacaf5890')

# Needs called outside of __init__ - otherwise the model reloads on every call to predict 
# Slack issue is open to label studio development team about this (10/18/2022)
MODEL = torch.hub.load('PATH_TO_YOLOv5_DIR', 
                        'custom', 
                        path='PATH_TO_best.pt', 
                        source="local", 
                        force_reload=True)  

class YoloV5(LabelStudioMLBase):
    def __init__(self, config_file=None,
                 yolo_directory='PATH_TO_YOLOv5_DIR',
                 checkpoint_file='PATH_TO_best.pt',
                 base_dir="",
                 labels_file=None, score_threshold=0.3, device='cuda', **kwargs):

        # don't forget to initialize base class...
        super(YoloV5, self).__init__(**kwargs)
        
        # Load the model 
        self.model = MODEL
        self.model.eval().to("cuda")
        
        upload_dir = 'PATH_TO_LABEL_STUDIO_MEDIA_UPLOADS'
        # Usually here: 'C:\\Users\\AppData\\Local\\label-studio\\label-studio\\media\\upload\\#\\'

        self.image_dir = upload_dir

        self.score_thresh = score_threshold
        
        # print("DATA DIR HERE")
        # print(get_data_dir())

        # print(os.getcwd())

        #create a label map
        self.predicted_label_map = {}

        self.model_label_map = {'LABEL_MAP_HERE'}
        # In the form: {0:"diver", 1:"diver_partial", 2:"diver_reflection"}

        self.from_name, self.to_name, self.value, self.labels_in_config = get_single_tag_keys(
            self.parsed_label_config, 'RectangleLabels', 'Image'
        )
       
        self.base_dir = base_dir
        schema = list(self.parsed_label_config.values())[0]
        self.labels_in_config = set(self.labels_in_config)

        self.label_attrs = schema.get('labels_attrs')
        print(self.label_attrs)
        if self.label_attrs:
            for label_name, label_attrs in self.label_attrs.items():
                for predicted_value in label_attrs.get('predicted_values', '').split(','):
                    self.predicted_label_map[predicted_value] = label_name

    def get_image_url(self, task):
        image_url = task['data'][self.value] 

        image_url_base, image_url_filename = os.path.split(image_url)
        
        image_url = self.image_dir + image_url_filename
        return image_url
    
    
    def predict(self, tasks, **kwargs):
        """_summary_

        Args:
            tasks (_type_): a list of tasks 
        """

        # Get annotation tag first, and extract from_name/to_name keys from the labeling config to make predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        to_name = schema['to_name'][0]
        
        results = []

        for task in tqdm(tasks): 
            print(task)
            
            start_task_time = time.time()

            # Get the path to the image 
            image_url = self.get_image_url(task)

            print(f"Processing: {image_url}")

            # Load the image data 
            img = Image.open(image_url)

            # Get the size of the image 
            img_width, img_height = get_image_size(image_url)

            # Run inference using the initialized model (with data on the GPU)
            dets = self.model(img)

            for det in dets.xyxy[0]:
                # x and y are the upper left corner and width and height are the width and height of the box 
                if det.size(axis=0) != 0: 
                    x_min = float(det[0].detach().cpu().numpy())
                    y_min = float(det[1].detach().cpu().numpy())
                    x_max = float(det[2].detach().cpu().numpy())
                    y_max = float(det[3].detach().cpu().numpy())
                    confidence = float(det[4].detach().cpu().numpy())
                    predicted_class = int(det[5].detach().cpu().numpy())
                    print(predicted_class)
                    print(self.model_label_map[predicted_class])
                    print(self.predicted_label_map)
                    predicted_label = self.predicted_label_map[self.model_label_map[predicted_class]]

                    print(predicted_class)
                    
                    task_time = time.time() - start_task_time

                    if confidence >= self.score_thresh: 
                        result = {
                                'from_name': from_name,
                                'to_name': to_name,
                                "original_width": img_width,
                                "original_height": img_height,
                                'type': 'rectanglelabels',
                                'value': {
                                    'rectanglelabels': [predicted_label],
                                    'x': x_min / img_width * 100,
                                    'y': y_min / img_height * 100,
                                    'width': (x_max - x_min) / img_width * 100,
                                    'height': (y_max - y_min) / img_height * 100
                                },
                                'score': confidence
                            }

                        results.append(result)

                        print(f"Model Outputs: {x_min} {y_min} {x_max} {y_max} {confidence} {predicted_label}")
                        print(f"Label Studio Receives: {from_name} {to_name} {img_width} {img_height} {predicted_label} {confidence} {task_time}")
                        print(f"Time Taken (s): {task_time}")
                    else: 
                        print(f"Model Outputs: {x_min} {y_min} {x_max} {y_max} {confidence} {predicted_label}")
                        print(f"Label Studio Receives: Nothing; Confidence Lower than Score Threshold {self.score_thresh}")
                        print(f"Time Taken (s): {task_time}")

                else: 
                    task_time = time.time() - start_task_time

                    print(f"Model Outputs: No Detections")
                    print("Label Studio Receives: Empty List")
                    print(f"Time Taken (s): {task_time}")

        return [{
        'result': results
        }]

    def fit(self, completions, workdir=None, **kwargs):
        return {}
