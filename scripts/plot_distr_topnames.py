#!/usr/bin/env python
# coding: utf-8

#%% ---- DEPENDENCIES
import ast
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import manynames as mn

#%% ---- FUNCTIONS TO RECREATE DISTRIBUTION FIGURE
def statistics_mn_topnames(df, domain_key, lang, print_stats=False):
    """
    VG image distribution, MN entry-level distribution, per domain
    """
    # count frequency of vg object names
    obj_name_df = df[["topname", domain_key]]
    
    # in case the MN-ZH is being plotted (topname in MN-ZH is a list)
    if lang == 'Chinese':
        # create a copy of the DataFrame to avoid SettingWithCopyWarning
        obj_name_df_copy = obj_name_df.copy()
        # modify the 'topname' column in the copied DataFrame so each element is treated as a list
        obj_name_df_copy.loc[:, 'topname'] = [ast.literal_eval(x) for x in obj_name_df_copy['topname']]
        # explode the lists in the 'topname' column and replicate 'domain' values
        obj_name_df = obj_name_df_copy.explode('topname').reset_index(drop=True)
        # # (optional) save df
        # obj_name_df.to_csv('topnames_per_domain_zh.csv')
    
    obj_name_df = pd.DataFrame(obj_name_df.groupby(by=["topname", domain_key])["topname"].count())
    obj_name_df.rename(columns={"topname": "mn_count"}, inplace=True)
    obj_name_df.reset_index(level=[1], inplace=True)
    obj_name_df["topname"] = obj_name_df.index
    obj_name_df.set_index(pd.Index(list(range(len(obj_name_df)))), inplace=True)
    obj_name_df.sort_values(by=[domain_key, "mn_count"], ascending=False, inplace=True)
    
    print_df = dict()
    for cat in set(df.vg_domain):
        top_names = obj_name_df[obj_name_df[domain_key]==cat].head(10)["topname"].tolist()
        counts_top_names = obj_name_df[obj_name_df[domain_key]==cat].head(10)["mn_count"].tolist()
        print_df[cat] = ["%s (%d)" % (top_names[idx], round(counts_top_names[idx])) for idx in range(len(top_names))]
        
    print_df = pd.DataFrame.from_dict(print_df)
    if print_stats:
        print("\n\n**Top 10 MN names for each MN/VG domain**")
        print(print_df.to_latex())
    
    return obj_name_df, print_df


def plot_function(domain, ax, nm2domain, domain_gdf, domains, lang, text_fontsize=8):
    """
    A bit hacky function to create a stacked bar plot for an individual MN domain.
    """
    domain_gdf_numeric = domain_gdf.apply(pd.to_numeric, errors='coerce')
    num_1domain = domain_gdf_numeric.loc[domain][domain_gdf_numeric.loc[domain] > 0].sort_values(ascending=False)

    a = num_1domain.unstack(fill_value=0)
    
    # set the default font family to a font that supports Chinese characters
    plt.rcParams['font.family'] = ['Arial Unicode MS']
    
    plot_singledomain = a.plot(ax=ax, kind="bar", stacked=True, legend=False, alpha=0.65, width=.6)
    # hide x ticks ("vg_count")
    plot_singledomain.xaxis.set_major_formatter(plt.NullFormatter())
    plot_singledomain.set_xlabel(domain.replace("_", "/"), fontsize=(text_fontsize+1))
    plot_singledomain.set_ylabel("Cumulative sum of images / name", fontsize=(text_fontsize+2))
    
    # label some subbars with their names
    ypositions = num_1domain.cumsum()
    idx2show = [("c",0)]
    for idx in range(1, len(ypositions)):
        # set different filtering values for each language (figures vary considerably)
        if lang == 'English':
            if -ypositions[idx-1]+ypositions[idx] < 90:
                break
        elif lang == 'Chinese':
            if -ypositions[idx-1]+ypositions[idx] < 8:
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
        # set a specific format for y-axis scale depending on the language
        if lang == 'English':
            if domain!="animals_plants":
                ax.spines['left'].set_visible(False)
            else:
                mkfunc = lambda x, pos: '%1.0fK' % (x / 1000)
                mkformatter = plt.FuncFormatter(mkfunc)
                plot_singledomain.yaxis.set_major_formatter(mkformatter)
                plot_singledomain.tick_params(labelsize=text_fontsize-1)
            if domain!="vehicles":
                ax.spines['right'].set_visible(False)
        elif lang == 'Chinese':
            if domain!="animals_plants":
                ax.spines['left'].set_visible(False)
            else:
                mkfunc = lambda x, pos: '%.1f' % (x / 100)
                mkformatter = plt.FuncFormatter(mkfunc)
                plot_singledomain.yaxis.set_major_formatter(mkformatter)
                plot_singledomain.tick_params(labelsize=text_fontsize-1)
            if domain!="vehicles":
                ax.spines['right'].set_visible(False)
    return plot_singledomain

