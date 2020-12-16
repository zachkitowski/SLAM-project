# SLAM-project
DSO:

    ```bash
    bin/dso_dataset files=[path_to_images_folder] calib=[path_to_camera_calibration] preset=0 mode=1
    ```

ORB-SLAM3  
1. Install all the required packages and build ORB-SLAM3  
2. Run the command  
    ```bash
    ./Examples/Monocular/mono_euroc ./Vocabulary/ORBvoc.txt ./Examples/Monocular/the_calibration_file 
    the_dataset_file ./Examples/Monocular/EuRoC_TimeStamps/the_timestamp_file  
    ```
    the_dataset_file: where you put the dataset  
    the_calibraiton_file: JM_Cam1/2/3_calibration.yaml  
    the_timestamp_file: depends on which videos you run
