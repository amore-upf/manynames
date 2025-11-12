# Release Notes
(Note: This file contains the release notes for all versions, in reverse chronological order.)

## ManyNames v2.3

The following changes have been introduced in version 2.3:

* Singletons (names that were produced only once for a given object) have been re-evaluated for quality using both manual and automatic procedures.

* The anonymized IDs of people who originally produced each name are now available for 3/4 of the English version of ManyNames.

* Lexical information has been enhanced. For both English and Mandarin Chinese, frequency information and context diversity have been added, and some source databases have been updated to achieve broader coverage.

* WordNet synsets and informativity ratings have been added for English, together with typicality ratings for each pair name-image.

Each step is described in more detail below. 

### Singleton re-evaluation

**Problem**: Some singletons that were annotated as 'correct' were not referring to the object in the bounding box (i.e. 'shirt' for a picture of a woman wearing a shirt.)

**Solution**: We devised two solutions. 

One consisted in manually annotating a sample of 200 images and testing the effects of changing the requirements for accepting an annotation. It was then decided to increase the requirements related to quality items, as it had a positive effect on erasing true negatives and especially false positives. Around 150 new annotations were collected according to the new criteria, and ManyNames was re-generated including these results.

The other solution was an automatic filter using WordNet, aimed at removing singletons marked as 'correct' that are out of domain (like 'shirt', which refers to clothing, for an image of domain 'person'). We first added a WordNet synset for each name (procedure explained below). The synset of a given singleton was compared to the synset of the top name of the corresponding image. The singleton was kept if it shares a common hypernym with the synset of the top name within a reasonable depth in the WordNet hierarchy (we defined a set of synset nodes that were too generic to be considered a good indicator of belonging to the same domain, e.g. 'entity.n.01', 'abstraction.n.06', 'instrumentality.n.03', etc.). Else, it was moved to column 'incorrect'.

**Affected columns**: responses, incorrect, singletons

### Subject information
We have included a version of the MN English dataset where each row corresponds to a single answer (file *subject-ids-en.tsv*), and includes the anonymized ID of the person that gave that answer (if available). In order to do so, earlier information about the data collection process was retrieved so as to match each answer in the current ManyNames dataset with an ID. However, some annotations were missing, so there are only up to 27 IDs available per image.
For Chinese, this information is not available, as it was not collected.

### New lexical and pair-related (name and image) information
We have added the following columns for each ManyNames dataset:

