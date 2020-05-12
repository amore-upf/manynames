#!/usr/bin/env python
# coding: utf-8
import glob
import json
import os
import sys
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.corpus import wordnet as wn

import manynames as mn # former module name: load_results

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

    for ix,row in manynames.iterrows():
        vg_is_common.append(int(row['mn_topname'] == row['vg_obj_name']))
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
    print(outdf.sort_values(by=['N'], ascending=[False]).to_latex(index=False))
    return outdf

def make_synset_df(manynames_df, vg_path="../vgenome/"):
    name2synset = None
    if False:
        objdf = pd.read_json(os.path.join(vg_path, "objects.json.zip"), 
                             compression='zip')
        objdf = pd.DataFrame([obj for listobj in list(objdf['objects']) for obj in listobj])
        objdf = objdf[objdf['synsets'].apply(lambda x: len(x) >0)]
        objdf['synset'] = objdf['synsets'].apply(lambda x: x[0])
        objdf['name'] = objdf['names'].apply(lambda x: x[0])
        name2synset = dict(list(zip(objdf['name'],objdf['synset'])))

    vg_is_common = []
    vg_prop = []
    ntypesmin = []

    syn2resp = {sn:Counter() for sn in set(manynames_df["vg_synset"].values)}
    syncount = Counter()
    for ix,row in manynames_df.iterrows():
        sn = row['vg_synset']
        syn2resp[sn].update(row['responses'])
        syncount[sn] += 1
    syn2domain = dict(zip(manynames_df["vg_synset"], manynames_df["vg_domain"]))
    
    new_rows = []
    for (sn, cnt) in syncount.items():
        sn_names = [l._name for l in wn.synset(sn).lemmas()]
        if row['vg_obj_name'] not in sn_names:
            sn_names.append(row['vg_obj_name'])
        new_rows.append(
            (sn, sn_names, syn2domain[sn],
             sn, syn2resp[sn], syncount[sn]))

    syndf = pd.DataFrame(new_rows,
                         columns=[
        'vg_obj_synset', 'vg_obj_names', 'vg_domain', 
        'vg_synset', 'responses', 'n_images'])

    syndf['responses_min2'] = syndf['responses'].apply(lambda x: Counter({k:x[k] for k in x if x[k] > 1}))

    for ix,row in syndf.iterrows():
        #mn_topname = row['mn_topname']
        mn_topname = row['responses'].most_common(1)[0][0]
        #vg_is_common.append(int(mn_topname == row['vg_obj_name']))
        vg_is_common.append(int(mn_topname in row['vg_obj_names']))
        vg_weight = sum([row['responses_min2'][n] for n in row['vg_obj_names']])/sum(row['responses'].values())
        vg_prop.append(vg_weight)
        min2types = [k for k in row['responses'].keys() if row['responses'][k] > 1]
        ntypesmin.append(len(min2types))


    syndf['vg_is_max'] = vg_is_common
    syndf['vg_mean'] = vg_prop
    syndf['n_types_min2'] = ntypesmin
    syndf['snodgrass_min2'] = syndf['responses_min2'].apply(lambda x: snodgrass_agreement(x,{},True))
    syndf['percent_agree_min2'] = syndf['responses_min2'].apply(lambda x: percent_agreement(x))
    #syndf['vg_name_synset'] = syndf['vg_obj_name'].apply(lambda x: name2synset[x])

    return syndf, name2synset

def agreement_boxplot(resdf, postfix=""):
    plotdata = []
    cats = ['all']
    plotdata.append(list(resdf['percent_agree_min2']))

    for c in set(list(resdf['vg_domain'])):
        cats.append(c)
        catdf = resdf[resdf['vg_domain'] == c]
        plotdata.append(list(catdf['percent_agree_min2']))

    fig, ax = plt.subplots()
    ax.boxplot(plotdata,labels=cats,widths=0.8,notch=True)
    plt.xticks(range(1,len(cats)), cats, rotation=45)
    plt.tight_layout()
    plt.savefig("agreebox%s.png" % postfix)

    sys.exit()
    fig, ax = plt.subplots()
    plotdata = []
    cats = []
    rangec = []

    for i,c in enumerate(list(set(list(resdf['vg_synset'])))[:20]):
        cats.append(c)
        rangec.append((i+1)*4)
        catdf = resdf[resdf['vg_synset'] == c]
        plotdata.append(list(catdf['percent_agree_min2']))

    print(rangec)
    fig, ax = plt.subplots()
    ax.boxplot(plotdata)
    plt.xticks(range(1,len(cats)+1), cats,fontsize = 6, rotation = 45)
    plt.subplots_adjust(bottom=0.15)
    plt.tight_layout()
    plt.savefig("agreebox_synset%s.png" % postfix)


if __name__ == '__main__':
    MN_V2 = False
    version = ""
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print("Creating agreement table for", fn)
    elif MN_V2 is True:
        fn = '../proc_data_phase0/mn_v2.0/manynames-v2.0.csv'
        version = "_manynames_v2"
    else:
        fn = "../manynames_v1.0.tsv"
        version = "_manynames_v1"

    manynames = mn.load_cleaned_results(fn)
    resdf = make_df(manynames)
    o1 = make_agreement_table(resdf)
    #agreement_boxplot(resdf, postfix=version)

    #syndf,name2synsets = make_synset_df(resdf)
    #print(syndf[syndf['vg_is_max'] == 1].head())
    #print(syndf[syndf['vg_is_max'] == 0].head())
    #o2 = make_agreement_table(syndf)
    #o3 = pd.concat([o1,o2[list(o2.columns[1:])]],axis=1)
    #print(o3.to_latex(index=False))

    
