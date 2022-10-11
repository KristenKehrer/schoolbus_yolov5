# Run training using a custom dataset in Comet

# Verbose logging on for yolov5
$env:YOLOv5_VERBOSE = "true"

# Include "per-class" metrics in comet logging
$env:COMET_LOG_PER_CLASS_METRICS = "true"

# Log predictions, which I think this does as a default anyways....
$env:COMET_LOG_PREDICTIONS = "true"

# Reduce the number image uploads, as the dataset artifact is already in comet.
# I'm hoping this avoids the "ResponseError('too many 502 error responses')" issue when uploading comet files.
$env:COMET_MAX_IMAGE_UPLOADS = 20

# Calling `train.py` from the yolov5 repo
python .\yolov5\train.py `
    <# This yaml file points to comet://kristenkehrer/schoolbus-yolov5-take2:latest #> `
    --data comet_artifact.yaml `
    <# Starting weights #> `
    --weights yolov5s.pt `
    <# image size in pixels #> `
    --img 640 `
    <# number of epochs #> `
    --epochs 150 `
    <# 0 refers to "first CUDA GPU device" #> `
    --device 0 `
    --save-period 150

