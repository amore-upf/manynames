# Other data
This subfolder contains:

* The ManyNames datasets in JSON format (`manynames-en.json`, `manynames-zh.json`).

* CSV files `lexical-info-en.csv`, `lexical-info-zh.csv`, containing lexical information (concreteness, familiarity, imageability, age of acquisition, frequency in English/Chinese, frequency within ManyNames, context diversity) for each name in ManyNames. This information has been retrieved from the resources listed below.

* A file with additional information about the ManyNames data (`additional-info-en.tsv`). Note that this information is here and not in the main file because it is likely to be of interest to few users only. More information about its content can be found below.

* A file with anonymized participant information for each response in the English version of ManyNames (`subject-ids-en.tsv`). Note that there are up to 27 IDs available per image only, because some annotation files were lost.

* A template in HTML and PDF of the task and instructions that were given to turkers for the manual singleton verification process (`instructions-for-singleton_verification.pdf / .html`).

## Additional information for English ManyNames

File `other-data/additional-info-en.tsv` contains the additional columns in the following table. These are pieces of information that correspond either to the adjudication process for the names (see [Silberer , Zarrieß, & Boleda 2020](https://aclanthology.org/2020.coling-main.172/); columns `vg_same_object`, `vg_adequacy_mean`, `vg_inadequacy_type`, `vg_clusters`, `clusters`, `same_object`, `adequacy_mean`, `inadequacy_type`), or to further information from VisualGenome (columns `filename`, `vg_cat`, `vg_bbox_xywh`).

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
| Concreteness (`concreteness`)|Brysbaert, M., Warriner, A.B. & Kuperman, V. (2014). Concreteness ratings for 40 thousand generally known English word lemmas. *Behavior Research Methods*, 46, 904–911. https://doi.org/10.3758/s13428-013-0403-5|Min: 1.62<br>Max: 5<br>Mean: 4.59<br>SD: 0.45|Concreteness values were retrieved from column `Conc.M`, which corresponds to the mean concreteness rating of each word. They lie on the range of 1 ("Abstract, language based") to 5 ("Concrete, experience based").|
|<br>Familiarity (`familiarity`)<br>Imageability (`imageability`)| Scott, G.G., Keitel, A., Becirspahic, M. et al. The Glasgow Norms: Ratings of 5,500 words on nine scales. *Behav Res* 51, 1258–1270 (2019). https://doi.org/10.3758/s13428-018-1099-3 |IMAGEABILITY<br>Min: 2.35<br>Max: 6.94<br>Mean: 6.18<br>SD: 0.68<br><br>FAMILIARITY<br>Min: 2.55<br>Max: 6.91<br>Mean: 5.68<br>SD: 0.81| Imageability and familiarity values were retrieved from subcolumn `M`  of columns `IMAG` and `FAM`, which correspond to the mean rating of each word regarding the corresponding measurement. They lie on the range of 1 ("very unimageable/unfamiliar") to 7 ("very imageable/familiar").|
| Age of Acquisition (`age_of_acquisition`)| Brysbaert, M., & Biemiller, A. (2017). Test-based age-of-acquisition norms for 44 thousand English word meanings. *Behavior Research Methods, 49*(4), 1520–1523. https://doi.org/10.3758/s13428-016-0811-4 |Min: 2<br>Max: 14<br>Mean: 4.39<br>SD: 3.29| Age of acquisition was retrieved from column `AoAtest-based`, which corresponds to the age at what each word is considered to be integrated in the vocabulary of children, according to the results of a multiple-choice test. As stated by Brysbaert & Biemiller (2016), "words were assigned to the grade level at which 67 %–80 % of the specific word meanings were passed."|
| Frequency (`freq_en`) <br> Log frequency (`log10freq_en`) <br> Context diversity (`context_div_en`)| Brysbaert, M., & New, B. (2009). Moving beyond Kučera and Francis: A critical evaluation of current word frequency norms and the introduction of a new and improved word frequency measure for American English. *Behavior Research Methods, 41*(4), 977–990. https://doi.org/10.3758/brm.41.4.977 |FREQUENCY<br>Min: 0.02<br>Max: 5247.45<br>Mean: 29.51<br>SD 156.13<br><br>LOG FREQ<br>Min: 0.3<br>Max: 5.43<br>Mean: 2.3<br>SD: 0.89<br><br>CONTEXT DIVERSITY<br>Min: 1<br>Max: 8353<br>Mean: 542.7<br>SD: 1080.86|<ul><li>Values in MN column `freq_en` were retrieved from column `SUBTLWF` (frequency per million words).</li><li>Values in MN column `log10freq_en` were retrieved from `Lg10WF` (based on log10).</li><li>Values in MN column `context_div_en` were retrieved from `CDcount` (number of films in which the word appears).</li></ul>|
|Frequency in the dataset (`n_tokens`, `n_images`) | | NUMBER OF TOKENS<br>Min: 1<br>Max: 37358<br>Mean: 290.44<br>SD: 2157.97<br><br>NUMBER OF IMAGES<br>Min: 1<br>Max: 3913<br>Mean: 28.43<br>SD: 152.02| <ul><li>`n_tokens`: Frequency of each name within correct answers of ManyNames (tokens; each subject production of a name counts once)</li><li>`n_images`: Frequency of each name in terms of the number of images of ManyNames in which it appears as a correct answer</li></ul>|

### For Mandarin Chinese

| Measurement retrieved | Original source citation | Measurement scale | Notes |
|:----------------------|:-------------------------|:------------------|:------|
| Concreteness (`concreteness`) <br> Imageability (`imageability`)| Chan, YL., Tse, CS. Decoding the essence of two-character Chinese words: Unveiling valence, arousal, concreteness, familiarity, and imageability through word norming. *Behav Res* 56, 7574–7601 (2024). https://doi.org/10.3758/s13428-024-02437-w |CONCRETENESS<br>Min: 3.4<br>Max: 6.55<br>Mean: 5.51<br>SD: 0.51<br><br>IMAGEABILITY<br>Min: 2.6<br>Max: 6.65<br>Mean: 5.41<br>SD: 0.59 | Concreteness and imageability values were retrieved from columns `conc_mean` and `imag_mean` respectively, corresponding to the mean rating of each word. They lie on the range of 1 ("very abstract/difficult to form a mental image") to 7 ("very concrete/easy to form a mental image").|
| Familiarity (`familiarity`) | Su, Y., Li, Y. & Li, H. Familiarity ratings for 24,325 simplified Chinese words. *Behav Res* 55, 1496–1509 (2023). https://doi.org/10.3758/s13428-022-01878-5 | Min: 3.67<br>Max: 7<br>Mean: 6.06<br>SD: 0.56 |Familiarity values were retrieved from column `FAM_M`, corresponding to the mean familiarity rating of each word. They lie on the range of 1 ("very unfamiliar, which means that the word is unrecognizable or rarely seen") to 7 ("very familiar, which means that they have seen, heard, or used the word nearly every day in life").|
| Age of Acquisition (`age_of_acquisition`)|Xu, X., Li, J. & Guo, S. Age of acquisition ratings for 19,716 simplified Chinese words. *Behav Res* 53, 558–573 (2021). https://doi.org/10.3758/s13428-020-01455-8 | Min: 3.86<br>Max: 17.63<br>Mean: 9.49<br>SD: 2.32|Age of acquisition values were retrieved from column `AoA Mean`, corresponding to the mean age of acquisition for each word. Participants were asked to "recall and enter the age (in years) at which they had learned it", meaning the age at "they could understand the word [...] even if they had not used, read, or written it at the time" (Xu, Li & Guo, 2011).|
| Frequency (`freq_zh`) <br> Log frequency (`log10freq_zh`) <br> Context diversity (`context_div_zh`)| Cai, Q., & Brysbaert, M. (2010). SUBTLEX-CH: Chinese Word and Character Frequencies Based on Film Subtitles. *Plos ONE, 5(6), e10729*. https://doi.org/10.1371/journal.pone.0010729 | FREQUENCY<br>Min: 2<br>Max: 5015513<br>Mean: 7667.16<br>SD: 141184.95<br><br>LOG FREQ<br>Min: 0<br>Max: 52898<br>Mean: 19532.93<br>SD: 10506.09<br><br>CONTEXT DIVERSITY<br>Min: 1<br>Max: 6243<br>Mean: 403.54<br>SD: 850.93| <ul><li>Values in MN column `freq_zh` were retrieved from column `W.million`, and correspond to the word frequency per million words.</li><li>Values in MN column `log10freq_zh` were retrieved from column `log10W` of the same file, and correspond to the log10 of column `WCount`.</li><li>Values in MN column `context_div_zh` were retrieved from column `W-CD`, corresponding to the number of films in which the word was observed (out of a maximum of 6,243).</li></ul>|
|Frequency in the dataset (`n_tokens`, `n_images`) | | NUMBER OF TOKENS<br>Min: 1<br>Max: 1322<br>Mean: 11.8<br>SD: 63.77<br><br>NUMBER OF IMAGES<br>Min: 1<br>Max: 310<br>Mean: 3.73<br>SD: 11.84| <ul><li>`n_tokens`: Frequency of each name within correct answers of ManyNames (tokens; each subject production of a name counts once)</li><li>`n_images`: Frequency of each name in terms of the number of images of ManyNames in which it appears as a correct answer</li></ul>|