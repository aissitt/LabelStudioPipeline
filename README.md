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
![Screenshot of Label Studio login page.](https://github.com/aissitt/LabelStudioPipeline/blob/79d8b3d390e63f698ab631f3fba588bdbd501817/LabelStudioLogin.png)
5. Create a project by clicking on the "Create" button. The project will automatically be numbered. You can rename the project, but keep track of this number for later.
6. Import the data you wish to annotate, and select the labeling format. Here we use bounding boxes and labels.
7. Annotate about 20-30 representative frames, and export these annotations in YOLO format.

## YOLOv5 Setup
## Label Studio ML Backend Setup
