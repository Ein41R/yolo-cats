# YOLO CAT DETECTION MODEL

view [Dataset]{https://www.kaggle.com/datasets/adeneousminz/lab5-dat301m-dataset-praparing}

view imageset for [Testing]{https://github.com/AtharvaTaras/Cat-Images-Dataset}a


## documentation

The first training finished within 232 Epoch, but the finished model barely recognised any cats.

I tried specifying training details for training,
tried switching the base model,
questioned wheter I used a pretrained model or training a model from scratch.

Checked logs, found that label classes were corrupted, some with 0 (cat) and 25 (undefined). manually fixed dataset.