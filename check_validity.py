import cv2
import imageio
import logging
logger = logging.getLogger('object_detection')
logger.setLevel(logging.INFO)

def check_validity(video_file_path):
    
    videogen = imageio.get_reader(video_file_path,'ffmpeg')
        
    # Check for valid video file
    try:
        num_frames = videogen.get_meta_data()['nframes']
        logger.info("Valid video file registered. No of frames is {}".format(num_frames))
        return num_frames
    
    except:
        cap = cv2.VideoCapture(video_file_path)
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if num_frames == 0:
            logger.info("Problem with video file, unable to find num of frames")
            num_frames = None
            return num_frames
        else:
            logger.info("Valid video file registered. No of frames is {}".format(num_frames))
            num_frames = None
            return num_frames