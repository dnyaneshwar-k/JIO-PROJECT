import platform
import matplotlib 

if platform.system() == 'Darwin':
    matplotlib.use('TkAgg')

if platform.system() == 'Linux':
    matplotlib.use('Agg')
    
#import matplotlib.pyplot as plt
import os,sys
from PIL import Image
import config
sys.path.append(config.root_path)
from object_detection.utils import visualization_utils as vis_util
from model import category_index



def visualize_and_save(frame, confidence, c, box_io, instance_masks, file_name, 
                       frame_number, visualize=False):
	# visualize you code
    vis_util.visualize_boxes_and_labels_on_image_array( frame,
                                                        box_io,
                                                        c,
                                                        confidence,
                                                        category_index,
                                                        instance_masks=instance_masks,
                                                        use_normalized_coordinates=True,
                                                        line_thickness=4)
    #plt.figure(figsize=(12, 8))
#    if visualize:
#	    plt.imshow(frame)
#	    plt.show()
    save_path = os.path.join(file_name, str(frame_number))
    img = Image.fromarray(frame)
    img.save(save_path+".jpg")
    #plt.close()

