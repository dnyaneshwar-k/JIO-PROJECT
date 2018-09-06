#import numpy as np
import os
import platform

TEST_MODE = False

# Platform Specific Setup
if platform.system() == 'Darwin':
    root_path = "/Users/pradip.gupta/JEAP/object_detection"
    database = "/Users/pradip.gupta/JEAP_database"
    # Spark for Mac
    spark_home = "/Users/pradip.gupta/spark-2.3.1-bin-hadoop2.7"
    spark_master = 'spark://LM0000258:7077'

else:
    root_path = "/home/dnyaneshwar/Pictures/object_detection/object_detection"
    database = os.path.join(root_path,"database")
    # Spark for server
    spark_home = "/home/dnyaneshwar/spark-2.3.1-bin-hadoop2.7"
    spark_master = 'spark://dnyaneshwar-HP-ProBook-440-G3:7077'   

# Spark for DK
#spark_home = "/home/dnyaneshwar/spark-2.3.1-bin-hadoop2.7"
#spark_master = 'spark://AZDEAIJEAPP01:7077'

# Input video file
video_list_path = os.path.join(database,"video_primary_list.xlsx")

if TEST_MODE: 
    modified_frames = os.path.join(database,"modified_frames_test")
    logfiles = os.path.join(database,"logfiles_test")
    model_to_use = "faster_rcnn_resnet101_coco_2018_01_28" # Detection (106, 32)
    #model_to_use = "faster_rcnn_nas_coco_2018_01_28"+stamp # Detection (1833, 43)
else:
    modified_frames = os.path.join(database,"modified_frames")
    logfiles = os.path.join(database,"logfiles")
    model_to_use = "mask_rcnn_inception_v2_coco_2018_01_28" # Detection (620, 37)   
    #model_to_use = "mask_rcnn_inception_resnet_v2_atrous_coco_2018_01_28" #Detection + Segmentation (771, 36)
    
# Model path defintions
model_folder = os.path.join(database, "model_files")
model_file = os.path.join(model_folder,model_to_use,"frozen_inference_graph.pb")

# Check if model file is present, if not download
if not os.path.exists(model_file):
    print("Required model file not found. Downloading it now: ")
    import wget
    import tarfile
    
    url = os.path.join("http://download.tensorflow.org/models/object_detection/",
                       model_to_use+".tar.gz")
    filename = wget.download(url,model_folder)
    tar = tarfile.open(filename, "r:gz")
    tar.extractall(model_folder)
    tar.close()
    os.remove(filename)
        
coco_label_map_path  = os.path.join(model_folder,"mscoco_label_map.pbtxt")
video_path = os.path.join(database,"video_library")
Object_detection_path = os.path.join(root_path,"object_detection")

# Tensorflow gpu utlisation
gpu_allocation = float(0.2)

# Global variables
NUM_CLASSES = 90

#Configurable parameters
confidence = 0.6
scene_detect_thresh = 50
frame_spacing = 10

#db settings
HOST= "127.0.0.1" #local PC
PORT = "27017"
USER = "jioaicoejeap"
PASSW = "jioaicoejeap"
DB_NAME = "videos"
COL_NAME = "urlinfo"

print("Config file loaded successfully")
