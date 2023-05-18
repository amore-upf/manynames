# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:46:59 2023
- creates a folder "images" and downloads the images specified in the csv 
  downloaded from the ManyNames website into it
- can be run on the command line with:
  "python download_Manynames_images.r"
@author: amaed
"""

#%% ---- DEPENDENCIES
import csv
import os
import urllib.request 

#%% ---- MAIN
if __name__=="__main__":
    
    # read csv
    with open('ManyNames_data.csv') as f:
        mn = list(csv.DictReader(f, delimiter=","))
        
    #make image folder
    dir_name = 'images/'
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)  

    #download unique image files
    img_links = set([i['link_mn'] for i in mn])
    for url in img_links:
        file_path = url.replace('http://object-naming-amore.upf.edu//', dir_name)
        urllib.request.urlretrieve(url, file_path)
        print(file_path + ' complete')