#%% ---- MAIN
if __name__ == '__main__':
    #make sure new path exists
    new_dir = 'imgs/'
    os.makedirs(new_dir, exist_ok=True)

    #dict with MN versions, paths, and lang codes
    datasets = {'English': {'path': '../manynames-en.tsv', 'code': 'en'},
                'Chinese': {'path': '../manynames-zh.tsv', 'code': 'zh'}
                }
    for lang in datasets:
        #%%% ----- CHECK ARGUMENTS
        #setup argument parser
        arg_parser = argparse.ArgumentParser(
            description = '''plots the top name distribution (reproducing Figure 3 
                            in Silberer, Zarrieß, & Boleda, 2020)''')
        
        #add required arguments
        arg_parser.add_argument('-mnfile', type=str, 
                          	    help='path to the TSV file containing the ManyNames data',
                                default=datasets[lang]['path'])
        
        #check provided arguments
        args = arg_parser.parse_args()
        
        #set values
        fn = args.mnfile

        #%%% ----- PROCESSING
        manynames_df = mn.load_manynames(fn)

        if lang == 'English':
            # add VG columns
            additional_df = pd.read_csv('../other-data/additional-info-en.tsv', sep='\t')[['vg_object_id', 'vg_obj_name', 'vg_domain']]
            manynames_df = pd.merge(manynames_df, additional_df, on='vg_object_id')
        
        nm2domain = dict(zip(manynames_df["vg_obj_name"], manynames_df["vg_domain"]))
        
        domain_key = "domain" #"vg_domain"
        obj_name_df, print_df = statistics_mn_topnames(manynames_df, domain_key, lang)

        domain_groups = obj_name_df.groupby([domain_key]).apply(lambda x: (x.groupby('topname')
                                            .sum().sort_values('mn_count', ascending=False)))
        domain_gdf = domain_groups.unstack(fill_value=0)
        domains = [domain[0] for domain in domain_gdf.iterrows()]

        n_subplots = len(domains)
        fig, axes = plt.subplots(nrows=1, ncols=n_subplots, 
                                sharey=True, figsize=(7.5, 3.5), 
                                dpi=300)  # width, height
        
        # iterate over subplots to hide y-axis ticks
        for i, ax in enumerate(axes):
            if i != 0:
                ax.tick_params(left=False)
                
        # (optional) set a title
        plt.title(f'Top name distribution in {lang}', x=-2.5, y=1.0, fontname="Verdana", weight='bold')
        
        graph = dict(zip(domains, axes))
        plots = list(map(lambda domain: plot_function(domain, graph[domain], 
                        nm2domain, domain_gdf, domains, lang), graph))
        fig.tight_layout()
        fig.subplots_adjust(wspace=0)
        
        # save image
        plt.savefig(f"{new_dir}topname_distribution_{datasets[lang]['code']}.png", dpi=300)
        
        plt.show()



