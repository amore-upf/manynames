# Release Notes - ManyNames v2.1

In version 2.1 we addressed some potentially problematic issues regarding the definition of topnames and domains and well as the treatment of spelling variants. We also adjusted the treatment of singleton responses so that singleton responses which are likely to be correct names for the target object are no longer excluded from name agreement calculation. Finally, we simplified the structure of the data columns detailing the verification data to ease accessibility. Each issue is described in more detail below.

### Definition of topnames and incorrect responses
**Problem**: In ManyNames v2.0 it could happen that a cluster of words referring to the same object *overall* had a higher number of selections than the most frequent name alone. For instance, in a case like: {*giraffe*: 12, *woman*: 10, *person*: 9}, the cluster *woman-person* has a higher number of selections than the cluster *giraffe*.

**Solution**: In these cases, the *topname* is defined as the most frequent name within the largest name cluster (instead of the most frequent name overall). In addition names belonging to the largest cluster are coded as correct (instead of names belonging to the cluster of the most frequent name). In the example above, the topname was changed to *woman* (instead of *giraffe*) and *woman*, *girl*, and *person* are now counted as correct (and *giraffe* as incorrect).

**Affected columns**: clusters (new), topname, responses, incorrect

### Update/correct domains

**Problem**: Some domain definitions may have to be adjusted after updating the topname (see above). In addition, some domain definitions were incorrect or inconsistent across the data set (i.e., images with the same topname could have different domain definitions).

**Solution**: To resolve inconsistencies we now define the domain for each image as the domain in which the respective topname appears most frequently in. In case of a tie, we manually selected the most appropriate domain. For the topname *mouse*, the domain was generally changed from *animals_plants* to *home* (we only have images of the electronic device).

Please note, that for some images/names the most appropriate domain label is not unequivocally clear.

* Some names could be placed into multiple MN domains. This concerns cases like *mirror* (home, vehicles -- in case of a motorcycle mirror), *clock* (home, buildings -- in case of a clock tower), and *banana* (animals_plants, food). For these cases, we just applied the frequency rule.

* The names *sand*, *snow*, *field*, *water*, *grass* were lacking a corresponding MN domain. In order to avoid adding a new (and very sparse) domain label, these names were included into the domain *animals_plants* (which therefore may be more broadly understood as *natural world*).

**Affected columns**: domain

### Spelling variants
**Problem**: Different spellings of noun-noun compounds were so far counted as different names (e.g., 'tea pot' vs 'teapot').

**Solution**: When responses differed only in one white space, the response counts were summed under the most frequent spelling variant.

**Affected columns:**: responses

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

To verification data (same object and adequacy ratings) are now stored for all names (correct and incorrect) in the same columns (see below). The column *incorrect* now only includes the incorrect names with their response counts but no longer their verification data.

* **same_object**: it now contains, for all the naming annotations of each data point (correct and incorrect names), their reciprocal *same object* score. Singletons - which are included in the responses, but for which we do not have a *same object* score - are labelled with “NA”.

* **inadequacy_type**: it now contains, for all the naming annotations of each data point (correct and incorrect names), the corresponding *inadequacy type* information. Singletons - which are included in the responses, but for which we do not have any *inadequacy type* annotations - are labelled with “NA”. Note that, differently, a *inadequacy type* "None", means that annotators have marked that name as totally adequate for the corresponding image.

* **adequacy_mean**: it now contains, for all the naming annotations of each data point (correct and incorrect names), the corresponding *adequacy mean* information. Singletons - which are included in the responses, but for which we do not have any *adequacy mean* annotations - are labelled with “NA”.
