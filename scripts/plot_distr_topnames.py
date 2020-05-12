#!/usr/bin/env python
# coding: utf-8
import os
import sys

from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt

import manynames as mn # former module name: load_results


def statistics_mn_topnames(df, domain_key, print_stats=False):
    """
    VG image distribution, MN entry-level distribution, per domain
    """
    # count frequency of vg object names
    obj_name_df = df[["mn_topname", domain_key]]
    obj_name_df = pd.DataFrame(obj_name_df.groupby(by=["mn_topname", domain_key])["mn_topname"].count())
    obj_name_df.rename(columns={"mn_topname": "mn_count"}, inplace=True)
    obj_name_df.reset_index(level=[1], inplace=True)
    obj_name_df["mn_topname"] = obj_name_df.index
    obj_name_df.set_index(pd.Index(list(range(len(obj_name_df)))), inplace=True)
    obj_name_df.sort_values(by=[domain_key, "mn_count"], ascending=False, inplace=True)
    
    print_df = dict()
    for cat in set(df.vg_domain):
        top_names = obj_name_df[obj_name_df[domain_key]==cat].head(10)["mn_topname"].tolist()
        counts_top_names = obj_name_df[obj_name_df[domain_key]==cat].head(10)["mn_count"].tolist()
        print_df[cat] = ["%s (%d)" % (top_names[idx], round(counts_top_names[idx])) for idx in range(len(top_names))]
        
    print_df = pd.DataFrame.from_dict(print_df)
    if print_stats:
        print("\n\n**Top 10 MN names for each MN/VG domain**")
        print(print_df.to_latex())
    
    return obj_name_df, print_df


def plot_function(domain, ax, nm2domain, text_fontsize=8):
    """
    A bit hacky function to create a stacked bar plot for an individual MN domain.
    """
    num_1domain = domain_gdf.loc[domain][domain_gdf.loc[domain]>0].sort_values(ascending=False)

    a = num_1domain.unstack(fill_value=0)
    plot_singledomain = a.plot(ax=ax, kind="bar", stacked=True, legend=False, alpha=0.65, width=.6)
    # hide x ticks ("vg_count")
    plot_singledomain.xaxis.set_major_formatter(plt.NullFormatter())
    plot_singledomain.set_xlabel(domain.replace("_", "/"), fontsize=text_fontsize)
    plot_singledomain.set_ylabel("Cumulated sum of images / name", fontsize=text_fontsize)

    # label some subbars with their names
    ypositions = num_1domain.cumsum()
    idx2show = [("c",0)]
    for idx in range(1, len(ypositions)):
        if -ypositions[idx-1]+ypositions[idx] < 90:
            break
        idx2show.append(("c", idx))
    no_nms2show = 5
    num = 0
    for idx in list(range(16, len(ypositions),3)):
        obj_name = a.columns[idx]
        mn_domain = nm2domain.get(obj_name, "")
        if mn_domain != domain:
            continue
        idx2show.append(("r",idx))
        num += 1
        if num >= no_nms2show:
            break
    if True:
        adj_ycoord = 0
        for (pos,idx) in idx2show:
            if idx == 0:
                ycoord = int(ypositions[idx]/2)
            else:
                ycoord = int((ypositions[idx-1]+ypositions[idx])/2) 
            if pos=="r":
                xcoord = int(domains.index(domain)/(len(domains)*2.5))+.28
                if adj_ycoord > 0:
                    ycoord = adj_ycoord
                    adj_ycoord += 200
                else:
                    adj_ycoord = ycoord + 200
            else:
                xcoord = int(domains.index(domain)/(len(domains)*2.5))
            obj_name = a.columns[idx]
            ax.text(xcoord, ycoord, 
                    obj_name, ha='center', va='center', 
                    color='black', fontsize=text_fontsize-1)
        if domain!="animals_plants":
            ax.spines['left'].set_visible(False)
        else:
            mkfunc = lambda x, pos: '%1.0fK' % (x / 1000)
            mkformatter = plt.FuncFormatter(mkfunc)
            plot_singledomain.yaxis.set_major_formatter(mkformatter)
            plot_singledomain.tick_params(labelsize=text_fontsize-1)
            
        if domain!="vehicles":
            ax.spines['right'].set_visible(False)
    return plot_singledomain


if __name__ == '__main__':
    MN_V2 = False
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        print("Creating agreement table for", fn)
        postfix = "manynames_vx.x"
    elif MN_V2 is True:
        fn = '../proc_data_phase0/mn_v2.0/manynames-v2.0_valid_responses_ad0.40.csv'
        postfix = "manynames_v2.0"
    else:
        fn = "../manynames_v1.0.tsv"
        postfix = "manynames_v1.0"

    manynames_df = mn.load_cleaned_results(fn)
    nm2domain = dict(zip(manynames_df["vg_obj_name"], manynames_df["vg_domain"]))
    
    domain_key = "mn_domain" #"vg_domain"
    obj_name_df, print_df = statistics_mn_topnames(manynames_df, domain_key)

    domain_groups = obj_name_df.groupby([domain_key]).apply(lambda x: (x.groupby('mn_topname')
                                          .sum().sort_values('mn_count', ascending=False)))
    domain_gdf = domain_groups.unstack(fill_value=0)
    domains = [domain[0] for domain in domain_gdf.iterrows()]

    n_subplots = len(domains)
    fig, axes = plt.subplots(nrows=1, ncols=n_subplots, 
                             sharey=True, figsize=(7, 3.5), 
                             dpi=200)  # width, height

    graph = dict(zip(domains, axes))
    plots = list(map(lambda domain: plot_function(domain, graph[domain], 
                     nm2domain), graph))
    fig.tight_layout()
    fig.subplots_adjust(wspace=0)
    plt.savefig(os.path.join("distr_imgs-per-domain_%s.png" % postfix))
    plt.show()



