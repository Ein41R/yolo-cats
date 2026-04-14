# YOLO CAT DETECTION MODEL

view [Dataset](https://www.kaggle.com/datasets/adeneousminz/lab5-dat301m-dataset-praparing)

view imageset for [Testing](https://github.com/AtharvaTaras/Cat-Images-Dataset)a


## documentation

The first training finished within 232 Epoch, but the finished model barely recognised any cats.

I tried specifying training details for training,
tried switching the base model,
questioned wheter I used a pretrained model or training a model from scratch.

Checked logs, found that label classes were corrupted, some with 0 (cat) and 25 (undefined). manually fixed dataset.

unfortunatel switched 0 to 25 but 0-0 class indicies are needed for single class dataset

### Update: 
Training worked now, reliably detecting cats, however, I just found the following [repo](https://github.com/jones139/catocam/tree/main), how quiant. So I won't be needing this project in the future, since [jones139](https://github.com/jones139) undoubtedly did a better job training a cv model than I did. Therefore I will be orphaning this repo after properly documenting my work. 

Reached peak accuracy after 152 Epochs this time, plots will follow, since I had to interrupt the process early, I will write a script to visualise the results.csv and upload it all to the repo.
