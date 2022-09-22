# Run training using a custom dataset in Comet

# Verbose logging on for yolov5
$env:YOLOv5_VERBOSE = "true"

# Include "per-class" metrics in comet logging
$env:COMET_LOG_PER_CLASS_METRICS = "true"

# Log predictions, which I think this does as a default anyways....
$env:COMET_LOG_PREDICTIONS = "true"


# Calling `train.py` from the yolov5 repo
python .\yolov5\train.py `
    <# This yaml file points to comet://kristenkehrer/schoolbus-yolov5-take2:latest #> `
    --data comet_artifact.yaml `
    <# Starting weights #> `
    --weights yolov5s.pt `
    <# image size in pixels #> `
    --img 640 `
    <# number of epochs #> `
    --epochs 5 `
    <# 0 refers to "first CUDA GPU device" #> `
    --device 0 `
    <# Save model file to Comet every X epochs #> `
    --save-period 5
