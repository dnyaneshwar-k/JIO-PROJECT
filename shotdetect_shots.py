from __future__ import division

import subprocess
import cv2
import time
import datetime
def extract_shots_with_shotdetect(video_file_path, fps,min_scene_length,threshold=60):

    print("Started shot detection....")
    start = time.time()
    
    scene_ps = subprocess.Popen(("shotdetect", 
                                "-i",
                                video_file_path,
                                "-o",
                                "output_dir",
                                "-s",
                                str(threshold)),
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
    output = scene_ps.stdout.read()
    
    scene_list,scene_list_tc = extract_boundaries_from_shotdetect_output(output,fps)
    if not scene_list:
        final_scene_list = [1,int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1]
    else:
        final_scene_list = []
        init_frame_no = 1
        for frame_no in  scene_list:
            if (frame_no-init_frame_no)>min_scene_length:
                final_scene_list.append((init_frame_no,frame_no))
                init_frame_no = frame_no
        
    print("Total time taken for shot detection is {} secs".format(round((time.time()-start),2)))
    print("--"*50)    
    return final_scene_list,scene_list_tc

def extract_boundaries_from_shotdetect_output(output,fps):
    """
    extracts the shot boundaries from the string output
    producted by shotdetect
    
    Args:
        output (string): the full output of the shotdetect
            shot detector as a single string
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    data = parse_output(output)
    scene_list_tc = []
    scene_list = []
    for i in range(0, len(data)-1,1):
        time = float(data[i].split(' :: ')[-1])/1000
        scene_list.append(int(time*fps))
        scene_list_tc.append(str(datetime.timedelta(seconds=time)))
    return scene_list,scene_list_tc

def parse_output(output):
    """
    slices the output of the shotdetector to retrieve
    the relevant data
    
    Args:
        output (string): the full output of the shotdetect
            shot detector as a single string
    
    Returns: 
        List[string]: a list of strings containing the data
        held as part of the ouput string"""
    data = output.decode().split('\n')

    for i in range(2,len(data)):
        if 'Shot log' in data[i]:
            return data[i:]
    return None
