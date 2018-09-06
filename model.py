
import config
import numpy as np
import tensorflow as tf
import sys

sys.path.append(config.root_path)

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util

label_map = label_map_util.load_labelmap(config.coco_label_map_path)
categories = label_map_util.convert_label_map_to_categories(label_map, 
                                                            max_num_classes=config.NUM_CLASSES, 
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


invertor = lambda ar, inv_ratio: np.array(ar)*inv_ratio


class ObjectDetector(object):
    
    def __init__(self):
        pass

    def detect(self, image_np, frame_no, graph_def_bc):
        
        # Load network graph
        tf.import_graph_def(graph_def_bc, name='')
        
        # Configure session for gpu support
        config_tf = tf.ConfigProto()
        config_tf.gpu_options.allow_growth = True
        config_tf.gpu_options.per_process_gpu_memory_fraction = config.gpu_allocation
        config_tf.gpu_options.allocator_type = "BFC"
        
        with tf.Session(config=config_tf) as sess:
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                    ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                
                # Reframe is required to translate mask from box coordinates to 
                # image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])
                detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,
                                   feed_dict={image_tensor: np.expand_dims(image_np, 0)})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            output_dict['frame_no'] = frame_no
            
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]

        # Prevent memory leaking
        tf.reset_default_graph()
        
        return output_dict
