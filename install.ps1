# Script to initially populate all dependencies.

Write-Host "* Installing pip dependencies..."
# make sure to activate virtual environment
./venv/scripts/activate.ps1
if(!$?) {
    Write-Host "ERROR: Don't forget to setup virtual environment with: python -m venv venv"
    Exit
}

# upgrade pip
pip install --upgrade pip
# install all dependencies
pip install -r requirements.txt


Write-Host "* Configuring credential files..."
# This is for entering your super secret passwords
python setup_credentials.py


Write-Host "* Checking out yolov5 repository..."
# Remove `yolov5/` directory if it exists 
Remove-Item yolov5 -Recurse -Force -ErrorAction SilentlyContinue
# Clone the repo
git clone https://github.com/ultralytics/yolov5
cd yolov5
# Always check out the same version of the repository to avoid future yolov5 changes messing me up
git checkout 959a4665f820362c95f7435dc05175deeff19671
cd ..
