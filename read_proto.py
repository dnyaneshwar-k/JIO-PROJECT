proto_path = "/Users/pradip.gupta/JEAP_database/logfiles/3IdiotsRajusJobInterview.bytes"

from read_protobuf import read_protobuf
import scenewise_pb2
#import pandas as pd
    
scene_list = scenewise_pb2.Scene_list()
    
f = open(proto_path,'rb') 
scene_list.ParseFromString(f.read())

s = open('output.txt', "w")
s.write(str(scene_list))

df = read_protobuf(proto_path, scene_list, prefix_nested=True)
df.to_csv("output.csv",encoding="utf-8")

f.close()
s.close()

# =============================================================================
# s = scene_list.scenes #all scenes
# 
# a = s[0]  #first scene
# a.video_id 
# a.s_no
# a.str_time
# a.stop_time
# 
# frames = a.frames #all frames of that scene
# 
# frame = frames[0] #first frame of that scene
# frame.frameno
# objs = frame.objs #all objects of that frame
# 
# obj = objs[0] #first object of that frame
# obj.class_name
# obj.conf
# obj.bbox   
# 
# with open('output_json.txt', "w") as g:    
#     for scene in scene_list.scenes:
#         g.write(scene.video_id+" "+scene.s_no+" "+scene.str_time+" "+scene.stop_time)
# =============================================================================
    
    
    