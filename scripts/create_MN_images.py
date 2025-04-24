# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:42:20 2023
- recreate MN_images from VG-source
@author: amaed
"""

#%% ----- DEPENDENCIES
import argparse
import os
import pandas as pd
import json
import requests
from io import BytesIO
from tqdm import tqdm
from PIL import Image, ImageDraw


#%% ----- MAIN
if __name__=="__main__":
    
    #%%% ----- CHECK ARGUMENTS
    #setup argument parser
    arg_parser = argparse.ArgumentParser(description = 'create ManyNames images from VG')
       
    #add required arguments
    arg_parser.add_argument('-mnfile', type=str, 
                            help='local path to the JSON file containing the ManyNames data',
                            default='../other-data/manynames-en.json')
      
    arg_parser.add_argument('-vgimg', type=str, 
                            help='path to the VG images (with subfolders VG_100K and VG_100K_2)', 
                            default='https://cs.stanford.edu/people/rak248/')
    
    arg_parser.add_argument('-outdir', type=str, 
                            help='output path for the ManyNames images', 
                            default='MN_images/')
    
    #check provided arguments
    args = arg_parser.parse_args()
    
    #set values
    mn_file = args.mnfile
    vg_img_dir = args.vgimg
    mn_img_dir = args.outdir
  

    #%%% ----- PROCESSING
    #data import
    manynames_df = pd.read_json(mn_file)
    additional_df = pd.read_csv('../other-data/additional-info-en.tsv', sep='\t')[['vg_object_id', 'link_vg']] #add needed columns
    mn_data = pd.merge(manynames_df, additional_df, on='vg_object_id').to_dict(orient='records')

    #create outdir
    if not os.path.isdir(mn_img_dir):
        os.mkdir(mn_img_dir)

    #image parameters
    lwidth = 7 #thickness of bounding box outline in pixels
    max_w = 597 # max width MN image 
    max_h = 447 # max height MN image

    for mn_itm in tqdm(mn_data[0:10]):
        
        #open vg_image
        if vg_img_dir == 'https://cs.stanford.edu/people/rak248/':
            response = requests.get(mn_itm['link_vg'])
            vg_img = Image.open(BytesIO(response.content))
        else:
            vg_img = Image.open(mn_itm['link_vg'].replace(
                'https://cs.stanford.edu/people/rak248/', vg_img_dir))
        
        #resize to max dimensions
        vg_w, vg_h = vg_img.size
        resize_ratio = min(max_h/vg_h, max_w/vg_w)
        mn_h = round(vg_h * resize_ratio)
        mn_w = round(vg_w * resize_ratio)
        vg_img = vg_img.resize((mn_w, mn_h), resample = Image.LANCZOS)
        
        #draw box on MN size image
        bbox = [mn_itm['vg_bbox_xywh'][0],
                mn_itm['vg_bbox_xywh'][1],
                mn_itm['vg_bbox_xywh'][0] + mn_itm['vg_bbox_xywh'][2],
                mn_itm['vg_bbox_xywh'][1] + mn_itm['vg_bbox_xywh'][3]]

        #draw image
        ImageDraw.Draw(vg_img).rectangle(bbox, outline ="red", width = lwidth)
    
        #save
        vg_img.save(mn_itm['link_mn'].replace(
            'http://manynames.upf.edu/', mn_img_dir))


