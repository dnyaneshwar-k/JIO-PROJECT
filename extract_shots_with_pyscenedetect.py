import scenedetect
import os,sys
import time
import pandas as pd
from file_download import file_download
import config
import imageio
import pickle
from multiprocessing import Pool
from functools import partial
#import logging
#logger = logging.getLogger('object_detection')
#logger.setLevel(logging.INFO)

null = open(os.devnull, 'w')
stdout = sys.stdout
    
def extract_shots_with_pyscenedetect(video_url,filename, threshold,
                                         min_scene_len):
    scene_list_dict = {}

    video_file_path, proto_name,video_title = file_download(video_url)

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
    
    #scene_list=[0]+smgr.scene_list +[int(frames_read-1)]
    scene_list = smgr.scene_list
    scene_list_tc = process(video_fps, scene_list)
    
    print("Total time taken for shot detection is {} secs".format(round((time.time()-start),2)))
    print("--"*50)
    
    video_feature = [video_file_path,scene_list,scene_list_tc,proto_name]
    scene_list_dict[video_url] = video_feature

    with open(filename,'ab') as wpf:
        pickle.dump(scene_list_dict,wpf,protocol=pickle.HIGHEST_PROTOCOL)

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
    video_list = video_list[5:6].tolist()
    
    filename = 'scene_list_file.dat'
    
    if os.path.exists(filename):
        processed_videos = []
        with (open(filename, "rb")) as openfile:
            while True:
                try:
                    processed_videos.append(pickle.load(openfile))
                except EOFError:
                    break
        processed_video_urls = []

        for video in processed_videos:
            for key in video:
                processed_video_urls.append(key)

        not_processed_urls = []
        for video in video_list:
            if video not in processed_video_urls:
                not_processed_urls.append(video)
    else:
        not_processed_urls = video_list
    
    print(not_processed_urls)
    
    for video_url in not_processed_urls:
        start_time = time.time()
        extract_shots_with_pyscenedetect(video_url,filename = filename,threshold = config.scene_detect_thresh,min_scene_len = 250)
        print("time taken for shot detection is:",time.time()-start_time)
    print("total time:",time.time()-start_time)

    ####FOR MULTIPLE URLS AT A TIME #########

    # if len(not_processed_urls) != 0:
    #     p = Pool()
    #     func = partial(extract_shots_with_pyscenedetect,filename = filename,threshold = config.scene_detect_thresh,min_scene_len = 250)
    #     p.map(func,not_processed_urls)
    # else:
    #     print("all videos are processed")

