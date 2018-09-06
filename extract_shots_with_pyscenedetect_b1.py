import scenedetect
import os,sys
import time
import pandas as pd
from file_download import file_download
import config
import imageio
import pickle
#import logging
#logger = logging.getLogger('object_detection')
#logger.setLevel(logging.INFO)

null = open(os.devnull, 'w')
stdout = sys.stdout
    
def extract_shots_with_pyscenedetect(video_file_path, threshold,
                                         min_scene_len):
    print("Started shot detection....")
    start = time.time()
    
    sys.stdout = null
    scene_list = []
    
    # Scene change detection (Finding boder frames for scene change)
    content_detector = scenedetect.detectors.ContentDetector(
            threshold = threshold, min_scene_len = min_scene_len)
    smgr = scenedetect.manager.SceneManager(detector=content_detector,
                                            quiet_mode=True)
    video_fps, frames_read, frames_processed=scenedetect.detect_scenes_file(
            video_file_path, smgr)
    
    scene_list=[0]+smgr.scene_list +[int(frames_read-1)]
    
    scene_list_tc = process(video_fps, scene_list)
    
    print("Total time taken for shot detection is {} secs".format(round((time.time()-start),2)))
    print("--"*50)
    
    return scene_list, scene_list_tc


def process(video_fps, scene_list):   
    
    sys.stdout = stdout
    
    print("No of scenes detected are {}".format(len(scene_list) - 1))
    # create new list with scene boundaries in milliseconds instead of frame #.
    scene_list_msec = [(1000.0 * x) / float(video_fps) for x in scene_list]
    # create new list with scene boundaries in timecode strings ("HH:MM:SS.nnn").
    scene_list_tc = [scenedetect.timecodes.get_string(x) for x in scene_list_msec]
    print("The scene changes are at the following time stamps {}".format(scene_list_tc))

    return scene_list_tc


if __name__ == '__main__':
    df = pd.read_excel(config.video_list_path)
    video_list = df["links"]
    video_list = video_list[2:5]
    scene_list_dict = {}
    filename = 'scene_list_file.dat'
    for video_url in video_list:
        print("Collecting scenes from {}".format(video_url))
        if os.path.exists(filename):
            with open(filename,'rb') as rpf:
                scene_list_dict = pickle.load(rpf)
        
        if video_url in scene_list_dict.keys():
            print("This video already present in file,skiping it")
            continue
        video_id, proto_name,video_title = file_download(video_url)
        videogen = imageio.get_reader(video_id,'ffmpeg')
        fps = videogen.get_meta_data()['fps']
        scene_list,scene_list_tc =  extract_shots_with_pyscenedetect(video_id,threshold = config.scene_detect_thresh, 
                min_scene_len = 10*fps)
        #pickling scene_list      

        video_feature =[video_id,scene_list,scene_list_tc]
        scene_list_dict[video_url] = video_feature
        
        with open(filename,'wb') as wpf:
            pickle.dump(scene_list_dict,wpf)
        #video_feature[:] = []