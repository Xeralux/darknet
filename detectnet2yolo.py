#!/usr/bin/env python3
import os, sys, shutil
import csv
from PIL import Image

# fname = '01cvg/sensity/orig/ImageDataBase_NEW/train/labels/Sensity_Timelapse_USA_WashingtonDC_N02c01055-0306170201-0_TrafficAndParking_F0018.txt'

# example INPUT looks like this:
# ['Car', '0.0', '0', '0.0', '527.0', '356.0', '627.0', '474.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '']
# ['Car', '0.0', '0', '0.0', '739.0', '389.0', '838.0', '487.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '']
# ['DontCare', '0.0', '0', '0.0', '1098.0', '401.0', '1277.0', '527.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '']

# example OUTPUT should look like this:
# [class_id_car, rel_topleft_x, rel_topleft_y, width, height]
# etc...

classes = ['Car', 'Person', 'cyclist', 'Bus', 'Trailer', 'Machine', 'Truck']

# Remove these labels
discarded_classes = ['Bus', 'Trailer', 'Machine', 'Truck']


def convert_bbox(size, box):
    # Normalize box size
    # centralize X, Y
    # compute H, W
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    abs_w = box[1] - box[0]
    abs_h = box[3] - box[2]
    x = x * dw
    w = abs_w * dw
    y = y * dh
    h = abs_h * dh
    return [x, y, w, h]

def get_corresponding_image_path(annot_fname):
    # INPUT: ~/<annot_fname>
    # OUTPUT: ~/../images/<annot_fname_without_extension>+.jpg
    basename = os.path.basename(annot_fname)
    name = os.path.splitext(basename)[0]
    res = annot_fname[:annot_fname.find(basename)] + '../images/' + name + '.bmp'
    return res


def check_image_exists(annot_fname):
    img_fname = get_corresponding_image_path(annot_fname)
    return os.path.exists(img_fname)

def get_image_dims(img_fname):
    im=Image.open(img_fname)
    w = int(im.size[0])
    h = int(im.size[1])
    return w, h

def get_corresponding_dims(annot_fname):
    img_fname = get_corresponding_image_path(annot_fname)
    return get_image_dims(img_fname)

def get_abs_bbox_from_record(record):
    xmin, ymin, xmax, ymax = list(map(float, record[4:8]))
    # have to reshape it first to VOC
    return xmin, xmax, ymin, ymax

def process_record(record, dimensions):
    cid = classes.index(record[0])
    detectnet_bbox = get_abs_bbox_from_record(record)
    yolo_bbox = convert_bbox(dimensions, detectnet_bbox)
    return [cid] + yolo_bbox

def process_file(fname):

    with open(fname, 'r') as f:
        csvreader = csv.reader(f, delimiter=' ')
        records = list(csvreader)
    shutil.move(fname, fname+'.bak')
    dims = get_corresponding_dims(fname)
    try:
        f = open(fname, 'w')
        csvwriter = csv.writer(f, delimiter=' ')
        for record in records:
            if record[0] in discarded_classes:
                continue
            csvwriter.writerow(process_record(record, dims))
    except BaseException as e:
        shutil.move(fname+'.bak', fname)
        raise e


if __name__ == '__main__':
    fname = sys.argv[1]
    if check_image_exists(fname):
        try:
            process_file(fname)
            print('+++ script finished succesfully: %125s' % fname)
        except BaseException as e:
            print('!!! ERROR: %125s' % fname)
            raise e
    else:
        print('--- no corresponding image file: %125s' % fname)
