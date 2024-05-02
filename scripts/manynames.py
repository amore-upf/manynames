#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
import argparse
import pandas as pd

#%% ---- FUNCTION TO LOAD MANYNAMES.TSV
def load_manynames(filename="../manynames-en.tsv", sep="\t", 
                         index_col=None):
    
    # read tsv
    resdf = pd.read_csv(filename, sep=sep, index_col=index_col)

    # remove any old index columns ==> @PAOLA remove this when we've made sure that the tsv files are ok
    columns = [col for col in resdf.columns if not col.startswith("Unnamed")]
    resdf = resdf[columns]
        
    # run eval on nested lists/dictionaries
    evcols = ['vg_same_object', 'vg_inadequacy_type', 
              'bbox_xywh', 'clusters', 'responses', 'singletons', 
              'same_object', 'adequacy_mean', 'inadequacy_type']
    
    for icol in evcols:
        if icol in resdf:
            resdf[icol] = resdf[icol].apply(lambda x: eval(x))
    
    return resdf

#%% ---- MAIN
if __name__=="__main__":
    
    #%%% ----- CHECK ARGUMENTS
    #setup argument parser
    arg_parser = argparse.ArgumentParser(
        description = '''opens TSV file for ManyNames and runs eval on nested data structures''')
       
    #add required arguments
    arg_parser.add_argument('-mnfile', type=str, 
                            help='path to the TSV file containing the ManyNames data',
                            default='../manynames-en.tsv')
    
    #check provided arguments
    args = arg_parser.parse_args()
    
    #set values
    fn = args.mnfile
    
    #%%% ----- PROCESSING
    print("Loading data from", fn)
    manynames = load_manynames(filename = fn)
    print(manynames.head())
