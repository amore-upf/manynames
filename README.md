# ManyNames
Repository for the ManyNames dataset (version 2.2) for English and Mandarin Chinese. The English version of ManyNames provides ca. 36 name annotations for each of 25K objects in images selected from VisualGenome, whereas the Chinese version provides approximately 20 name annotations for 1319 objects in images selected from ManyNames. For an illustration see the image below.

<img src="examples/mn_images_example5.png" alt="ManyNames example" width="500"/>

For details of the data collection see [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/) (version 1.0) and [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/) (version 2.0), and [He, Liao, Liang, & Boleda, 2023](https://aclanthology.org/2023.conll-1.30/) (Mandarin Chinese version). For changes in the present version see the [release notes](https://github.com/amore-upf/manynames/blob/master/release_notes_v2.2.md). Previous versions of the dataset can be accessed as older releases in this repository.

## Notation
|Abbreviation | Description |
| -------- |  -------- |
|MN| ManyNames  |
|VG| VisualGenome (the dataset from which the MN images were extracted) |

## Data files
The dataset is provided in two formats:

* **TSV**: tab-separated text file, first row contains the column labels, nested data is stored as python dictionaries (i.e., "{key: value}")
* **JSON**: the same data set in .json format to facilitate access (to the nested data) outside of python. Included in subfolder *other_data*

The columns that are included for **both languages** are labelled as follows.

| Column | Type | Description |
| -------- | :-------: | -------- |
| vg_object_id | int | The VG id of the object |
| link_mn | str | The url to the image, with the object marked |
| topname | str | The most frequent name produced by subjects for the object |
| responses | dict | Correct responses and their counts |
| mn_bbox_xywh | list| The coordinates of the object: "[left x, bottom y, width, height]"; y=0 is at the top of the image.
| vg_image_id | int | The VG id of the image |
| vg_obj_name | str | The VG name of the object |
| vg_domain | str | The MN domain of the VG name, which may be a superset of its WordNet category (encoded in column vg_cat). Example: The MN domain *food* subsumes the WordNet categories *food, solid food*, and *food, nutrient*. |
| vg_synset | str | The WordNet synset of the object, as provided by VG.  |
| domain | str | The MN domain of the object, i.e. categorisation of objects into *people*, *animals_plants*, *vehicles*, *food*, *home*, *buildings*, and *clothing* |
| N | int | The number of types in the MN responses (each name counts once) |
| total_responses | int | Sum count of correct responses (tokens; each subject production of a name counts once)|
| perc_top | float | The relative frequency of the topname (among correct responses), in percentage|
| H | float | The H agreement measure from Snodgrass and Vanderwart (1980), which is the entropy over subject responses |

The English ManyNames dataset also includes the columns listed below.

| Column | Type | Description |
| -------- | :-------: | -------- |
| link_vg | str | The url to the image in VG |
| incorrect | dict | Incorrect responses and their counts |
| split | str | Use of the image in training vs. test vs. validation in [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/) |

The Mandarin Chinese ManyNames dataset also includes the following columns.

| Column | Type | Description |
| -------- | :-------: | -------- |
|  list  |  str | Lists of images assigned to participants |
| familiarity | float | Familiarity approximated as the weighted average of the corpus frequency of the responses |


*Note*: A subset of the ManyNames data has also been annotated for Catalan within the [AINA project](https://projecteaina.cat/). It is available [here](https://huggingface.co/datasets/projecte-aina/cat_manynames).

## Subfolder: other-data/

This folder contains the MN datasets in JSON format, a file with additional information about the MN objects, and files with lexical information (concreteness, familiarity, imageability, age of acquisition and frequency per million tokens) for each name in the ManyNames datasets. See the README inside the folder for more information.

## Subfolder: scripts/

### Python scripts
The python scripts require the following packages:
  * `pandas` for `manynames.py`, `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`
  * `skimage` (for `visualise.py`)
  * `matplotlib.pyplot` (for `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`)
  * `PIL` (for `create_MN_images.py`, `download_MN_images.py`)
  * `tqdm` (for `create_MN_images.py`, `download_MN_images.py`)

The scripts can be run from the command line. Use `python <script-name> -h` for more information.

* **`manynames.py`**
  loads the MN data into a pandas DataFrame.
* **`visualise.py`**
  provides a function to draw the bounding box around the target object and label it with its MN object names (and VG name).
* **`agreement_table.py`**
  creates a summary table of name agreement indices (reproducing Table 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the current data).
* **`plot_distr_topnames.py`**
  creates a stacked box plot, showing the distribution of MN topnames per domain (reproducing Figure 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with current data).
* **`create_MN_images.py`**
  creates the images as stored under manynames.upf.edu from their VG source.
* **`download_MN_images.py`**
  downloads a subset of images from manynames.upf.edu.
* **`showExamples.py`**
  annotates and displays subsets of MN-images.

### R scripts
The R-script **`download_MN_images.r`** can be used, as its Python counterpart, to download a subset of images from manynames.upf.edu.


## Citing ManyNames / attribution
* For **any use** of ManyNames:

Silberer, C., S. Zarrieß, G. Boleda. 2020. [Object Naming in Language and Vision: A Survey and a New Dataset](https://aclanthology.org/2020.lrec-1.710/). Proceedings of the 12th International Conference on Language Resources and Evaluation (LREC 2020).

```
@inproceedings{silberer2020manynames,
  title = {{Object Naming in Language and Vision: A Survey and a New Dataset}},
  author = {Silberer, Carina and Zarie{\ss}, Sina and Boleda, Gemma},
  booktitle = {Proceedings of the 12th International Conference on Language Resources and Evaluation (LREC 2020)},
  year = {2020},
  url = {https://aclanthology.org/2020.lrec-1.710/},
  pages = "5792--5801"
}
```

* In addition, if you refer to anything specific to version 1 of ManyNames:

Silberer, C., S. Zarrieß, M. Westera, G. Boleda. 2020. [Humans meet models on object naming: A new dataset and analysis](https://aclanthology.org/2020.coling-main.172/). Proceedings of the 28th International Conference on Computational Linguistics.

```
@inproceedings{silberer-etal-2020-humans,
    title = "Humans Meet Models on Object Naming: A New Dataset and Analysis",
    author = "Silberer, Carina and Zarrie{\ss}, Sina and Westera, Matthijs and Boleda, Gemma",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    year = "2020",
    url = "https://aclanthology.org/2020.coling-main.172",
    doi = "10.18653/v1/2020.coling-main.172",
    pages = "1893--1905"
}
```

* In addition, if you use the data for Mandarin Chinese:

He, Y., Liao, X., Liang, J., Boleda, G. 2023. [The Impact of Familiarity on Naming Variation: A Study on Object Naming in Mandarin Chinese](https://aclanthology.org/2023.conll-1.30/). Proceedings of the 27th Conference on Computational Natural Language Learning (CoNLL).

```
@inproceedings{he-etal-2023-impact,
    title = "The Impact of Familiarity on Naming Variation: A Study on Object Naming in {M}andarin {C}hinese",
    author = "He, Yunke and Liao, Xixian and Liang, Jialing and Boleda, Gemma",
    booktitle = "Proceedings of the 27th Conference on Computational Natural Language Learning (CoNLL)",
    year = "2023",
    url = "https://aclanthology.org/2023.conll-1.30",
    doi = "10.18653/v1/2023.conll-1.30",
    pages = "456--475"
}
```

## Version history
* **version 2.2**: Added all singletons responses (= responses given only once) following a manual correction procedure; added Mandarin Chinese names for a subset of the data

* **version 2.1.1**: Added bounding box coordinates for ManyNames image versions. Updated image links to new domain: manynames.upf.edu

* **version 2.1**: Corrections to topname and domain definitions, inclusion of some singleton responses (for details see [release notes](https://github.com/amore-upf/manynames/blob/master/release_notes_v2.1.md))

* **version 2.0**: Integration of name verification data (for details see [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/))

* **version 1.0**: Initial release (for details see [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/))

## About
ManyNames is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/), and based on  VisualGenome at [visualgenome.org](https://visualgenome.org).

This project has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 715154).
