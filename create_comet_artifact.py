"""
Download an exported dataset from Roboflow, and create a Comet data artifact with the files.

"""
from roboflow import Roboflow
from glob import glob
from comet_ml import Artifact, Experiment
import yaml
import os
import shutil

# These are all the "configuration parameters" to set before running this script
roboflow_workspace = "kristen-kehrer"
roboflow_project = "schoolbus-images"
roboflow_version = 4
staging_directory = f"Schoolbus-Images-{roboflow_version}"
roboflow_api_key_file = '.roboflow_api_key'
comet_artifact_name = 'schoolbus-yolov5-take2'


def download_roboflow_artifact():
    # Delete the staging directory if it already exists
    if os.path.exists(staging_directory):
        shutil.rmtree(staging_directory)

    if not os.path.exists(roboflow_api_key_file):
        raise f'Missing configuration file: {roboflow_api_key_file}'

    # Load api key from saved credential file and strip whitespace characters from the ends
    roboflow_api_key = open(roboflow_api_key_file).read().strip()

    # With the Roboflow python SDK, download the desired dataset.
    # After `.download("yolov5")` completes, the full data artifact will
    # be on the local filesystem at `staging_directory`
    rf = Roboflow(api_key=roboflow_api_key)
    project = rf.workspace(roboflow_workspace).project(roboflow_project)
    dataset = project.version(roboflow_version).download("yolov5")


def create_comet_artifact():
    # Start a comet experiment (project name / api key are already set in `.comet.config`)
    experiment = Experiment()

    # Load the `data.yaml` file (this is how data needs to be formatted for YOLOv5) from the Roboflow artifact
    metadata = yaml.load(open(os.path.join(staging_directory, 'data.yaml')), Loader=yaml.Loader)

    # Convert the `names` field in the metadata from a list of strings to an integer-keyed dictionary
    # of strings  (`['bus', 'car']` needs to be `{ '0': 'bus', '1': 'car'}` for the comet metadata
    # I created a PR to add this to the yolov5 library, I'll remove this once it's merged.
    names_dict = {}
    for i in range(len(metadata['names'])):
        names_dict[str(i)] = metadata['names'][i]
    metadata['names'] = names_dict

    # Create the comet Artifact object
    artifact = Artifact(name=comet_artifact_name, artifact_type="dataset", metadata=metadata)

    # Iterate through all files in `staging_directory`, and add the file to the artifact
    for file in glob(f'{staging_directory}/**/*.*', recursive=True):
        artifact.add(file, logical_path=file.replace('\\', '/'))

    # Log the artifact and end the experiment
    experiment.log_artifact(artifact)
    experiment.end()


def write_yolov5_data_file():
    with open('comet_artifact.yaml', 'w') as file:
        file.write(f'path: comet://kristenkehrer/{comet_artifact_name}:latest"\n')


# When this script is run, run these two functions:
download_roboflow_artifact()
#create_comet_artifact()
#write_yolov5_data_file()
