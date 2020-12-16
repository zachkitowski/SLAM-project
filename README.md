# Investigating Monocular SLAM Algorithms
### Camera Calibration 
Run the command
```bash
calibrate.py cam1v2  
```
cam1v2: Folder where images for calibration go 

### Video to image 
Run the command 

```bash
Videotofile.py cam1v2.mov cam1v2 
```

### Make Timestamp Text File
Edit the folder name within this file to map to the folder with all of the images and the output text file name. 
Run the command 

```bash
make_image_list.py 
```

### DSO
1. Build DSO, full instructions can be found here: https://github.com/JakobEngel/dso
2. Run the command
```bash
bin/dso_dataset files=[path_to_images_folder] calib=[path_to_camera_calibration] preset=0 mode=1
```

### ORB-SLAM3
1. Install all the required packages and build ORB-SLAM3, full instructions can be found here: https://github.com/UZ-SLAMLab/ORB_SLAM3
2. Run the command  
```bash
./Examples/Monocular/mono_euroc ./Vocabulary/ORBvoc.txt ./Examples/Monocular/the_calibration_file the_dataset_file ./Examples/Monocular/EuRoC_TimeStamps/the_timestamp_file  
```
the_dataset_file: where you put the dataset  
the_calibraiton_file: JM_Cam1/2/3_calibration.yaml  
the_timestamp_file: depends on which videos you run

### ORB-SLAM2
1. Install all the required packages and build ORB-SLAM2, full instructions can be found here: https://github.com/raulmur/ORB_SLAM2
2. Run the command  
```bash
./Examples/Monocular/mono_euroc /home/zach/ORB_SLAM2/Vocabulary/ORBvoc.txt /home/zach/dev_code/JM_Calibration/JM.yaml /home/zach/dev_code/JM_Video /home/zach/dev_code/JM_01.txt
```

### DynaSLAM
1. Install all the required packages and build DynaSLAM, full instructions can be found here: https://github.com/BertaBescos/DynaSLAM
2. Run the command  
```bash
./Examples/Monocular/mono_tum /home/zach/DynaSLAM/Vocabulary/ORBvoc.txt /home/zach/dev_code/JM_Videos/JM_cam3.yaml /home/zach/dev_code/JM_Videos/cam3_figure8 /home/zach/dev_code/JM_Videos/cam3_figure8.txt
```
