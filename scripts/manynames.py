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
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        
    elif MN_V2 is True:
        fn = '../proc_data_phase0/mn_v2.0/manynames-v2.0_valid_responses_ad0.40.csv'
    else:
        fn = "../manynames_v1.0.tsv"

    print("Loading ManyNames from", fn)
    manynames = load_cleaned_results(fn)
    print(manynames.head())
    
