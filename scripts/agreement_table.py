#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
import argparse
from collections import Counter
import numpy as np
import pandas as pd
import manynames as mn

#%% ---- FUNCTIONS TO RECREATE AGREEMENT TABLE
def snodgrass_agreement(rdict):
    vec = np.array([rdict[key] for key in rdict])
    vec_rel = vec/(np.sum(vec))
    agr = np.sum(vec_rel * np.log2(1/vec_rel))
    return agr

def percent_agreement(rdict):
    topname = rdict.most_common(1)[0][0]
    total = sum(rdict.values())
    return rdict[topname]/total

def make_df(manynames):
    vg_prop = []
    ntypesmin2 = []
    
    if not isinstance(manynames.iloc[0]['responses'], Counter):
        manynames['responses'] = manynames['responses'].apply(lambda x: Counter(x))

    for ix,row in manynames.iterrows():
        vg_weight = row['responses'][row['vg_obj_name']]/sum(row['responses'].values())
        vg_prop.append(vg_weight)
        min2types = [k for k in row['responses'].keys()]
        ntypesmin2.append(len(min2types))

    manynames['n_types_min2'] = ntypesmin2
    manynames['percent_agree_min2'] = manynames['responses'].apply(lambda x: percent_agreement(x))
    manynames['snodgrass_min2'] = manynames['responses'].apply(lambda x: snodgrass_agreement(x))
    return manynames
    
def make_agreement_table(resdf):
    tablerows = []
    tablerows.append(('all',
                     str("%.1f"%np.mean(resdf['n_types_min2'])),
                     str("%.1f (%.1f)"%(np.mean(resdf['percent_agree_min2'])*100,
                     np.std(resdf['percent_agree_min2'])*100)),
                     str("%.1f (%.1f)"%(np.mean(resdf['snodgrass_min2']),
                     np.std(resdf['snodgrass_min2'])))
                    ))

    for c in set(list(resdf['vg_domain'])):
        catdf = resdf[resdf['vg_domain'] == c]

        tablerows.append((c,
                        str("%.1f"%np.mean(catdf['n_types_min2'])),
                         str("%.1f (%.1f)"%(np.mean(catdf['percent_agree_min2'])*100,
                         np.std(catdf['percent_agree_min2'])*100)),
                         str("%.1f (%.1f)"%(np.mean(catdf['snodgrass_min2']),
                         np.std(catdf['snodgrass_min2'])))
                    ))

    outdf = pd.DataFrame(tablerows,columns=['domain','N','%top','H'])
    outdf['domain'] = pd.Categorical(outdf['domain'], 
                                     ['all', 'people', 'clothing', 'home', 'buildings', 
                                      'food', 'vehicles', 'animals_plants'])
    return outdf

#%% ---- MAIN
if __name__ == '__main__':
    #dict with paths to datasets
    datasets = {'en': '../manynames-en.tsv',
                'zh': '../manynames-zh.tsv'
                }
    for lang in datasets:
        #%%% ----- CHECK ARGUMENTS
        #setup argument parser
        arg_parser = argparse.ArgumentParser(
            description = '''Creates a summary table of name agreement indices 
                            (reproducing Table 3 in Silberer, Zarrieß, & Boleda,2020)''')
        
        #add required arguments
        arg_parser.add_argument('-mnfile', type=str, 
                                help='path to the TSV file containing the ManyNames data',
                                default=datasets[lang])
        
        #check provided arguments
        args = arg_parser.parse_args()
        
        #set values
        fn = args.mnfile
        
        #%%% ----- PROCESSING
        manynames = mn.load_manynames(fn)
        resdf = make_df(manynames)
        o1 = make_agreement_table(resdf)
        print(o1.sort_values(by = 'domain'))
        
        #save into CSV file
        o1.to_csv(f'agreement_table_{lang}.csv', index=False)
        
