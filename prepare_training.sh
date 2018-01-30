#!/bin/bash
wget https://pjreddie.com/media/files/darknet19_448.conv.23 -O pretrained.weights
mkdir backup_weights
echo "Rewrite `cfg/sensity.data` file-list path to your path"
echo "Run `make -j28` to compile darknet. (tested with CUDA 8, cuDNN 7.0.5)"
echo "Run `./darknet detector train cfg/sensity.data cfg/sensity-architecture.cfg pretrained.weights -gpus 0,1`"
