from pytube import YouTube
import config
import os
import re
import time
#import logging
#logger = logging.getLogger('object_detection')
#logger.setLevel(logging.INFO)


def file_download(url):
    
    start = time.time()
    print("Attempting file download....")
    
    yt = YouTube(url)
    heading = re.sub('[^A-Za-z0-9]+', '', yt.title)
    
    stream=yt.streams.first()
    extension=stream.mime_type.split('/')
    video_id=os.path.join(config.video_path,heading+'.'+extension[1])   
    
    if not os.path.exists(video_id):
        yt.streams.first().download(config.video_path,filename=heading)
        print("Time taken for download is {} secs".format(round((time.time()-start),2)))
        print("--"*50)
    else:
        print("Video file  for url {} already present in database. Not downloading it".format(url))
        print("Time consumed is {} secs".format(round((time.time()-start),2)))
        print("--"*50)
        
    proto_name=heading+".bytes"
        
    return(video_id, proto_name,heading)
    
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=ZQ9_zrvv5W4&pbjreload=10"
    video_id, proto_name = file_download(url)
    print(video_id, proto_name)