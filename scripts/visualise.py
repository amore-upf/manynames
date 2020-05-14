
from skimage import io
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.ion()

import manynames as mn

def show_objects(img_name, bbox, objname, img_dir="../images", block_display=True):
    im = io.imread(os.path.join(img_dir, '%s'%img_name))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(im, aspect='equal')

    if bbox[0] == 0:
        bbox[0] = 1
    if bbox[1] == 0:
        bbox[1] = 1
        
    plt.gca().add_patch(
        plt.Rectangle((bbox[0], bbox[1]),
                        bbox[2], bbox[3], fill=False,
                        edgecolor='red', linewidth=2, alpha=0.5)
            )
    plt.gca().text(bbox[0], bbox[1] - 2,
                '%s' % (objname),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=10, color='white')
        
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show(block=block_display)

        
if __name__=="__main__":
    imagedata = mn.load_images("../images.tsv")
    manynames = mn.load_cleaned_results("../manynames_v1.0.tsv")
    
    for image_id in [2417690, 2417892, 2388484, 2417993, 2388471, 65, 413, 2417452]:
        mn_item = manynames[manynames["vg_image_id"]==image_id]
        responses = mn_item["responses"].values[0]
        mn_objnames = "MN: "+" / ".join(responses.keys())
            
        item = imagedata[imagedata["vg_image_id"]==image_id]
        bbox = item["bbox_xywh"].values[0]
        vg_objname = "VG: "+item["vg_obj_name"].values[0]
        image_name = item["vg_image_name"].values[0]
        show_objects(image_name, 
                    bbox, 
                    mn_objnames + "   (%s)" % vg_objname, 
                    img_dir="../images/")
    
                
                
    
