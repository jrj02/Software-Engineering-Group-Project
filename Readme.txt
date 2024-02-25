install PyQt5
//pip install pyqt5

install pyinstaller
//pip install pyinstaller

**restart VScode if necessary**

//try to run the code from VScode using the sample videos from:
https://numcmy-my.sharepoint.com/personal/kcztm_nottingham_edu_my/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fkcztm_nottingham_edu_my%2FDocuments%2FUNMC-Current%2FResearch%2FDatasets%2FUSM-UNM-Nadine&ct=1698655164412&or=Teams-HL&ga=1

if there are no errors, and the app runs just fine, then there is no need to do the following steps//


install a codec (if the app cannot run)
go to codecguide.com on Chrome -> go to download under K-Lite Codec and download
the "Standard" pack

run the standard pack etc


********************** to run the run_detector.py file (for windows) **********************************************

Firstly, install mambaforge:
link: https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Windows-x86_64.exe

Next, update to the latest nvidia graphics driver if necessary:

Make sure to have git installed in your computer as well.

Install the megadetector model, MDv5a. Make sure to save this file in the directory c:\megadetector
link: https://github.com/agentmorris/MegaDetector/releases/download/v5.0/md_v5a.0.0.pt

Now that everything is installed, run the mambaforge prompt. To search it, input miniforge in your computer search
and "miniforge prompt" should appear (they are the same thing).

In the prompt, add these lines below:
--------------------------------------------------------
mkdir c:\git
cd c:\git
git clone https://github.com/agentmorris/MegaDetector
git clone https://github.com/ecologize/yolov5/
cd c:\git\MegaDetector
mamba env create --file envs\environment-detector.yml
mamba activate cameratraps-detector
set PYTHONPATH=c:\git\MegaDetector;c:\git\yolov5
---------------------------------------------------------

The miniforge will start installing some files.

After it is done, the environment should change from (base) to (cameratraps_detector)

Now, copy these lines:
----------------------------------------------------------
cd c:\git\MegaDetector
mamba activate cameratraps-detector
set PYTHONPATH=c:\git\MegaDetector;c:\git\yolov5
----------------------------------------------------------

Make sure to have the run_detector.py file in your computer

With this, just inlcude this line into the mambaforge prompt:
------------------------------------------------------------------------------------------------
python detection\run_detector.py MDV5A --image_file "some_image_file.jpg" --threshold 0.1
------------------------------------------------------------------------------------------------
Replacing some_image_file.jpg with the FULL path file of the image you are detecting.

