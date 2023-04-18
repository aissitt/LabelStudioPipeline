# Label Studio Pipeline Walkthrough

## Environment Setup
1. In command line, navigate to the folder where your environment will reside. Here, we use "labeldemo".
2. Set up a conda environment using the following command in the command line:
```
conda create --name labeldemo
```
Activate with:
```
conda activate labeldemo
```

## Label Studio Setup
3. Install from source
```
git clone https://github.com/heartexlabs/label-studio.git
cd label-studio
# Install all package dependencies
pip install -e .
# Run database migrations
python label_studio/manage.py migrate
# Collect static files
python label_studio/manage.py collectstatic
# Start the server in development mode at http://localhost:8080
python label_studio/manage.py runserver
```
4. Navigate to http://localhost:8080/projects and login or create account.

![Screenshot of Label Studio login page.](https://github.com/aissitt/LabelStudioPipeline/blob/9b527506d1b9fad981ea17251de0443e70ceab31/LabelStudioLogin.png)

5. Create a project by clicking on the "Create" button. The project will automatically be numbered. You can rename the project, but keep track of this number for later.

![Screenshot of Label Studio project default name and number.](https://github.com/aissitt/LabelStudioPipeline/blob/e2bb1021ff0720cdef1d15325b4c46c6478946c5/LabelStudioProject.png)

6. Import the data you wish to annotate, and select the labeling format. Here we use bounding boxes and labels.

![Screenshot of Label Studio data import.](https://github.com/aissitt/LabelStudioPipeline/blob/e2bb1021ff0720cdef1d15325b4c46c6478946c5/UploadImages.png)
![Screenshot of Label Studio labeling formats.](https://github.com/aissitt/LabelStudioPipeline/blob/1386af21dc3d16034aaceb6bc5e6c096c970645c/LabelingFormat.png)

7. Annotate about 20-30 representative frames, and export these annotations in YOLO format.

![Screenshot of Label Studio sample annotation.](https://github.com/aissitt/LabelStudioPipeline/blob/1386af21dc3d16034aaceb6bc5e6c096c970645c/SampleAnnotation.png)

![Screenshot of Label Studio annotation forms.](https://github.com/aissitt/LabelStudioPipeline/blob/9b527506d1b9fad981ea17251de0443e70ceab31/AnnotationForms.png)

## YOLOv5 Setup
* Now we train a YOLOv5 backbone using Google Colab 
* The original custom training file is found here: https://colab.research.google.com/github/roboflow-ai/yolov5-custom-training-tutorial/blob/main/yolov5-custom-training.ipynb
* Changes were made to the training file to better suite our needs. The updated file can be found here: https://colab.research.google.com/drive/1mwwkymB6cs_iEBMf0MfJJ8Y1UW5NPFiM?usp=sharing
## Label Studio ML Backend Setup
