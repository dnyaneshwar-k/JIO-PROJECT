#import os
from flask import Flask, request, json
# import json
import VideoDetector
#import logging

app = Flask(__name__)

confidence = 0.6
video_level_detector = VideoDetector.VideoLevelDetector(confidence)

@app.route('/detect_objects', methods=['POST'])
def classify_doc():
    
    try:
        video_url = request.form['video_url']
        
        try:
            proto_url = video_level_detector.video_detector(video_url)
            return proto_url
        except:
            print("Error in processing video file")
            return None
    
    except:
        print("Error in input. Valid url not found")
        return None
    


