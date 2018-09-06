# Import List
#To supress warnings
import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

import warnings
if not sys.warnoptions:
   warnings.simplefilter("ignore") 

# Standard lib imports
import numpy as np
import imageio
import time
import pandas as pd
import tensorflow as tf
from functools import partial
import pickle

# Custom file imports
sys.path.append("..")
import config
import scenewise_pb2
from model import category_index

from file_download import file_download
from shotdetect_shots import extract_shots_with_shotdetect
#from extract_shots_with_pyscenedetect import extract_shots_with_pyscenedetect
from check_validity import check_validity
from utility import visualize_and_save


class Spark_Video_Detector():

    def __init__(self, confidence=0.6):
        self.confidence = confidence
        self.start_time = time.time()
    
    def frame_processing(self,frame_no,video_file_path_bc,graph_def_bc):   
        
        from model import ObjectDetector
        
        videogen = imageio.get_reader(video_file_path_bc.value,'ffmpeg')
        frame_img = videogen.get_data(frame_no)

        #Processing frame wise
        output_dict =ObjectDetector().detect(frame_img,frame_no,graph_def_bc.value) 
            
        return  output_dict         

    def detect(self, video_file_path, proto_name,sc):
        
        #adding files to workers
        sc.addFile('config.py')
        sc.addPyFile('model.py')
        
        sc.addPyFile('utility.py')
        sc.addPyFile('scenewise_pb2.py')
        sc.addPyFile('check_validity.py')
        sc.addPyFile('shotdetect_shots.py')
        sc.addPyFile('file_download.py')


        #check validity
        num_frames = check_validity(video_file_path)
        
        # Load the video frame by frame
        videogen = imageio.get_reader(video_file_path,'ffmpeg')
        fps = videogen.get_meta_data()['fps'] #fps to be used to decide min scene length
        
        # Create a folder to store frames of the modified video
        mod_folder, _ = proto_name.split(".")
        modified_frames_path = os.path.join(config.modified_frames, mod_folder)
        if not os.path.exists(modified_frames_path):
            os.mkdir(modified_frames_path)  
        
        
        # Scene detection algorithm
        scene_list, scene_list_tc = extract_shots_with_shotdetect(
                video_file_path, fps,fps,threshold = config.scene_detect_thresh)

        # Variable initialise
        sno = 1
        start_frame=0
        frames_scanned = 0
        t = 0
        method='wb' #Open bytes file in write mode
        
        # Load Frozen Network Model
        print("Loading forzen graph into memory...")
        t1 = time.time()
        with tf.gfile.FastGFile(config.model_file,'rb') as f:
            model_pb = f.read()
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(model_pb)
        graph_def_bc = sc.broadcast(graph_def)
        print("Model file loaded and broadcasted in {} secs".format(round((time.time()-t1),2)))
        
        # Broadcasted varibales
        object_detection_path = config.Object_detection_path
        object_detection_path = sc.broadcast(object_detection_path)
        num_frames = sc.broadcast([num_frames])
        video_file_path_bc = sc.broadcast(video_file_path)
        
        # Proto file initialisation
        proto_path = os.path.join(config.logfiles, proto_name)
        
        
        for k in scene_list[1:3]: #This for loop will run once for each scene
            
            frame_list = np.linspace(start_frame,k[0],
                                     int((k[0]-start_frame)/config.frame_spacing))
            frame_list = frame_list.astype(int)
            
            print("--"*50)            
            print("No of frames in Scene {} are {}".format(sno,
                                                            len(frame_list)))
            print("The frames are listed as {}".format(frame_list))
                                    
            start_frame = k[0]+1

            frame_list = frame_list[:2]
            frame_list_rdd = sc.parallelize(frame_list, 4)
            
            t1=time.time()

            output_dict_rdd = frame_list_rdd.map(partial(self.frame_processing,
                                        video_file_path_bc=video_file_path_bc,
                                        graph_def_bc = graph_def_bc)).collect()
            t2=time.time()
            delta = t2 - t1
            t = t + delta
            
            frames_scanned = frames_scanned + len(frame_list)
            
            # Proto add for scene-level info
            scene_list_pb = scenewise_pb2.Scene_list()
            scene = scene_list_pb.scenes.add()
            scene.video_id = video_file_path
            scene.s_no = sno
            scene.str_time = scene_list_tc[sno-1]
            scene.stop_time =  scene_list_tc[sno]            
            
            #print(type(scenelist))
            #print(getsizeof(output_dict_rdd))
            print("Objects found in scene no {} are:".format(sno))
            
            for frame_no in frame_list: # this loop will run once for each frame
                
                frame = scene.frames.add()
                frame.frameno = frame_no
                
                frame_img = videogen.get_data(frame_no)
                idx = [i for i,_ in enumerate(output_dict_rdd) if _['frame_no'] == frame_no][0]
                indices=np.where(output_dict_rdd[idx]["detection_scores"]>self.confidence)
                
                if (len(indices) > 0):
                    confidence=output_dict_rdd[idx]["detection_scores"][indices]
                    classes=output_dict_rdd[idx]["detection_classes"][indices]
                    box_io=output_dict_rdd[idx]["detection_boxes"][indices]
                    
                    if "detection_masks" in output_dict_rdd[idx]:
                        instance_masks=output_dict_rdd[idx]['detection_masks'][indices]
                    else:
                        instance_masks=output_dict_rdd[idx].get("detection_masks")
                        
                    saved_im_path = visualize_and_save(frame_img,confidence,
                                                       classes, box_io, instance_masks,
                                                       modified_frames_path, frame_no)
                    
                    #print("Objects Found are:")
                    for confidence, classes, box_io in zip(confidence,classes,box_io):                          
                            
                        obj = frame.objs.add()
                        obj.class_name = category_index[classes]['name'] 
                        obj.conf = confidence
                        obj.bbox = str([box_io])
                                               
                        print(category_index[classes]['name'],end=",")
                        
            print("\nWriting scene no {} to proto file".format(sno))
            with open(proto_path,method) as f:
                f.write(scene_list_pb.SerializeToString())
                f.close()
            
                
            method='ab' # change method to append mode
                        
            sno = sno + 1
            output_dict_rdd[:]=[]
        
        #proto_url = s3_file_upload(proto_path,proto_name)
        total_time = round((time.time()-self.start_time),2)
        print("--"*50)
        print("Total Execution time for {} is {}".format(video_file_path ,
                                                                total_time))
        
        print("Scanned {} frames in {} secs".format(frames_scanned, round(t,2)))
        print("Processing speed per frame is {}".format(t/frames_scanned))
        print("Model file used is {}".format(os.path.basename(config.model_to_use)))
            
        return proto_path
    
    def video_detector(self, video_url,sc):
        
        video_id, proto_name,self.video_title = file_download(video_url)
        proto_url = self.detect(video_id,proto_name,sc)
        
        return proto_url    


