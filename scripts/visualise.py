#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
import argparse
import matplotlib.pyplot as plt
from skimage import io
import manynames as mn
import pandas as pd
from ast import literal_eval

#%% ---- FUNCTION TO SHOW OBJECT WITH BOUNDING BOX AND NAMES
def show_objects(url, bbox, objname, block_display=True):
    # set the default font family to a font that supports Chinese characters
    plt.rcParams['font.family'] = ['Arial Unicode MS']
    
    im = io.imread(url)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(im, aspect='equal')

    if bbox[0] == 0:
        bbox[0] = 1
    if bbox[1] == 0:
        bbox[1] = 1
        
    plt.gca().add_patch(
        plt.Rectangle((bbox[0], bbox[1]),
                        bbox[2], bbox[3], fill=False,
                        edgecolor='red', linewidth=2, alpha=0.5)
            )
    plt.gca().text(bbox[0], bbox[1] - 2,
                '%s' % (objname),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=10, color='white')
        
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show(block=block_display)

#%% ---- DIRECTLY RUN
if __name__=="__main__":
    
    #%%% ----- CHECK ARGUMENTS
    #setup argument parser
    arg_parser = argparse.ArgumentParser(
        description = '''Draws example images using the VG-souce and showing the MN-target object and observed object names.''')
       
    #add arguments
    arg_parser.add_argument('-mnfile', type=str, 
                            help='path to the TSV file containing the ManyNames data',
                            default='../manynames-en.tsv')
    
    arg_parser.add_argument('-vgids', type=str, 
                            help='a list of VG_image_ids',
                            default='[2415243, 2354270, 2404023, 2374399, 2362509, 2368028, 2388175, 2366047]')
    
    #check provided arguments
    args = arg_parser.parse_args()
    
    #set values
    fn = args.mnfile
    ids = literal_eval(args.vgids)


    #%%% ----- PROCESSING
    manynames = mn.load_manynames(filename=fn)
    additional = pd.read_csv('additional-info.tsv', sep='\t')[['vg_object_id', 'vg_obj_name', 'vg_image_name', 'link_vg']]
    manynames = pd.merge(manynames, additional, on='vg_object_id')
   
    for image_id in ids:
        mn_item = manynames[manynames["vg_image_id"]==image_id]
        url = mn_item["link_vg"].values[0]
        responses = mn_item["responses"].values[0]
        mn_objnames = " / ".join(responses.keys())
        bbox = literal_eval(mn_item["vg_bbox_xywh"].values[0])
        show_objects(url, bbox, mn_objnames)
    
                
                
    
