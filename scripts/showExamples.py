#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% ---- DEPENDENCIES
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
import random
import requests

#%% ---- FUNCTIONS
# Response formatting
def refrmt_resp(x, lang, type, incl, linewidth, asterisks):
    resp = x['responses']
    # which responses to include (for now, only applicable to English)
    if lang == 'English':
        if incl == "incorrect":
            if asterisks and len(x['incorrect']) > 0:
                x['incorrect'] = {key + '*': value for key, value in x['incorrect'].items()}
            resp.update(x['incorrect'])
    
    # order by count
    resp = sorted(resp.items(), key=lambda item: (-int(item[1]) if isinstance(item[1], int) else item[1]))
    
    #calculate values (count vs. percent)
    if type == "count":
        values = [f"({y[1]})" for y in resp]
    elif type == "pct":
        total = sum(y[1] for y in resp)
        values = [f"({round(y[1] / total * 100)})" for y in resp]
    
    #combine to one string
    y = ""
    line_length = 0
    for i, (name, value) in enumerate(resp):
        # prevent lines from breaking in the middle of a word
        element_length = len(name) + 1 + len(values[i]) + 2  # length of name + space + length of value + 2 (for comma and space)
        # add newline if adding next element would exceed linewidth
        if line_length + element_length > linewidth and i > 0:
            y += '\n'
            line_length = 0
        y += f"{name} {values[i]}, "
        line_length += element_length
    
    # Remove the comma and space of last annotation
    y = y.rstrip(", ")
    # split into lines
    lines = y.split('\n')
    
    # only keep 2 lines as maximum per response and add '...' if there are more lines
    if len(lines) > 2:
        lines[1] += ' ...'
        lines = lines[0:2]
    
    # combine lines again
    y = '\n'.join(lines)
    
    # return string with lines combined
    return y

# Open image from URL
def read_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise Exception(f"Failed to fetch image from URL: {url}")

# Annotate image
def annotate_image(x, lang, type="count", incl="correct", asterisks=True, linewidth=35, txtsize=40, nCols=3):
    # format string of responses
    txt = refrmt_resp(x, lang, type, incl, linewidth, asterisks)
    # read image
    img = read_image_from_url(x['link_mn']) # open image from link
    # create canvas
    canvas = Image.new("RGB", (690, 530 + txtsize*4), "white")
    # calculate coordinates for pasting the image centered on the canvas
    x_offset = (canvas.width - img.width) // 2
    # paste the image into the center of the canvas
    canvas.paste(img, (x_offset, 20))
    draw = ImageDraw.Draw(canvas)
    
    # add font (especialy for examples of Chinese MN) 
    font = ImageFont.truetype("fonts/NotoSansSC-Medium.ttf", txtsize)

    # calculate dimensions of the text box
    text_bbox = draw.textbbox((0, 0), txt, font=font)
    # calculate position of the text box
    txt_x_offset = (canvas.width - text_bbox[2]) // 2
    # draw the text onto the canvas
    draw.text((txt_x_offset, 480), txt, fill="black", font=font)
    
    # return annotated image
    return canvas

# Arrange images
def arrange_images(x, lang, type="count", incl="correct", asterisks=True, nCols=3, linewidth=35, txtsize=40, add_caption=True):
    # add condition for Chinese (smaller linewidth works better)
    if lang == 'Chinese':
        linewidth = 25
        
    # annotate images
    images = []
    for img in x:
        images.append(annotate_image(img, lang, type, incl, asterisks, linewidth=linewidth, txtsize=txtsize))

    # arrange in grid (with nCols)
    num_images = len(images)
    img_width, img_height = images[0].size 
    rows = []
    for i in range(0, num_images, nCols):
        row_images = images[i:i+nCols]
        max_height = max(image.size[1] for image in row_images)
        row_images = [image.resize((img_width, max_height), resample=Image.LANCZOS) for image in row_images]
        rows.append(Image.new("RGB", (img_width * nCols, max_height), "white"))
        for j, image in enumerate(row_images):
            rows[-1].paste(image, (j * img_width, 0))

    # create canvas
    arrangement = Image.new("RGB", (img_width * nCols, max_height * len(rows)), "white")
    
    # paste annotated images arranged into rows
    for i, row in enumerate(rows):
        arrangement.paste(row, (0, i * max_height))
    
    # add caption
    if add_caption:
        caption = "Note. "
        if type == "count":
            caption += "Numbers in parentheses are counts."
        elif type == "pct":
            caption += "Numbers in parentheses are percentages."
        if incl == "incorrect":
            caption += " Includes incorrect responses"
            if asterisks:
                caption += " (marked with *)."
            else:
                caption += "."

        draw = ImageDraw.Draw(arrangement)
        
        # add font
        font = ImageFont.truetype("fonts/NotoSansSC-Medium.ttf", (txtsize - 10))
        
        # calculate dimensions of the text box
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        # calculate position of the text box
        capt_y_offset = arrangement.height - (text_bbox[1]*6)
        # draw the text onto the canvas
        draw.text((30, capt_y_offset), caption, fill="black", font=font)
    
    # return image arrangement
    return arrangement

# Intercalate elements of a list
def fix_order(lst):
    mid = len(lst) // 2
    first_half = lst[:mid]
    second_half = lst[mid:]
    result = []
    for i in range(mid):
        result.append(first_half[i])
        result.append(second_half[i])
    # if the list length is odd, add the last element from the second half
    if len(lst) % 2 == 1:
        result.append(second_half[-1])
    return result

