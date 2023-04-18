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

![Screenshot of Label Studio login page.](/images/LabelStudioLogin.png)

3. Create a project by clicking on the "Create" button. The project will automatically be numbered. You can rename the project, but keep track of this number for later.

![Screenshot of Label Studio project default name and number.](/images/LabelStudioProject.png)

4. Import the data you wish to annotate, and select the labeling format. Here we use bounding boxes and labels.

![Screenshot of Label Studio data import.](/images/UploadImages.png)
![Screenshot of Label Studio labeling formats.](/images/LabelingFormat.png)

5. Annotate about 20-30 representative frames, and export these annotations in YOLO format. In this case, we have annotated frames with three classes: boat, boat_partial, and boat_reflection.

![Screenshot of Label Studio sample annotation.](/images/SampleAnnotation.png)

![Screenshot of Label Studio annotation forms.](/images/AnnotationForms.png)

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
3. Create a folder under "labeldemo" with the name of your model, in this case "boat", and place the best.pt inside.
4. Install the appropriate PyTorch version from https://pytorch.org/get-started/locally/ (torchaudio not needed):
![Screenshot of PyTorch downloads.](/images/PyTorchVersions.png)
5. Clone the Label Studio Machine Learning Backend git repository:
```
git clone https://github.com/heartexlabs/label-studio-ml-backend
```
6. Set up the environment:
```
cd label-studio-ml-backend

# Install label-studio-ml and its dependencies
pip install -U -e .

# Install the dependencies for the example or your custom ML backend
pip install -r path/to/my_ml_backend/requirements.txt
```
7. Prepare ml.py. Fill in the capitialized fields with paths on your local machine.
8. In file explorer, navigate to label-studio/label-studio-ml-backend/label_studio_ml/examples. Create a folder under "examples" with your desired name, here we use "boat". Place ml.py inside this folder.
9. Back in command line, run the following (or substitute your model name for "boat" here):
    ```
    label-studio-ml init boat --script label_studio_ml/examples/boat/ml.py
    ```

      1. If this command fails due to missing dependancies, install them, then continue to 9-ii below.
      2. If this command fails due to this error message:
      ![Screenshot of error message.](/images/ErrorMessage.png)
      A new folder has populated with the name of your model, likely in label-studio/label-studio-ml-backend. Delete this folder, then run command again.
      3. If this command executes successfully, you will receive a message like this:
      ![Screenshot of success message for backend setup.](/images/BackendSuccess.png)
10. Start your backend:
```
label-studio-ml start .\boat
```
Take note of the url at the bottom:
![Screenshot of backend details.](/images/BackendRunning.png)
This will be used to configure our backend in Label Studio.

11. Navigate to the settings page for your Label Studio project. 

12. Select the "Machine Learning" tab, then select "Add Model".
    1. Enter your model name, the url obtained earlier, and a description.
    2. Activate the slider to enable interactive preannotations. 
    ![Screenshot of ML backend setup in Label Studio.](/images/mlSettings.png)
    3. Select "validate and Save".

13. Activate sliders for ML-Assisted Labeling:

![Screenshot of ML backend labeling settings.](/images/AssistedLabeling.png)

