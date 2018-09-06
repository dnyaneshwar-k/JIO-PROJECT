# object_detection
An automated pipeline to evaluate multiple real time object detection algorithm

**Install requirements**
 ```
cd object_detection
pip install -r requirements.txt
 ```

**Start with making some directories**

```
cd object_detection
mkdir data
mkdir modified_frames
```

**Download the ssd_mobilenet_v2_512 model**

```
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
tar -xzvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
rm ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

**To check how to use run the video level detector**

```
cd object_detection
cp tests/test_video_level.py ../
python test_video_level.py
```

