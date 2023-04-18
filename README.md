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
1. Install from source as seen here https://labelstud.io/guide/install.html#Install-from-source:
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
2. Navigate to http://localhost:8080/projects and login or create account.

![Screenshot of Label Studio login page.](/LabelStudioLogin.png)

3. Create a project by clicking on the "Create" button. The project will automatically be numbered. You can rename the project, but keep track of this number for later.

![Screenshot of Label Studio project default name and number.](/LabelStudioProject.png)

4. Import the data you wish to annotate, and select the labeling format. Here we use bounding boxes and labels.

![Screenshot of Label Studio data import.](/UploadImages.png)
![Screenshot of Label Studio labeling formats.](/LabelingFormat.png)

5. Annotate about 20-30 representative frames, and export these annotations in YOLO format. In this case, we have annotated frames with three classes: boat, boat_partial, and boat_reflection.

![Screenshot of Label Studio sample annotation.](/SampleAnnotation.png)

![Screenshot of Label Studio annotation forms.](/AnnotationForms.png)

## YOLOv5 Setup
* Now we train a YOLOv5 backbone using Google Colab 
* The original custom training file, YOLOv5-Custom-Training.ipynb, is found here: https://colab.research.google.com/github/roboflow-ai/yolov5-custom-training-tutorial/blob/main/yolov5-custom-training.ipynb
* Changes were made to the training file to better suite our needs. The updated file, YOLOv5-Custom-Backbone-Training.ipynb, can be found here: https://colab.research.google.com/drive/1mwwkymB6cs_iEBMf0MfJJ8Y1UW5NPFiM?usp=sharing

### Prepare Dataset
1. Using split.ipynb, define your desired ratios and split the annotations into test, train, and validation folders. Ratios are defined here:
```
# Split with a ratio
# Group prefix is 2 to capture image and annotation files for each
splitfolders.ratio(input_folder, output=output_folder,
    seed=1337, ratio=(.8, .1, .1), group_prefix=2, move=False)
```
2. Upload dataset to Google Drive. Here, we place it in a folder named "dataset".
3. Next, data.yaml needs to be configured. 
    1. In the "train" field, enter the path to the "train" folder in your Drive. Insert corresponding paths for the "val" and "test" fields as well. 
    2. Now, change the "nc" field to the number of classes you plan to train on. In this case, we have three.
    3. Finally, enter each class name in the "names" field.
    4. Place data.yaml in the same directory as your dataset.
4. Change any paths in YOLOv5-Custom-Backbone-Training.ipynb if you have used different folder names/paths. Set your desired number of epochs here:
```
!python train.py --img 416 --batch 16 --epochs 500 --data /content/drive/MyDrive/dataset/data.yaml --weights yolov5s.pt --cache
```
5. Run all cells in the file, and keep track of best.pt when it downloads.

## Label Studio ML Backend Setup
1. In a new command terminal, navigate to your environment directory, here we're using "labeldemo" and activate the environnment.
2. Clone the YOLOv5 repository:
```
git clone https://github.com/ultralytics/yolov5/
```
3. Install the appropriate PyTorch version from https://pytorch.org/get-started/locally/ (torchaudio not needed):
![Screenshot of PyTorch downloads.](/PyTorchVersions.png)
5. Clone the Label Studio Machine Learning Backend git repository:
```
git clone https://github.com/heartexlabs/label-studio-ml-backend
```
5. Set up the environment:
```
cd label-studio-ml-backend

# Install label-studio-ml and its dependencies
pip install -U -e .

# Install the dependencies for the example or your custom ML backend
pip install -r path/to/my_ml_backend/requirements.txt
```

## Integrate with Label-Studio
*label map
