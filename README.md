# schoolbus_yolov5_take2
I'll be linking blog article tutorials to walk you through the project here when they're completed.

## Running
1. create virtual env directory `venv/` with pycharm or from the command line
   ```
    python -m venv venv
   ```
3. install everything with [install.ps1](./install.ps1)
   ```
    .\install.ps1
   ```
4. create comet artifact by running [create_comet_artifact.py](./create_comet_artifact.py)
   ```
    python create_comet_artifact.py
   ```
5. run training with  [train.ps1](./train.ps1)
   ```
    .\train.ps1
   ```
6. run detection program [detect_bus.py](./detect_bus.py):
   ```
    python detect_bus.py
   ```


## Full list of documentation
* [aws.py](./aws.py) - Utility functions that use AWS
* [camera.py](./camera.py) - Functions for connecting to the webcam
* [check_cuda.py](./check_cuda.py) - Super short file to check that CUDA is working
* [create_comet_artifact.py](./create_comet_artifact.py) - create a comet artifact from a roboflow export
* [detect_bus.py](./detect_bus.py) - the bus detector script!
* [detector.py](./detector.py) - A class for managing notifications
* [install.ps1](./install.ps1) - The initial install script for setting up dependencies
* [setup_credentials.py](./setup_credentials.py) - writes all the needed credential files for authentication with stuff
* [train.ps1](./train.ps1) - script to run yolov5 training on custom data set
* [yolov5_detect.py](./yolov5_detect.py) - my copy of the detect.py script from yolov5
