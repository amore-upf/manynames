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
    evcols = ['vg_same_object', 'target_coord', 'clusters', 'responses', 
              'singletons', 'same_object', 'adequacy_mean', 'inadequacy_type',
              'bbox_xywh', 'vg_inadequacy_type', 'incorrect', 'perc_top_v2']
    
    for icol in evcols:
        if icol in resdf:
            resdf[icol] = resdf[icol].apply(lambda x: eval(x))
    
    #percentage topname as value not list
    resdf['perc_top_v2'] = resdf['perc_top_v2'].apply(lambda x: x[0])
    
    #return df
    return resdf

#%% ---- DIRECTLY RUN
if __name__=="__main__":
    
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "../manynames.tsv"

    print("Loading data from", fn)
    manynames = load_cleaned_results(filename = fn)
    print(manynames.head())