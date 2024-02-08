Release Notes - ManyNames v2.2
==============================

In version 2.2, we verified the singletons that were not automatically accepted in v. 2.1.
To achieve this, we started from re-generating v2.1, with slight modifications to the cleaning rules appled; then, we applied two automatic filtering steps to the singletons, to identify some of the incorrect ones; finally, we annotated the remaining singletons on AMT, asking annotators whether the singletons correctly referred to the object in the bounding box.

After the data collection, we reorganized the CSV so that the answers classified as *singletons* (i.e. included in column *singletons*) were reclassified as either correct (column *responses*), if at least 2 annotators marked them as correct, or incorrect (column *incorrect*) otherwise.

Each step is described in more detail below. 

## Re-generate MNv2.1

We repeated the process of generating MNv2.1, following the same cleaning rules illustrated [here](https://github.com/amore-upf/manynames/blob/master/release_notes_v2.1.md), but improving some aspects of them; e.g., we made sure to correct spelling mistakes in the singletons column as well (because of a bug, this was not done properly in the previous MNv2.1).
After generating a new temporary MNv2.1, we verified the appropriatness of the singletons present in this file with human annotators.


## Verify singletons

**Problem**: in ManyNames v.2.1.1 we added some singleton responses (those that according to WordNet were were synonyms or hypernyms of the topname) to the other correct responses. The remaining singletons were left in the ***singletons*** column, which potentially excluded viable object names.

**Solution**: manual verification procedure. AMT workers were asked to identify singletons that could be plausible names for the object in the relevant images. This process encompassed 1834 batches launched on AMT, annotated by 3 people each and summing up to 21,149 images. Singletons chosen by 2+ workers were included in the ***responses*** column, whereas if they were chosen by less than 1 they were shifted to the ***incorrect*** column. The ***singletons*** column has been removed in v2.2.

**Affected columns**: responses, incorrect, singletons

### Before verification 
Before collecting data for the singleton verification, we filtered out singletons that we could safely identify as incorrect without need of manual annotation. This involved two steps:

1. **Filtering of multi-word singletons**: Some singletons consisted of more than one word. Some multi-word expressions, such as "tennis player", are very lexicalized, meaning that the individual word components co-occur in language so often that the multi-word expression can be considered a single name. We considered these expressions valid naming annotations for ManyNames, and they were included in the verification process. We identified valid multi-word expressions through the database in Muraki, E. J., Abdalla, S., Brysbaert, M., & Pexman, P. M. (2022). Concreteness ratings for 62 thousand English multiword expressions. https://doi.org/10.31234/osf.io/m397u. Multi-word expressions appearing in this dataset were kept, and the rest were automatically discarded.
  
2. **Filtering of incorrect parts-of-speech**: We PoS-tagged the singletons words with StanfordCoreNLP PoS tagger, keeping all PoS but but RB (adverb), IN (preposition/subordinating conjunction), and FW (foreign word), so as to automatically filter out words that are likely not names.

**Affected columns**: incorrect, singletons

## Generate MNv2.2

We generated a new version of ManyNames file, where the singletons (originally in column *singletons*) were moved to column *responses*, if 2+ subjects selected them as correct, and to column *incorrect*, otherwise. We also updated the following columns to account for the newly included data:

* total_responses (sum of correct responses)
* perc_top percentage (name agreement in %)
* H (name agreement score)
* N (number of response types)

**Affected columns**: singletons (removed), responses, incorrect, the ones listed just above.

The final version of the English ManyNames file (v2.2) corresponds to file `manynames-en.tsv/.json`, and it contains the following columns:

|Column     |Type    |Description   |
|:--------- |:------ |:------------ |
|*vg_image_id*    |	int  | The VG id of the image |
|*vg_object_id*  |	int     |	The VG id of the object     |
|*link_mn*   |	str  |  The url to the image, with the object marked    |
|*link_vg*              |	str  |	The url to the image in VG |
|*vg_obj_name*       |	str  |	The VG name of the object |
|*vg_domain*        |	str  |	The MN domain of the VG name, which may be a superset of its WN category (vg_cat).  |
|*vg_synset* |  str |  The WN synset of the object, provided by VG  |
|*mn_bbox_xywh* | list |	The coordinates of the object in the ManyNames version of the image: "[left x, bottom y, width, height]"; y=0 is at the top of the image.   |
|*topname*   | str  |	The most frequent name of the object in the largest cluster |
|*responses* |	dict |	Correct responses and their counts  |
|*incorrect* | dict | Incorrect responses and their counts|
|*total_responses* | int | Sum count of correct responses|
|*perc_top* | float | The relative frequency of the topname (among correct responses)|
|*H* | float | The H agreement measure from Snodgrass and Vanderwart (1980)|
|*N* | int | The number of types in the MN responses|
|*domain*  | str  | The MN domain of the object |
|*split* | str | Use of the image in training vs. test vs. validation in Silberer, Zarrieß, Westera, & Boleda, 2020|


The file `additional-info-manynames-en.tsv` includes additional information about the data in v.2.2. It contains the following columns:

|Column     |Type  |Description   |
|:----------|:-----|:-------------|
|*vg_image_id*|int |The VG id of the image|
|*link_mn*  |str   |The url to the image, with the object marked|
|*vg_same_object*|dict|Same object ratings for the vg_object_name|
|*vg_adequacy_mean*|str|Mean adequacy rating for the vg_object_name|
|*vg_inadequacy_type*|dict|Rated inadequacy type for the vg_object_name|
|*vg_image_name*|str|The name of the VG image|
|*vg_cat*|str|The WN hypernym of the VG synset, corresponds roughly to one of the 7 MN domains|
|*clusters* |dict  |Response clusters and total count per cluster|
|*adequacy_mean*|dict|Mean adequacy ratings for MN responses|
|*inadequacy_type*|dict|Rated inadequacy rating for MN responses|
|*same_object*|dicts|Mean same-object ratings for response pairs|

## Update and add Chinese version of ManyNames
We added the Chinese version of ManyNames to this release after complementing its [last version](https://github.com/flyingpiggy1214/ManyNames_ZH) by adding additional information about the data included.

***Affected columns***: vg_image_id (added), vg_object_id (added), vg_obj_name (added), vg_domain (added), vg_synset (added), mn_bbox_xywh (added), response (renamed to *responses*), perc_top (added), total_respondes (added)


