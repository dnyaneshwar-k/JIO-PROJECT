import file_download
from config import config
import pandas as pd

class JEAP(object):
    def __init__(self):
        #the url input has to be a list. Now this list can have mulitple files or single file.
        df = pd.read_csv(config.video_file_path)
        df = df["links"]
        
        for link in df:
            video_id, proto_name = file_download(link) #video_ids are nothing but path to the video files. 