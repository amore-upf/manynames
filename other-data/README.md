# Other data
This subfolder contains:

* the ManyNames datasets in JSON format (`manynames-en.json`, `manynames-zh.json`).

* CSV files `lexical-info-en.csv`, `lexical-info-zh.csv`, containing lexical information (concreteness, familiarity, imageability, age of acquisition, frequency in English/Chinese, frequency within ManyNames) for each name in ManyNames. This information has been retrieved from the resources listed below.

* a file with additional information about the ManyNames data (`additional-info-en.tsv`). Note that this information is here and not in the main file because it is likely to be of interest to few users only. More information about its content can be found below.

* a file with anonymized participant information for each response in the English version of ManyNames (`subject-ids-en.tsv`). Note that there are up to 27 IDs available per image only, because some annotation files were lost.

* a template in HTML and PDF of the task and instructions that were given to turkers for the manual singleton verification process (`instructions_for_singleton_verification.pdf / .html`).

## Additional information for English ManyNames

File `other-data/additional-info-en.tsv` contains the additional columns in the following table. These are pieces of information that correspond either to the adjudication process for the names (see [Silberer , Zarrieß, & Boleda 2020](https://aclanthology.org/2020.coling-main.172/); in columns `vg_same_object`, `vg_adequacy_mean`, `vg_inadequacy_type`, `vg_clusters`, `clusters`, `same_object`, `adequacy_mean`, `inadequacy_type`), or to further information from VisualGenome (in columns `filename`, `vg_cat`, `vg_bbox_xywh`).

| Column | Type | Description |
|:-------|:----:|:------------|
| vg_object_id | int | The VG id of the object |
| vg_image_id | int | The VG id of the image |
| link_vg | str | The url to the image in VG |
| vg_same_object | dict | Same object ratings for the vg_object_name
| vg_adequacy_mean | str | Mean adequacy rating for the vg_object_name
| vg_inadequacy_type | dict | Rated inadequacy type for the vg_object_name
| filename | str | The filename of the VG image |
| vg_cat | str | The WN hypernym of the VG synset, corresponds roughly to one of the 7 ManyNames domains. |
| clusters | dict | Response clusters and total count per cluster |
| adequacy_mean | dict | Mean adequacy ratings for ManyNames responses |
| inadequacy_type | dict | Rated inadequacy rating for ManyNames responses |
| same_object | dicts | Mean same-object ratings for response pairs |

## Resources for lexical information

### For English

| Measurement retrieved | Original source citation | Measurement scale | Notes |
|:----------------------|:-------------------------|:------------------|:------|
| Concreteness (`concreteness`)|Brysbaert, M., Warriner, A.B. & Kuperman, V. (2014). Concreteness ratings for 40 thousand generally known English word lemmas. *Behavior Research Methods*, 46, 904–911. https://doi.org/10.3758/s13428-013-0403-5|Min: 1.04<br>Max: 5.00<br>Mean: 3.04<br>SD: 1.04|Concreteness values were retrieved from column `Conc.M`, which corresponds to the mean concreteness rating of each word. They lie on the range of 1 ("Abstract, language based") to 5 ("Concrete, experience based").|
|<br>Familiarity (`familiarity`)<br>Imageability (`imageability`)| Scott, G.G., Keitel, A., Becirspahic, M. et al. The Glasgow Norms: Ratings of 5,500 words on nine scales. *Behav Res* 51, 1258–1270 (2019). https://doi.org/10.3758/s13428-018-1099-3 |IMAGEABILITY<br>Min: 1.737<br>Max: 6.941<br>Mean: 4.79<br>SD: 1.35<br><br>FAMILIARITY<br>Min: 1.647<br>Max: 6.939<br>Mean: 5.26<br>SD: 0.93| Imageability and familiarity values were retrieved from subcolumn `M`  of columns `IMAG` and `FAM`, which correspond to the mean rating of each word regarding the corresponding measurement. They lie on the range of 1 ("very unimageable/unfamiliar") to 7 ("very imageable/familiar").|
| Age of Acquisition (`age_of_acquisition`)| Brysbaert, M., & Biemiller, A. (2017). Test-based age-of-acquisition norms for 44 thousand English word meanings. *Behavior Research Methods, 49*(4), 1520–1523. https://doi.org/10.3758/s13428-016-0811-4 |Min: 2.00<br>Max: 14.00<br>Mean: 8.66<br>SD: 3.93| Age of acquisition was retrieved from column `AoAtest-based`, which corresponds to the age at what each word is considered to be integrated in the vocabulary of children. As stated by Brysbaert & Biemiller (2016), "words were assigned to the grade level at which 67 %–80 % of the specific word meanings were passed."|
| Frequency (`freq_en`) <br> Log frequency (`log_freq_en`) <br> Context diversity (`context_div_en`)| Brysbaert, M., & New, B. (2009). Moving beyond Kučera and Francis: A critical evaluation of current word frequency norms and the introduction of a new and improved word frequency measure for American English. *Behavior Research Methods, 41*(4), 977–990. https://doi.org/10.3758/brm.41.4.977 |FREQUENCY<br>Min: 0.02<br>Max: 41857.12<br>Mean: 13.12<br>SD 338.77<br><br>LOG FREQ<br>Min: 0.301<br>Max: 6.3293<br>Mean: 1.19<br>SD: 0.84<br><br>CONTEXT DIVERSITY<br>Min: 1<br>Max: 8388<br>Mean: 121.61<br>SD: 611.50|<ul><li>Values in MN column `freq_en` were retrieved from column `SUBTLWF` (frequency per million words).</li><li>Values in MN column `log_freq_en` were retrieved from `Lg10WF` (based on log10).</li><li>Values in MN column `context_div_en` were retrieved from `CDcount` (number of films in which the word appears).</li></ul>|
|Frequency in the dataset (`freq_mn`) | | Min: 1<br>Max: 37358<br>Mean: 290.44<br>SD: 2157.97 | Frequency of each name within correct answers of ManyNames (tokens; each subject production of a name counts once) |

### For Mandarin Chinese

| Measurement retrieved | Original source citation | Measurement scale | Notes |
|:----------------------|:-------------------------|:------------------|:------|
| Concreteness (`concreteness`) <br> Imageability (`imageability`)| Chan, YL., Tse, CS. Decoding the essence of two-character Chinese words: Unveiling valence, arousal, concreteness, familiarity, and imageability through word norming. *Behav Res* 56, 7574–7601 (2024). https://doi.org/10.3758/s13428-024-02437-w |CONCRETENESS<br>Min: 2.2<br>Max: 6.65<br>Mean: 4.60<br>SD: 0.72<br><br>IMAGEABILITY<br>Min: 1.85<br>Max: 6.65<br>Mean: 4.21<br>SD: 0.87 | Concreteness and imageability values were retrieved from columns `conc_mean` and `imag_mean` respectively, corresponding to the mean rating of each word. They lie on the range of 1 ("very abstract/difficult to form a mental image") to 7 ("very concrete/easy to form a mental image").|
| Familiarity (`familiarity`) | Su, Y., Li, Y. & Li, H. Familiarity ratings for 24,325 simplified Chinese words. *Behav Res* 55, 1496–1509 (2023). https://doi.org/10.3758/s13428-022-01878-5 | Min: 1.634921<br>Max: 7.0<br>Mean: 5.56<br>SD: 0.75 |Familiarity values were retrieved from column `FAM_M`, corresponding to the mean familiarity rating of each word. They lie on the range of 1 ("very unfamiliar, which means that the word is unrecognizable or rarely seen") to 7 ("very familiar, which means that they have seen, heard, or used the word nearly every day in life").|
| Age of Acquisition (`age_of_acquisition`)|Xu, X., Li, J. & Guo, S. Age of acquisition ratings for 19,716 simplified Chinese words. *Behav Res* 53, 558–573 (2021). https://doi.org/10.3758/s13428-020-01455-8 | Min: 3.857142857142857<br>Max: 21.235294117647058<br>Mean: 11.91<br>SD: 2.30|Age of acquisition values were retrieved from column `AoA Mean`, corresponding to the mean age of acquisition for each word. Participants were asked to "recall and enter the age (in years) at which they had learned it", meaning the age at "they could understand the word [...] even if they had not used, read, or written it at the time" (Xu, Li & Guo, 2011).|
| Frequency (`freq_zh`) <br> Log frequency (`log_freq_zh`) <br> Context diversity (`context_div_zh`)| Cai, Q., & Brysbaert, M. (2010). SUBTLEX-CH: Chinese Word and Character Frequencies Based on Film Subtitles. *Plos ONE, 5(6), e10729*. https://doi.org/10.1371/journal.pone.0010729 | FREQUENCY<br>Min: 2<br>Max: 5015513<br>Mean: 928.87<br>SD: 32353.26<br><br>LOG FREQ<br>Min: 0<br>Max: 62259<br>Mean: 7359.29<br>SD: 8937.11<br><br>CONTEXT DIVERSITY<br>Min: 1<br>Max: 6243<br>Mean: 74.76<br>SD: 397.49| <ul><li>Values in MN column `freq_zh` were retrieved from column `W.million`, and correspond to the word frequency per million words-</li><li>Values in MN column `log_freq_zh` were retrieved from column `log10W` of the same file, and correspond to the log10 of column `WCount`.</li><li>Values in MN column `context_div_zh` were retrieved from column `W-CD`, corresponding to the number of films in which the word was observed (out of a maximum of 6,243).</li></ul>|
|Frequency in the dataset (`freq_mn`)||Min: 1<br>Max: 1322<br>Mean: 11.80<br>SD: 63.77|Frequency of each name within correct answers of ManyNames (tokens; each subject production of a name counts once)|