if __name__ == "__main__":
    
    from sparkSetup import start_spark, get_spark_context, stop_spark
    
    start_spark()
    
    #import findspark
    #findspark.init(config.spark_home)
    #from pyspark import SparkContext, SparkConf
        
    #start_spark()
    #conf = SparkConf().setAppName('ObjectDetection').setMaster(config.spark_master)
    #sc = SparkContext(conf=conf)
    
    sc = get_spark_context()    
    svd = Spark_Video_Detector()

    
    # with open('scene_list_file.dat','rb') as rpf:

    #     while True:
    #         try:
    #             video_details = pickle.load(rpf)
    #             #video_details.append(pickle.load(rpf))
    #             for key in video_details:
    #                 video_url = key
    #             video_file_path = video_details[video_url][0]
    #             scene_list = video_details[video_url][1]
    #             scene_list_tc = video_details[video_url][2]
    #             proto_name = video_details[video_url][3]
    #             print("Processing {} as the input video url".format(video_url))
    #             proto_url = svd.detect(video_file_path,proto_name,sc,scene_list,scene_list_tc)
    #             print("Url for the final proto file is {}".format(proto_url))
    #         except RuntimeError as err:
    #             print("Error in processing video list -> {}".format(err))                
            
    #         except EOFError:
    #             break

    #         finally:   
    #             print("Shutting down spark context and spark session")
    #             sc.stop()       
    #             stop_spark()


    df = pd.read_excel(config.video_list_path)
    video_list = df["links"]
    video_list = video_list[2:5]    
    
    try: 
        for video_url in video_list:
      
            print("***"*80)        
            print("Processing {} as the input video url".format(video_url))
            proto_url = svd.video_detector(video_url,sc) 
            print("Url for the final proto file is {}".format(proto_url))
            
    except RuntimeError as err:
        
        print("Error in processing video list -> {}".format(err))
        
    finally:   
        print("Shutting down spark context and spark session")
        sc.stop()       
        stop_spark()

    #stop_spark()

    # UrbanClap ad
    #video_url = 'https://www.youtube.com/watch?v=h4xxeZCR-kI'
    
