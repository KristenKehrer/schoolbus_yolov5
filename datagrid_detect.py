from yolov5_detect import detect
import os
import comet_ml

nano_weights_experiment = 'kristenkehrer/schoolbus-yolov5-take2/95731b2edc3c4944bc9282b60f5c008c'
small_weights_experiment = 'kristenkehrer/schoolbus-yolov5-take2/c935d75f6f0e40f0a085e0860613c2fa'


def load_model():
    """Download `best.pt` weights file from comet experiemnt"""
    # Set the COMET_EXPERIMENT_KEY to match the latest experiment from running .\train.ps1
    comet_experiment_key = small_weights_experiment
    model_path = 'schoolbus_weights_nano.pt'
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


detect(
    imgsz=(640, 640),
    weights='schoolbus_weights.pt',
    device=0,
    # Have yolov5 save video file of detection run in `yolov5/runs/detection/expX/`
    nosave=False,
    view_img=False,
    # Use the webcam URL as the source for detection
    source='Schoolbus-Images-4/valid/images',
    enable_data_grid=True
)
