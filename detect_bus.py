"""
This is the bus detector script.  Run it with `python detect_bus.py` in order to
start watching the webcam and notifying users whenever a "schoolbus" is detected
"""
import os
os.environ['YOLOv5_VERBOSE'] = 'false'

from yolov5_detect import detect
from camera import get_rtsp_url
import comet_ml
from detector import Detector
from aws import test_aws_access


# Making sure that I'm using the best model from all of my training runs and downloading it from Comet.  
# The experiment key needs to be manually updated.
# Returns the path of model file
def load_model():
    """Download `best.pt` weights file from comet experiment"""
    # Set the COMET_EXPERIMENT_KEY to match the latest experiment from running .\train.ps1
    comet_experiment_key = 'kristenkehrer/schoolbus-yolov5-take2/c935d75f6f0e40f0a085e0860613c2fa'
    model_path = 'schoolbus_weights.pt'
    print(f'downloading {model_path} from comet experiment {comet_experiment_key}...')

    # Remove the existing weights file if there is one
    if os.path.exists(model_path):
        os.remove(model_path)

    # Use the comet `APIExperiment` in order to get access to the asset list.
    api = comet_ml.api.API()
    exp = api.get(comet_experiment_key)

    # Retrieve all assets, then find the one named `best.pt`
    assets = exp.get_asset_list(asset_type='model-element')
    model = next(filter(lambda a: a['fileName'] == 'best.pt', assets), None)
    file = exp.get_asset(model['assetId'])

    # Save the model file locally and return the local filepath for use in the detect script
    open(model_path, 'wb').write(file)
    print(f'model download complete.  File saved to {model_path}')
    return model_path


def run_detection():
    # Before getting started, make sure aws credentials are set up correctly
    if not test_aws_access():
        raise "Cannot access AWS!"

    # Instantiate a new object of type `Detector`
    detector = Detector()

    # Run yolov5 detection!
    detect(
        # The size of our images in pixels
        imgsz=(640, 640),
        # The weights file, downloaded by `load_model()`
        weights=load_model(),
        # This refers to the 'first CUDA device', and will be the GPU in a single GPU system
        device=0,
        # We use a lambda to pass the `**kwargs` from the `on_objects_detected` function
        # to the `detector.objects_detected` function
        on_objects_detected=lambda **kwargs: detector.objects_detected(**kwargs),
        # Have yolov5 save video file of detection run in `yolov5/runs/detection/expX/`
        nosave=True,
        # Use the webcam URL as the source for detection
        source=get_rtsp_url()
    )


# When this script is run, start with run_detection()
run_detection()
