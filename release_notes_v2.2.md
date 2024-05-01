Release Notes - ManyNames v2.2
==============================

In version 2.2, we 

* Verified the singletons (names that were produced only once for a given object).

* Added names in Mandarin Chinese for a subset of the data.

* Added lexical information for the names in the English and Mandarin Chinese data.

* Reorganized the data and updated some scripts so as to facilitate use of ManyNames.

## Singleton verification

**Problem**: while in ManyNames v.2.1.1 we added some singleton responses (those that according to WordNet were synonyms or hypernyms of the topname) to the other correct responses, the remaining singletons were left in the *singletons* column, which potentially excluded viable object names. (*Note*: singletons were not included in the manual cleaning procedure that led from v. 1 to v. 2 because of time and budget constraints.)

**Solution**: classification of items in *singleton* as correct or incorrect via automatic filtering followed by manual verification, as explained next.

### Before verification: re-generating MNv2.1

Since we spotted some issues in MNv2.1, we first repeated the procedure that went from MNv2 to MNv2.1 with some improvements. The MNv2 => MNv2.1 process addressed some problematic issues regarding the definition of top names and domains and well as the treatment of spelling variants; adjusted the treatment of singleton responses; and simplified the structure of the data columns detailing the verification data to ease accessibility (full description of the process [here](https://github.com/amore-upf/manynames/blob/master/release_notes_v2.1.md)). The improvements we made in this release are the following: ***, but improving some aspects of them; e.g., we made sure to correct spelling mistakes in the singletons column as well (because of a bug, this was not done properly in the previous MNv2.1). ==> @PAOLA list all the improvements*** The singletons in the resulting data were subject to the following processing.

### Automatic filtering
We filtered out singletons that we could safely identify as incorrect without need of manual annotation. ***@PAOLA, did we put the incorrect ones in the "incorrect" column?***This involved two steps:

1. **Filtering of multi-word singletons**: Some singletons consisted of more than one word. Some multi-word expressions, such as "tennis player", are lexicalized, meaning that the individual word components co-occur in language so often that the multi-word expression can be considered a single name; others, like "cute red dress", are not lexicalized. With singletons, we follow the same procedure that we followed with the remaining names: multi-word expressions appearing in the dataset of Muraki, E. J., Abdalla, S., Brysbaert, M., & Pexman, P. M. (2022). [Concreteness ratings for 62 thousand English multiword expressions](https://doi.org/10.31234/osf.io/m397u) were kept for annotation, and the rest were automatically discarded.

2. **Filtering of incorrect parts-of-speech**: We PoS-tagged the singletons with StanfordCoreNLP, and kept all PoS but but RB (adverb), IN (preposition/subordinating conjunction), and FW (foreign word), so as to automatically filter out words that are likely not names. ***@PAOLA, did we filter out expressions containing any of these, or consisting only of these? if it is "containing", why didn't they get removed in step 1?***

**Affected columns**: incorrect, singletons

### Manual verification

AMT workers were asked whether singletons correctly referred to the relevant MN objects.
***@PAOLA DOUBLE-CHECK THE FOLLOWING (I CHANGED SOME EXPLANATIONS):*** This process encompassed 21,149 images, organized into 1834 batches launched on AMT, and annotated by 3 people each. More information about the annotation process is included in the Appendix below. ***@PAOLA please put the exact instructions that were given to the turkers in the appendix below***

### Generating English MNv2.2

After this procedure, we generated a new version of the English portion of ManyNames, where the singletons (originally in column *singletons*) were moved to column *responses*, if 2+ subjects selected them as correct, and to column *incorrect*, otherwise. We also updated the following columns to account for the newly included data:

* N
* total_responses
* perc_top
* H

**Affected columns**: singletons (removed, as it is no longer needed), responses, incorrect, the ones listed just above.

The final version of the English ManyNames (v2.2) is in files `manynames-en.tsv` / `manynames-en.json`. 

## Mandarin Chinese ManyNames

We added the Mandarin Chinese version of ManyNames to this release, by unifying the data in the [initial release](https://github.com/flyingpiggy1214/ManyNames_ZH) with the information in MN. These data consist of approximately 20 name annotations for 1319 objects in images selected from ManyNames. It is found in files `manynames-zh.tsv` / `manynames-zh.json`

***Affected columns***: vg_image_id (added), vg_object_id (added), vg_obj_name (added), vg_domain (added), vg_synset (added), mn_bbox_xywh (added), response (renamed to *responses*), perc_top (added), total_respondes (added)

## Lexical information

***@PAOLA add brief summary for this***

## Data reorganization, changes to scripts

* We reorganized the information in previous versions by moving some of the columns to file `other-data/additional-info-en.tsv` and reordering the columns (see the main README.md for which information is where). This was done to facilitate use.

* ***@PAOLA, what changes did we make to the scripts? (brief summary)***

## APPENDIX: Procedure for the manual verification
***@PAOLA to complete.***
