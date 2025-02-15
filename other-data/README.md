# Other data
This subfolder contains:

* the ManyNames datasets in JSON format (`manynames-en.json`, `manynames-zh.json`).

* CSV files `lexical-info-en.csv`, `lexical-info-zh.csv`, containing lexical information (concreteness, familiarity, imageability, age of acquisition, frequency in English/Chinese, frequency within ManyNames) for each name in ManyNames. This information has been retrieved from the resources listed below.

* a file with additional information about the ManyNames data (`additional-info-en.tsv`). Note that this information is here and not in the main file because it is likely to be of interest to few users only. More information about its content can be found below.

* a template in HTML and PDF of the task and instructions that were given to turkers for the manual singleton verification process (`instructions_for_singleton_verification.pdf / .html`).

## Additional information for English ManyNames

File `other-data/additional-info-en.tsv` contains the additional columns in the following table. These are pieces of information that correspond either to the adjudication process for the names (see [Silberer , Zarrieß, & Boleda 2020](https://aclanthology.org/2020.coling-main.172/); in columns `vg_same_object`, `vg_adequacy_mean`, `vg_inadequacy_type`, `vg_clusters`, `clusters`, `same_object`, `adequacy_mean`, `inadequacy_type`), or to further information from VisualGenome (in columns `vg_image_name`, `vg_cat`, `vg_bbox_xywh`).

| Column | Type | Description |
| -------- | :-------: | -------- |
| vg_object_id | int | The VG id of the object |
| vg_image_id | int | The VG id of the image |
| vg_obj_name | str | The VG name of the object |
| vg_domain | str | The ManyNames domain of the VG name, which may be a superset of its WordNet category (encoded in column vg_cat). Example: The ManyNames domain *food* subsumes the WordNet categories *food, solid food*, and *food, nutrient*. |
| link_vg | str | The url to the image in VG |
| vg_same_object | dict | Same object ratings for the vg_object_name
| vg_adequacy_mean | str | Mean adequacy rating for the vg_object_name
| vg_inadequacy_type | dict | Rated inadequacy type for the vg_object_name
| vg_image_name | str | The name of the VG image |
| vg_cat | str | The WN hypernym of the VG synset, corresponds roughly to one of the 7 ManyNames domains. |
| clusters | dict | Response clusters and total count per cluster |
| adequacy_mean | dict | Mean adequacy ratings for ManyNames responses |
| inadequacy_type | dict | Rated inadequacy rating for ManyNames responses |
| same_object | dicts | Mean same-object ratings for response pairs |

## Resources for lexical information

### For English

| Measurement retrieved | Original source citation | Measurement scale |
|:----------------------|:-------------------------|:------------------|
| Concreteness,<br>Familiarity,<br>Imageability | <ul><li>Retrieved from:</li><ul><li>Wilson, M. (1988). MRC psycholinguistic database: Machine-usable dictionary, version 2.00. *Behavior Research Methods, Instruments, & Computers, 20*, 6–10. https://doi.org/10.3758/BF03202594</li></ul><li>Originally from:</li><ul><li>Gilhooly, K. J., & Logie, R. H. (1980). Age-of-acquisition, imagery, concreteness, familiarity, and ambiguity measures for 1,944 words. *Behavior Research Methods, 12*(4), 395–427. https://doi.org/10.3758/bf03201693</li><li>Pavio, A., Yuille, J.C., & Madigan, S.A. (1968). Concreteness, imagery and meaningfulness values for 925 words. *Journal of Experimental Psychology, 76*(1, Pt.2), 1–25. https://doi.org/10.1037/h0025327.</li><li>Toglia, M. P., & Battig, W. F. (1978). *Handbook of semantic word norms*. New York: Erlbaum. | As stated in the [MRC Psycholinguistic Database](https://websites.psychology.uwa.edu.au/school/MRCDatabase/mrc2.html): <ul><li>Concreteness (min: 158; max 670; mean 438; SD 120), familiarity (max 657; mean 488; SD 99), and imageability (min 129; max 669; mean 450; SD 108) values lie in the range 100 to 700</li><li>Note that they are integer values; in the original publications the scale was from 1.0 to 7.0</li></ul>|
| Age of Acquisition | Brysbaert, M., & Biemiller, A. (2017). Test-based age-of-acquisition norms for 44 thousand English word meanings. *Behavior Research Methods, 49*(4), 1520–1523. https://doi.org/10.3758/s13428-016-0811-4 | The information retrieved was contained in column `AoAtest-based`, and corresponds to "the age of acquisition estimates based on word knowledge at different school grades" (Brysbaert & Biemiller, 2016)|
| Frequency | Brysbaert, M., & New, B. (2009). Moving beyond Kučera and Francis: A critical evaluation of current word frequency norms and the introduction of a new and improved word frequency measure for American English. *Behavior Research Methods, 41*(4), 977–990. https://doi.org/10.3758/brm.41.4.977 |According to the [SUBTLEX-US database webpage](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus):<ul><li>Values in column`freq_en` were retrieved from column `SUBTLWF`, which corresponds to the word frequency per million words</li><li>Values in column `log_freq_en` were retrieved from column `Lg10WF`, which corresponds to values "based on log10(FREQcount+1) with four digit precision"</li></ul>|

### For Chinese

| Measurement retrieved | Original source citation | Measurement scale |
|:-------------------|:-------------------------|:------------------|
| Concreteness | Xu, X., & Li, J. (2020). Concreteness/abstractness ratings for two-character Chinese words in MELD-SCH. *PLoS ONE 15(6): e0232133*. https://doi.org/10.1371/journal.pone.0232133 | As stated in Xu & Li (2020):<ul><li>Scale from 1 ("very concrete") to 5 ("very abstract")</li><li>An additional option “N” was also provided to participants when they felt that they did not know the meaning of the word</li></ul> |
| Familiarity,<br>Imageability,<br>Age of Acquisition | Song, D., & Li, D. (2021). Psycholinguistic Norms for 3,783 Two-Character Words in Simplified Chinese. *SAGE Open, 11*(4). https://doi.org/10.1177/21582440211054495 | As stated in Song & Li (2021):<ul><li>Familiarity (min: 2.82; max 7.00; mean 5.75; SD 0.63) and imageability (min 1.30; max 7.00; mean 4.69; SD 0.96) values are based on a seven-point Likert scale<ul><li>7 indicates more familiarity/more clearness of the images the word arouses in the participant's mind</li></ul><li>Age of acquisition (min 1.00; max 4.70; mean 2.48; SD 0.64) values are based on a seven-point Likert scale<ul><li>Participants were asked to select a number from 1 to 7 depending on when they consider they first saw, heard, or used each word</li><li>Numbers 1, 2, 3, 4, 5, and 6 refer to grades 3, 5, 8, 9, 11, and 12, respectively, and 7 refers to university studies</li></ul> |
| Frequency | Cai, Q., & Brysbaert, M. (2010). SUBTLEX-CH: Chinese Word and Character Frequencies Based on Film Subtitles. *Plos ONE, 5(6), e10729*. https://doi.org/10.1371/journal.pone.0010729 |<ul><li>Values in column `freq_zh` were retrieved from column `W.million` in file *SUBTLEX_CH_131210_CE.utf8*, and correspond to the word frequency per million words</li><li>Values in column `log_freq_zh` were retrieved from column `log10W` of the same file, and correspond to the log10 of column `WCount`</li></ul> |
