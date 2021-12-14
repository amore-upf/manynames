#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
import sys
import pandas as pd
from collections import Counter

#%% ---- FUNCTION TO LOAD MANYNAMES.TSV
def load_cleaned_results(filename = "../manynames.tsv", sep = "\t", 
                         index_col = None):
   
    # read tsv
    resdf = pd.read_csv(filename, sep=sep, index_col=index_col)
    
    # remove any old index columns
    columns = [col for col in resdf.columns if not col.startswith("Unnamed")]
    resdf = resdf[columns]
    
    # run eval on nested lists/dictionaries
    resdf['responses'] = resdf['responses'].apply(lambda x: Counter(eval(x)))
    resdf['singletons'] = resdf['singletons'].apply(lambda x: eval(x))

    return resdf

#%% ---- FUNCTION TO LOAD IMAGES.TSV
def load_images(filename = "../images.tsv", sep="\t", index_col=None):
    imagedf = pd.read_csv(filename, sep=sep, index_col=index_col)
    imagedf["bbox_xywh"] = imagedf["bbox_xywh"].apply(lambda x: eval(x))
    return imagedf

#%% ---- DIRECTLY RUN
if __name__=="__main__":
    
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "../manynames.tsv"

    print("Loading data from", fn)
    manynames = load_cleaned_results(filename = fn)
    print(manynames.head())