# Arrange images from two different datasets
def arrange_images_2_datasets(dic, type="count", incl="correct", asterisks=True, nCols=2, linewidth=35, txtsize=40, add_caption=True):
    images = []
    for lang in dic:
        # add condition for Chinese (smaller linewidth works better)
        if lang == 'Chinese':
            linewidth = 25
        with open(dic[lang]['path'], 'r') as f:
            mn = json.load(f)
            idx = [next(i for i, x in enumerate(mn) if x['vg_image_id'] == img_id) for img_id in dic[lang]['ids']]
            x = [mn[i] for i in idx]
            for img in x:
                images.append(annotate_image(img, lang, type, incl, asterisks, linewidth=linewidth, txtsize=txtsize))
                    
    num_images = len(images)
    img_width, img_height = images[0].size 
    
    # intercalate images of the two langs so they appear in different columns
    images = fix_order(images)

    rows = []
    for i in range(0, num_images, nCols):
        row_images = images[i:i+nCols]
        max_height = max(image.size[1] for image in row_images)
        row_images = [image.resize((img_width, max_height), resample=Image.LANCZOS) for image in row_images]
        rows.append(Image.new("RGB", (img_width * nCols, max_height), "white"))
        for j, image in enumerate(row_images):
            rows[-1].paste(image, (j * img_width, 0))

    arrangement = Image.new("RGB", (img_width * nCols, max_height * len(rows)), "white")
    
    for i, row in enumerate(rows):
        arrangement.paste(row, (0, i * max_height))

    if add_caption:
        caption = "Note. "
        if type == "count":
            caption += "Numbers in parentheses are counts."
        elif type == "pct":
            caption += "Numbers in parentheses are percentages."
        if incl == "incorrect":
            caption += " Includes incorrect responses"
            if asterisks:
                caption += " (marked with *)."
            else:
                caption += "."

        draw = ImageDraw.Draw(arrangement)
    
        font = ImageFont.truetype("fonts/NotoSansSC-Medium.ttf", (txtsize - 10))
        
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        capt_y_offset = arrangement.height - (text_bbox[1]*6)
        draw.text((30, capt_y_offset), caption, fill="black", font=font)

    return arrangement

#%% ---- MAIN
if __name__ == "__main__":
    # define a dict with MN versions, paths, and lang codes
    datasets = {'English': {'path': '../manynames-en.json', 'code': 'en'},
                'Chinese': {'path': '../manynames-zh.json', 'code': 'zh'}}
    # iterate over versions
    for lang in datasets:
        with open(datasets[lang]['path'], 'r') as f:
            mn = json.load(f)
        
        print('\n' + lang.upper() + ': ')
        # set seed for samples
        random.seed(1)
        
        # Example 1: Percentages - Only Correct
        idx = random.sample(range(len(mn)), 6)
        images = [mn[i] for i in idx]
        arrangement = arrange_images(images, lang, type="pct", incl="correct")
        arrangement.save("examples/mn_images_example1_" + datasets[lang]['code'] + ".png")
        print('Example 1 succesfully generated.')
    
        # Example 2: Counts - Only Correct
        idx = random.sample(range(len(mn)), 6)
        images = [mn[i] for i in idx]
        arrangement = arrange_images(images, lang, type="count", incl="correct")
        arrangement.save("examples/mn_images_example2_" + datasets[lang]['code'] + ".png")
        print('Example 2 succesfully generated.')
    
        # Example 3: Counts - Including Incorrect - Only Topname "Man"/"男人"
        if lang == 'English':
            word = 'man'
            idx = random.sample([i for i, x in enumerate(mn) if x['topname'] == word], 6)
        elif lang == 'Chinese':
            word = '男人'
            idx = random.sample([i for i, x in enumerate(mn) if word in x['topname']], 6)
        images = [mn[i] for i in idx]
        arrangement = arrange_images(images, lang, type="count", incl="correct")
        arrangement.save("examples/mn_images_example3_" + datasets[lang]['code'] + ".png")
        print('Example 3 succesfully generated.')
    
        # Example 4: Figure 1 from Silberer et al 2020
        if lang == 'English':
            ids = [2327551, 2358126, 2366945, 713859, 2359569, 2393177, 2371995, 2357939, 2341844]
            idx = [next(i for i, x in enumerate(mn) if x['vg_image_id'] == img_id) for img_id in ids]
            images = [mn[i] for i in idx]
            arrangement = arrange_images(images, lang, type="count", incl="correct")
            arrangement.save("examples/mn_images_example4_" + datasets[lang]['code'] + ".png")
            print('Example 4 succesfully generated.')
    
    # Example 5: Counts - Examples in English and Chinese
    dic = {'English': {'path': 'ManyNames_EN/manynames-en.json', 'ids': [2358126, 713859, 2393177]},
           'Chinese': {'path': 'ManyNames_ZH/manynames-zh.json', 'ids': [3327, 4692, 286036]}}
    
    print('\n' + list(dic.keys())[0].upper() + ' & ' + list(dic.keys())[1].upper() + ': ')
    
    arrangement = arrange_images_2_datasets(dic, type="count", incl="correct", nCols=2, add_caption=False)
    arrangement.save("examples/mn_images_example5.png")
    print('Example 5 succesfully generated.')
