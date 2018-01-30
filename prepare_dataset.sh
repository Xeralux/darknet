#!/bin/bash
# Set of training images overlap with all annotation
# Set of testing images overlap with all annotation
# There are annotations which has no corresponding images
# There are images that has no corresponding annotations

# This script SHOULD be modified as the syncing with the database gets better

ROOT_DIR=$(pwd)
TRAIN_LABEL_DIR="/home/dcsabai/video-analytics-train/DetectNetAnnotation/"
TRAIN_IMAGE_DIR="/home/dcsabai/ImageDataBase_NEW/train/images/"

VAL_LABEL_DIR="/home/dcsabai/video-analytics-train/DetectNetAnnotation/"
VAL_IMAGE_DIR="/home/dcsabai/ImageDataBase_NEW/val/images/"

rm data -r
mkdir data
cd data
mkdir train
cd train
echo "Synchronizing training images..."
rsync $TRAIN_IMAGE_DIR/ images -a --info=PROGRESS2,SYMSAFE
chown $USER:$USER images/
echo "Converting to JPG"
cd images
for f in $(ls); do
  sudo mogrify -format jpg $f &
done
cd ..
find $(pwd)/images/ -name "*.jpg" > train.txt
echo "Synchronizing labels:" $VAL_LABEL_DIR
rsync $TRAIN_LABEL_DIR/ labels -a --info=PROGRESS2,SYMSAFE
echo "Preprocessing labels (takes 1-2 min)..."
cd labels
for f in $(ls); do
  $ROOT_DIR/detectnet2yolo.py $f >> log &
done

echo
echo

cd $ROOT_DIR/data
mkdir val
cd val
echo "Synchronizing validation images..."
rsync $VAL_IMAGE_DIR/ images -a --info=PROGRESS2,SYMSAFE
chown $USER:$USER images/
echo "Converting to JPG"
cd images
for f in $(ls); do
  sudo mogrify -format jpg $f &
done
cd ..
find $(pwd)/images/ -name "*.jpg" > val.txt
echo "Synchronizing labels:" $VAL_LABEL_DIR
rsync $VAL_LABEL_DIR/ labels -a --info=PROGRESS2,SYMSAFE
echo "Preprocessing labels (takes 1-2 min)..."
cd labels
for f in $(ls); do
  $ROOT_DIR/detectnet2yolo.py $f >> log &
done
cd $ROOT_DIR