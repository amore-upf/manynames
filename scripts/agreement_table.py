#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
from collections import Counter
import sys
import numpy as np
import pandas as pd
import manynames as mn

#%% ---- FUNCTIONS TO RECREATE AGREEMENT TABLE
def snodgrass_agreement(rdict, vocab, singletons=False):
    # to decide: do we include singleton answers for calculating agreement?
    if singletons:
        vec = np.array([rdict[key] for key in rdict])
    else:
        vec = np.array([rdict[key] for key in rdict if vocab[key] > 1])
    vec_rel = vec/(np.sum(vec))
    agr = np.sum(vec_rel * np.log2(1/vec_rel))
    return agr

def percent_agreement(rdict):
    # to decide: do we include singleton answers for calculating agreement?
    topname = rdict.most_common(1)[0][0]
    total = sum(rdict.values())
    return rdict[topname]/total

def make_df(manynames):
    vg_is_common = []
    vg_prop = []
    ntypesmin2 = []
    
    if not isinstance(manynames.iloc[0]['responses'], Counter):
        manynames['responses'] = manynames['responses'].apply(lambda x: Counter(x))

    for ix,row in manynames.iterrows():
        vg_is_common.append(int(row['topname'] == row['vg_obj_name']))
        vg_weight = row['responses'][row['vg_obj_name']]/sum(row['responses'].values())
        vg_prop.append(vg_weight)
        min2types = [k for k in row['responses'].keys() if row['responses'][k] > 1]
        ntypesmin2.append(len(min2types))

    manynames['n_types_min2'] = ntypesmin2
    manynames['percent_agree_min2'] = manynames['responses'].apply(lambda x: percent_agreement(x))
    manynames['snodgrass_min2'] = manynames['responses'].apply(lambda x: snodgrass_agreement(x,{},True))
    manynames['vg_is_max'] = vg_is_common
    manynames['vg_mean'] = vg_prop
    return manynames
    
def make_agreement_table(resdf):
    nobjects = len(resdf)
    tablerows = []
    tablerows.append(('all',
                     str("%.1f"%np.mean(resdf['n_types_min2'])),
                     str("%.1f (%.1f)"%(np.mean(resdf['percent_agree_min2'])*100,
                     np.std(resdf['percent_agree_min2'])*100)),
                     str("%.1f (%.1f)"%(np.mean(resdf['snodgrass_min2']),
                     np.std(resdf['snodgrass_min2']))),
                     str("%.1f"%((np.sum(resdf['vg_is_max'])/nobjects)*100)),
                     str("%.1f"%((np.sum(resdf['vg_mean'])/nobjects)*100)),
                    ))

    for c in set(list(resdf['vg_domain'])):
        catdf = resdf[resdf['vg_domain'] == c]
        ncat = len(catdf)
        synagree = Counter()
        for s in set(list(catdf['vg_synset'])):
            syndf = catdf[catdf['vg_synset'] == s]
            synagree[s] = np.mean(syndf['vg_mean'])

        tablerows.append((c,
                        str("%.1f"%np.mean(catdf['n_types_min2'])),
                         str("%.1f (%.1f)"%(np.mean(catdf['percent_agree_min2'])*100,
                         np.std(catdf['percent_agree_min2'])*100)),
                         str("%.1f (%.1f)"%(np.mean(catdf['snodgrass_min2']),
                         np.std(catdf['snodgrass_min2']))),
                         str("%.1f"%((np.sum(catdf['vg_is_max'])/ncat)*100)),
                         str("%.1f"%((np.sum(catdf['vg_mean'])/ncat)*100)),
                    ))

    outdf = pd.DataFrame(tablerows,columns=['domain','N','%top','H','top=VG','%VG'])
    outdf['domain'] = pd.Categorical(outdf['domain'], 
                                     ['all', 'people', 'clothing', 'home', 'buildings', 
                                      'food', 'vehicles', 'animals_plants'])
    return outdf

#%% ---- DIRECTLY RUN
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print("Creating agreement table for", fn)
    else:
        fn = "../manynames.tsv"

    manynames = mn.load_cleaned_results(fn)
    resdf = make_df(manynames)
    o1 = make_agreement_table(resdf)
    print(o1.sort_values(by = 'domain'))
    
