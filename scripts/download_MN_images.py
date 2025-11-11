# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:46:59 2023
- takes a .tsv (like manynames-en.tsv from GitHub) or .csv (like manynames_data.csv 
  created from the search interface) as input. File needs to contain a column
  labelled "link_mn" with the image urls
- downloads the images specified in the input file into a folder (default: "MN_images/")
@author: amaed
"""

#%% ---- DEPENDENCIES
import argparse
import csv
import os
import urllib.request 
from tqdm import tqdm

#%% ---- MAIN
if __name__=="__main__":
    
    #%%% ----- CHECK ARGUMENTS
    #setup argument parser
    arg_parser = argparse.ArgumentParser(
        description = '''download subset of ManyNames images; requires a 
        .csv- or .tsv-file containing a column labelled "link_mn" with the urls 
        of the ManyNames images; the image search under 
        https://amore-upf.github.io/manynames/ can be used to generate such a file
        for a subset of ManyNames images''')
       
    #add required arguments
    arg_parser.add_argument('-mnfile', type=str, 
                            help='''path to the CSV or TSV file containing 
                            the image urls in a column labelled "link_mn"''',
                            default='../manynames-en.tsv')
      
    arg_parser.add_argument('-outdir', type=str, 
                            help='output path for the ManyNames images', 
                            default='MN_images/')
    
    #check provided arguments
    args = arg_parser.parse_args()
    
    #set values
    mn_file = args.mnfile
    mn_img_dir = args.outdir
    
    #%%% ----- PROCESSING
    # read file
    if mn_file[-4:] == '.tsv':
        delim = '\t'
    elif mn_file[-4:] == '.csv':
        delim = ','
    else: 
        raise Exception('Extension for input file needs to be .csv (comma-separated) or .tsv (tab separated).')
    
    with open(mn_file) as f:
        mn = list(csv.DictReader(f, delimiter=delim))
        
    #make image folder
    if not os.path.isdir(mn_img_dir):
        os.mkdir(mn_img_dir)

    #download unique image files
    img_links = list(set([i['link_mn'] for i in mn]))
    for url in tqdm(img_links):
        file_path = url.replace('http://manynames.upf.edu/', mn_img_dir)
        url = url.strip().replace(' ', '%20') # make sure urls with compounds are read properly
        if os.path.isfile(file_path):
            print('skipping: ' + file_path + ' because it already exists')
            continue
        else: 
            urllib.request.urlretrieve(url, file_path)
