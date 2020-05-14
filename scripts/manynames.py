#!/usr/bin/env python
# coding: utf-8
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from numpy import nan


def load_cleaned_results(filename, sep="\t", index_col=None):
    resdf = pd.read_csv(filename, sep=sep, index_col=index_col)
    # integrate with old csv format
    if "verified" in resdf.columns:
        return load_cleaned_results_old(filename, sep=sep, index_col=index_col)
    
    for col in ['spellchecked', 'spellchecked_min2', 'clean', 'canon', 'responses']:
        if col in resdf:
            resdf[col] = resdf[col].apply(lambda x: Counter(eval(x)))

    # remove any old index columns
    columns = [col for col in resdf.columns if not col.startswith("Unnamed")]
    resdf = resdf[columns]

    # eval verified column if present
    """ columns: adequacy_mean	inadequacy_type	same_object	vg_adequacy_mean	vg_inadequacy_type	vg_same_object incorrect """
    if 'adequacy_mean' in resdf:
        for verif_type in ['adequacy_mean', 'inadequacy_type', 'same_object',  'vg_inadequacy_type', 'vg_same_object']:
            resdf[verif_type] = resdf[verif_type].apply(lambda x: eval(x))
            
    if 'incorrect' in resdf: # MNv2.0
        resdf['incorrect'] = resdf['incorrect'].apply(lambda x: eval(x))

    return resdf

def load_images(filename, sep="\t", index_col=None):
    imagedf = pd.read_csv(filename, sep=sep, index_col=index_col)
    imagedf["bbox_xywh"] = imagedf["bbox_xywh"].apply(lambda x: eval(x))
    return imagedf
    
def _render_objects(sampled_data_df, image_df, 
                    imagedir_path, study_basedir, 
                    label_objects=False, save_fig=False):
    postfix = "-labeled" if label_objects else ""
    for row in sampled_data_df.iterrows():
        if save_fig:
            imgfile_out = _image_path_bbox(row[1]["image_id"],
                                        row[1]["object_id"],
                                        row[1]["sample_type"]+postfix,
                                        imagedir_path=os.path.join(study_basedir, "images"))
            if os.path.exists(imgfile_out):
                sys.stderr.write("Skipping %s ((image already exists))\n" % (imgfile_out))
                continue
        image_id = row[1]["image_id"]
        image_path = _image_path(image_df, image_id, imagedir_path=imagedir_path)
        if not os.path.exists(image_path):
            url = image_df[image_df["image_id"]==image_id]["url"].values[0]
            sys.stderr.write("Image path not found: %s\n\t(url: %s)\n" % (image_path, url))
            continue
        
        try:
            image = plt.imread(image_path)
        except OSError: 
            sys.stderr.write("OSError. Maybe file %s is empty.\n" % (image_path))
            continue
        img_height = image_df[image_df["image_id"]==image_id]["height"].values[0]
        img_width = image_df[image_df["image_id"]==image_id]["width"].values[0]
        bb = eval(row[1]["bbox_xywh"])
        
        plt.cla()
        plt.imshow(image)
        plt.gca().add_patch(
            plt.Rectangle((max(4, bb[0]-3), max(4, bb[1]-3)),
                            min(img_width-6, bb[2]), min(img_height-7, bb[3]), fill=False,
                            edgecolor='r', linewidth=6)
            )
        plt.xticks([])
        plt.yticks([])
        #plt.title('{}'.format(obj_names))
        if label_objects:
            obj_names = eval(row[1]["obj_names"])
            obj_names = "/".join(obj_names) if isinstance(obj_names, list) else obj_names
            plt.text(bb[0]+3, bb[1]+bb[3]-3, obj_names, fontsize=20, 
                     color="red", backgroundcolor="white")
        if save_fig:
            plt.tight_layout()
            sys.stderr.write("Saving rendered object in %s\n" % imgfile_out)
            plt.savefig(imgfile_out)
        else:
            plt.show()

def _image_path(image_df, image_id, imagedir_path="data/"):
    if WINDOWS:
        imagedir_path = os.path.join(imagedir_path, "windows_images")
    else:
        imagedir_path = os.path.join(imagedir_path, "images")
    url = image_df[image_df["image_id"]==image_id]["url"].values[0]
    img_dir, img_file = url.split("/")[-2:]
    return os.path.join(imagedir_path, img_dir, img_file)

def _image_path_bbox(image_id, object_id, sample_type, 
                     imagedir_path="pilot/images/"):
    imgfile_out = "%s_%s_%s.png" % (image_id, object_id, sample_type)
    return os.path.join(imagedir_path, imgfile_out)

def load_cleaned_results_old(filename, sep="\t", index_col=None):
    """
    @deprecated
    """
    sys.stderr.write("\nInformation in %s is outdated. Please consider using updated csv.\n"%filename)
    resdf = pd.read_csv(filename, sep=sep, index_col=index_col)
    resdf['spellchecked'] = resdf['spellchecked'].apply(lambda x: Counter(eval(x)))
    resdf['clean'] = resdf['clean'].apply(lambda x: Counter(eval(x)))
    resdf['canon'] = resdf['canon'].apply(lambda x: Counter(eval(x)))

    # remove any old index columns
    columns = [col for col in resdf.columns if not col.startswith("Unnamed")]
    resdf = resdf[columns]

    # eval verified column if present
    if 'verified' in resdf:
        resdf['verified'] = resdf['verified'].apply(eval)
    if 'spellchecked_min2' in resdf:
        resdf['spellchecked_min2'] = resdf['spellchecked_min2'].apply(lambda x: Counter(eval(x)))

    return resdf

if __name__=="__main__":
    MN_V2 = False
    LOAD_IMAGEDATA = False
    
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    elif MN_V2 is True:
        fn = '../proc_data_phase0/mn_v2.0/manynames-v2.0_valid_responses_ad0.40.csv'
    else:
        fn = "../manynames_v1.0.tsv"
        
    print("Loading ManyNames from", fn)
    manynames = load_cleaned_results(fn)
    print(manynames.head())
    
    if LOAD_IMAGEDATA:
        imagedata = load_images("../images.tsv")
    