- `log10freq_{language}` (English, Mandarin Chinese): Logarithmic corpus frequency of each name based on log10, retrieved from column `Lg10WF` of [SUBTLEXus](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus) and column `log10W` of [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch).
- `context_div_{language}` (English, Mandarin Chinese): Context diversity ratings of each name, retrieved from column `CDcount` of [SUBTLEXus](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus) and column `W-CD` of [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch).
- `n_tokens` (English, Mandarin Chinese): frequency of each name in the 'correct' column in ManyNames (tokens; each subject production of a name counts once).
- `n_images` (English, Mandarin Chinese): frequency of each name per image in ManyNames (types per image; each name counts once per image regardless of the number of times produced).
- `synsets` (English only): WordNet synset of the name. WordNet is a large lexical database consisting of interlinked synsets, or sets of synonyms, that can function as sense IDs. For nouns, these synsets form a hierarchy. In order to disambiguate among different senses of a given name (e.g. "pitcher" can refer to a baseball player or a jug), we identified a set of synsets for each value in the `domain` column (e.g. 'clothing.n.01' for domain 'clothing', 'animal.n.01' and 'plant.n.02' for domain 'animals_plants', etc.); we picked as synset for the name-domain pair the first synset of the name that is a hyponym of the domain synset.
- `informativeness` (English only): [Information content](https://wn.readthedocs.io/en/latest/api/wn.ic.html) rating, provided by WordNet, per available synset.
- `most_informative_synset_image` (English only): If any, the synset with highest informativity rating per image.
- `typicality` (English only): Image-text similarity score for each pair of name and object image, calculated using [BLIP2 (Li, Li, Savarese & Hoi, 2023)](https://arxiv.org/abs/2301.12597)

Also, we have changed the source of some lexical measurements, aiming to achieve a better coverage. These are the new sources employed:
- English:
    - Concreteness: [Brysbaert et al. (2014)](https://doi.org/10.3758/s13428-013-0403-5)
    - Familiarity: [Glasgow Norms (Scott et al., 2019)](https://doi.org/10.3758/s13428-013-0403-5)
    - Imageability: [Glasgow Norms (Scott et al., 2019)](https://doi.org/10.3758/s13428-013-0403-5)
- Mandarin Chinese: 
    - Concreteness: [Chan & Tse (2024)](https://doi.org/10.3758/s13428-024-02437-w)
    - Familiarity: [Su et al. (2023)](https://doi.org/10.3758/s13428-022-01878-5)
    - Imageability: [Chan & Tse (2024)](https://doi.org/10.3758/s13428-024-02437-w)
    - Age of acquisition: [Xu et al. (2021)](https://doi.org/10.3758/s13428-020-01455-8)

### Data reorganization
* File `additional-info.tsv` was renamed `additional-info-en.tsv`. Scripts using this file have also been modified.
* Columns *vg_domain* and *vg_obj_name* have been moved from `additional_info-en.tsv`to `manynames-en.tsv`.
* Column *vg_image_name* of `additional_info-en.tsv` has been renamed to `filename`.
* Script `add_lexical_info.py` has been added to subfolder *scripts/*.
* Column `mn_bbox_xywh` was renamed to `vg_bbox_xywh`, as it corresponds to the object coordinates only in the Visual Genome image.


&nbsp;
&nbsp;
&nbsp;

## ManyNames v2.2

The following changes have been introduced in version 2.2:

* Singletons (names that were produced only once for a given object) have been manually checked and added to columns *responses* or *incorrect* as appropriate.

* Names in Mandarin Chinese for a subset of the data have been added.

* Lexical information for the names in the English and Mandarin Chinese data has been added.

* Data has been reorganized and some scripts have been updated so as to facilitate use of ManyNames.

### Singleton verification

**Problem**: while in ManyNames v.2.1.1 we added some singleton responses (those that according to WordNet were synonyms or hypernyms of the topname) to the other correct responses, the remaining singletons were left in the *singletons* column, which potentially excluded viable object names. (*Note*: singletons were not included in the manual cleaning procedure that led from v. 1 to v. 2 because of time and budget constraints.)

**Solution**: classification of items in *singleton* as correct or incorrect via automatic filtering followed by manual verification, as explained next.

#### Before verification: re-generating ManyNames v2.1

Since we spotted some issues in ManyNames v2.1, we first repeated the procedure that went from ManyNames v2 to ManyNames v2.1 with some improvements. The ManyNames v2 => ManyNames v2.1 process addressed some problematic issues regarding the definition of top names and domains and well as the treatment of spelling variants; adjusted the treatment of singleton responses; and simplified the structure of the data columns detailing the verification data to ease accessibility (full description of the process [here](#manynames-v210)). In the current release, we make sure we correct spelling mistakes in the singletons column as well (because of a bug, this was not done properly in the previous ManyNames v2.1). The singletons in the resulting data were subject to the following processing.

#### Automatic filtering
We filtered out singletons that we could safely identify as incorrect without need of manual annotation, and added them to column *incorrect*. This involved two steps:

1. **Filtering of multi-word singletons**: Some singletons consisted of more than one word. Some multi-word expressions, such as "tennis player", are lexicalized, meaning that the individual word components co-occur in language so often that the multi-word expression can be considered a single name; others, like "cute red dress", are not lexicalized. With singletons, we follow the same procedure that we followed with the remaining names: multi-word expressions appearing in the dataset of Muraki, E. J., Abdalla, S., Brysbaert, M., & Pexman, P. M. (2022). [Concreteness ratings for 62 thousand English multiword expressions](https://doi.org/10.31234/osf.io/m397u) were kept for annotation, and the rest were automatically discarded.

2. **Filtering by part-of-speech**: We PoS-tagged the remaining singletons with the StanfordCoreNLP toolkit. Responses tagged as RB (adverb), IN (preposition/subordinating conjunction), and FW (foreign word) were identified as incorrect.

**Affected columns**: incorrect, singletons

#### Manual verification

AMT workers were asked whether singletons correctly referred to the relevant ManyNames objects. This process encompassed 21,149 images, organized into 1834 batches launched on AMT, and annotated by 3 people each. The instructions that were given to the workers are available [here](https://github.com/amore-upf/manynames/blob/master/other-data/instructions_for_singleton_verification.pdf), which contains.

### Resulting version of ManyNames (English)

After the process above, we automatically generated a new version of the English portion of ManyNames, where the singletons (originally in column *singletons*) were moved to column *responses*, if 2+ subjects selected them as correct, and to column *incorrect*, otherwise. We also updated the following columns to account for the newly included data:

* N
* total_responses
* perc_top
* H

**Affected columns**: singletons (removed, as it is no longer needed), responses, incorrect, the ones listed just above.

The final version of the English ManyNames (v2.2) is in files `manynames-en.tsv` / `manynames-en.json`. 

### Data in Mandarin Chinese

We added the Mandarin Chinese version of ManyNames to this release, by unifying the data in the [initial release](https://github.com/flyingpiggy1214/ManyNames_ZH) of these data with the information in ManyNames. These data consist of approximately 20 name annotations for 1319 objects in images selected from ManyNames. It is found in files `manynames-zh.tsv` / `manynames-zh.json`

***Affected columns***: we added columns vg_image_id, vg_object_id, vg_obj_name, vg_domain, vg_synset, mn_bbox_xywh, response (renamed to *responses*), perc_top, total_responses

### Lexical information

We have added files with lexical information for each name in the ManyNames datasets (both English and Mandarin Chinese). The following measurements are included:
- concreteness
- familiarity
- imageability
- age of acquisition
- frequency per million tokens

This information has been retrieved from several datasets listed [here](https://github.com/amore-upf/manynames/blob/master/other-data/README.md).

### Data reorganization, changes to scripts

* We reorganized the information in previous versions by moving some of the columns to file `other-data/additional-info.tsv` and reordering the columns (see the main README.md for which information is where). This was done to facilitate use.

* In the English version, we substituted missing values in column `split`, which corresponds to the use of the image in training vs. test vs. validation sets of ManyNames (v. [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/)), by values *test* and *val*, distributed randomly and equally (we do not know why there were missing values).

* We converted script `showExamples.r` to Python, resulting in script `showExamples.py`.

* We modified scripts `agreement_table.py`, `plot_distr_topnames.py`, and `showExamples.py` so they create results for the datasets in both English and Mandarin Chinese.

* We modified scripts `agreement_table.py`, `create_MN_images.py`, `plot_distr_topnames.py`, `showExamples.py`, and `visualise.py` so they retrieve needed columns from `other-data/additional-info.tsv`.

* In script `agreement_table.py`, we deleted columns *top=VG* and *%VG*.

* In script `plot_distr_topnames.py`, we hid the y-axis spine and ticks and added a title to the plot.

&nbsp;
&nbsp;
&nbsp;

## ManyNames v2.1.1
Added bounding box coordinates for ManyNames image versions. Updated ManyNames-image links to new domain: [manynames.upf.edu](manynames.upf.edu).
Added scripts for recreating ManyNames images from VG-source and downloading subsets of ManyNames images.

&nbsp;
&nbsp;
&nbsp;

## ManyNames v2.1.0
In version 2.1 we addressed some potentially problematic issues regarding the definition of topnames and domains and well as the treatment of spelling variants. We also adjusted the treatment of singleton responses so that singleton responses which are likely to be correct names for the target object are no longer excluded from name agreement calculation. Finally, we simplified the structure of the data columns detailing the verification data to ease accessibility. Each issue is described in more detail below.

### Definition of topnames and incorrect responses
**Problem**: In ManyNames v2.0 it could happen that a cluster of words referring to the same object *overall* had a higher number of selections than the most frequent name alone. For instance, in a case like: {*giraffe*: 12, *woman*: 10, *person*: 9}, the cluster *woman-person* has a higher number of selections than the cluster *giraffe*.

**Solution**: In these cases, the *topname* is defined as the most frequent name within the largest name cluster (instead of the most frequent name overall). In addition names belonging to the largest cluster are coded as correct (instead of names belonging to the cluster of the most frequent name). In the example above, the topname was changed to *woman* (instead of *giraffe*) and *woman*, *girl*, and *person* are now counted as correct (and *giraffe* as incorrect).

**Affected columns**: clusters (new), topname, responses, incorrect

### Update/correct domains

**Problem**: Some domain definitions may have to be adjusted after updating the topname (see above). In addition, some domain definitions were incorrect or inconsistent across the data set (i.e., images with the same topname could have different domain definitions).

**Solution**: To resolve inconsistencies we now define the domain for each image as the domain in which the respective topname appears most frequently in. In case of a tie, we manually selected the most appropriate domain. For the topname *mouse*, the domain was generally changed from *animals_plants* to *home* (we only have images of the electronic device).

Please note, that for some images/names the most appropriate domain label is not unequivocally clear.

* Some names could be placed into multiple ManyNames domains. This concerns cases like *mirror* (home, vehicles -- in case of a motorcycle mirror), *clock* (home, buildings -- in case of a clock tower), and *banana* (animals_plants, food). For these cases, we just applied the frequency rule.

* The names *sand*, *snow*, *field*, *water*, *grass* were lacking a corresponding ManyNames domain. In order to avoid adding a new (and very sparse) domain label, these names were included into the domain *animals_plants* (which therefore may be more broadly understood as *natural world*).

**Affected columns**: domain

### Spelling variants
**Problem**: Different spellings of noun-noun compounds were so far counted as different names (e.g., 'tea pot' vs 'teapot').

**Solution**: When responses differed only in one white space, the response counts were summed under the most frequent spelling variant.

**Affected columns**: responses

### Treatment of singleton responses
**Problem**: The strict exclusion of all singleton responses can remove viable object names.

**Solution**: Singletons are now treated as a correct response, if they are either *synonyms* or *hypernyms* of the topname, based on WordNet. Accepted singletons are now listed together with the other correct responses in the ***responses*** column, and they are erased from the ***singletons*** column. Non-accepted ones are left in the ***singletons*** column.

**Affected columns**: responses, singletons (overall 3038 singletons are now treated as correct responses).

### Update summary columns
Based on the updated topname and response variables, we have also updated the following columns:

* total_responses (sum of correct responses)
* perc_top percentage (name agreement in %)
* H (name agreement score)
* N (number of response types)

### Update verification data columns

The verification data (same object and adequacy ratings) are now stored for all names (correct and incorrect) in the same columns (see below). The column *incorrect* now only includes the incorrect names with their response counts but no longer their verification data.

* **same_object**: it now contains, for all the naming annotations of each data point (correct and incorrect names), their reciprocal *same object* score. Singletons - which are included in the responses, but for which we do not have a *same object* score - are labelled with “NA”.

* **inadequacy_type**: it now contains, for all the naming annotations of each data point (correct and incorrect names), the corresponding *inadequacy type* information. Singletons - which are included in the responses, but for which we do not have any *inadequacy type* annotations - are labelled with “NA”. Note that, differently, a *inadequacy type* "None", means that annotators have marked that name as totally adequate for the corresponding image.

* **adequacy_mean**: it now contains, for all the naming annotations of each data point (correct and incorrect names), the corresponding *adequacy mean* information. Singletons - which are included in the responses, but for which we do not have any *adequacy mean* annotations - are labelled with “NA”.

&nbsp;
&nbsp;
&nbsp;

## ManyNames v2.0.0
Integration of name verification data (for details, see [Silberer, Zarrieß, Westera, & Boleda, 2020](https://github.com/amore-upf/manynames/releases#:~:text=Silberer%2C%20Zarrie%C3%9F%2C%20Westera%2C%20%26%20Boleda%2C%20202))

&nbsp;
&nbsp;
&nbsp;

## ManyNames v1.0.0
Initial release (for details, see [Silberer, Zarrieß, Westera, & Boleda, 2020](https://github.com/amore-upf/manynames/releases#:~:text=Silberer%2C%20Zarrie%C3%9F%2C%20Westera%2C%20%26%20Boleda%2C%20202))
