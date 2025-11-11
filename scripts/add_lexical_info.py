#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% ---- DEPENDENCIES
import ast
import os
import pandas as pd
from collections import Counter

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

#%% ---- FUNCTIONS
def main():
    # Read MN data
    lang_code = 'en'
    
    mn_path = f'https://raw.githubusercontent.com/amore-upf/manynames/refs/heads/master/manynames-{lang_code}.tsv'
    df = pd.read_table(mn_path, sep='\t')
    
    lex_path = f"https://raw.githubusercontent.com/amore-upf/manynames/refs/heads/master/other-data/lexical-info-{lang_code}.tsv"   
    lex = pd.read_table(lex_path, sep='\t').set_index('name').to_dict('index')

    # Add desired measure
    df['concreteness'] = df['responses'].apply(lambda x: create_dict(x, lex, 'concreteness'))
    df['imageability'] = df['responses'].apply(lambda x: create_dict(x, lex, 'imageability'))
    df['familiarity'] = df['responses'].apply(lambda x: create_dict(x, lex, 'familiarity'))
    df['age_of_acquisition'] = df['responses'].apply(lambda x: create_dict(x, lex, 'age_of_acquisition'))
    df['freq_en'] = df['responses'].apply(lambda x: create_dict(x, lex, 'freq_en'))
    df['log10freq_en'] = df['responses'].apply(lambda x: create_dict(x, lex, 'log10freq_en'))
    df['context_div_en'] = df['responses'].apply(lambda x: create_dict(x, lex, 'context_div_en'))
    df['n_tokens'] = df['responses'].apply(lambda x: create_dict(x, lex, 'n_tokens'))
    df['n_images'] = df['responses'].apply(lambda x: create_dict(x, lex, 'n_images'))

    # Save to TSV (if needed)
    df.to_csv('manynames-en-lex.tsv', sep='\t')

    print(df.head())

# Retrieve the desired information of each name for each row
def create_dict(responses, lex, measure):
    # Make sure the responses are treated as a dict
    r = ast.literal_eval(responses)
    
    # Inicialize an empty dict and fill it with each word and its value
    dic = {}
    [dic.update({word: lex.get(word)[measure]}) for word in r.keys()]
    
    return dic

#%% ---- MAIN
if __name__ == "__main__":
    main()
