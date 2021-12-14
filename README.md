# ManyNames
Repository for the ManyNames dataset (version 2.1). ManyNames provides 36 name annotations for each of 25K objects in images selected from VisualGenome. For an illustration see the image below.

<img src="example/mn_images_example2.png" alt="ManyNames example" width="800"/>

For details of the data collection see [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/) (version 1.0) and [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/) (version 2.0). For changes in the present version see the [release notes](https://github.com/amore-upf/manynames/release_notes_v2.1.md). Previous versions of the dataset can be accessed as older releases in this repository.

## Notation
|Abbreviation | Description |
| -------- |  -------- |
|MN| ManyNames  |
|WN| WordNet  |
|VG| VisualGenome  |
|domain| Categorisation of objects into *people*, *animals_plants*, *vehicles*, *food*, *home*, *buildings*, and *clothing* |

For each domain, there exists at least one WordNet category out of *article of clothing*, *instrumentality, instrumentation*, *person*, *tableware*, *ware*, *food, nutrient*, *structure, construction*, *animal*, *tool*, *food, solid food*, *plant, flora, plant life*, *vehicle*.

## Data files
The dataset is provided in two formats:

* ***manynames.tsv***: tab-separated text file, first row contains the column labels, nested data is stored as python dictionaries (i.e., "{key: value}")
* ***manynames.json***: the same data set in .json format to facilitate access (to the nested data) outside of python

The columns are labelled as follows. The most important columns are listed first.

| Column | Type | Description |
| -------- | :-------: | -------- |
| ***vg_object_id*** | ***int*** | ***The VG id of the object*** |
| ***link_mn*** | ***str*** | ***The url to the image, with the object marked*** |
| ***topname*** | ***str*** | ***The most frequent name of the object in the largest cluster*** |
| ***responses*** | ***dict*** | ***Correct responses and their counts*** |
| vg_image_id | int | The VG id of the image |
| link_vg | str | The url to the image in VG |
| vg_obj_name | str | The VG name of the object |
| vg_domain | str | The MN domain of the VG name, which may be a superset of its WN category (vg_cat). <br>Example: The MN domain *food* subsumes the WN categories *food, solid food* and *food, nutrient*. |
| vg_synset | str | The WN synset of the object, provided by VG |
| vg_same_object | dict | Same object ratings for the vg_object_name
| vg_adequacy_mean | str | Mean adequacy rating for the vg_object_name
| vg_inadequacy_type | dict | Rated inadequacy type for the vg_object_name
| vg_image_name | str | The name of the VG image |
| vg_cat | str | The WN hypernym of the VG synset, corresponds roughly to one of the 7 MN domains. |
| target_coord | list| The coordinates of the object in the image: "[left x, bottom y, width, height]"; y=0 is at the top of the image.
| clusters | dict | Response clusters and total count per cluster |
| domain | str | The MN domain of the object |
| N | int | The number of types in the MN responses |
| total_responses | int | Sum count of correct responses |
| perc_top | float | The relative frequency of the topname (among correct responses)|
| H | float | The H agreement measure from Snodgrass and Vanderwart (1980) |
| incorrect | dict | Incorrect responses and their counts |
| singletons | dict | All responses which were given only once and are not synonyms or hypernyms of the topname (these are included in *responses*) |
| same_object | dicts | Mean same-object ratings for response pairs |
| adequacy_mean | dict | Mean adequacy ratings for MN responses |
| inadequacy_type | dict | Rated inadequacy rating for MN responses |


## Subfolder: scripts/

### Python scripts
The python scripts require the following packages:
  * `pandas`
  * `skimage` (for `visualise.py`)
  * `matplotlib.pyplot` (for `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`)

When run from the command line, the python scripts can be given as optional argument the path to the ManyNames dataset: `python <script-name> <path-to-manynames.tsv>`. By default this path is set to `../manynames.tsv` from the script directory.

* **`manynames.py`**
  *Loads the MN data into a pandas DataFrame.*<br>
* **`visualise.py`**
  *Provides a function to draw the bounding box around the target object and label it with its MN object names (and VG name).*
* **`agreement_table.py`**
  *Creates a summary table of name agreement indices (reproducing Table 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the v2.1 data).*<br>

* **`plot_distr_topnames.py`**
  *Creates a stacked box plot, showing the distribution of MN topnames per domain (reproducing Figure 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the v2.1 data).*<br>

### R scripts
The R-scripts can be used to view a subset of MN-images together with the respective name annotations. **`showExample.r`** can be used to recreate the example image above. **`functions_showExample.r`** contains custom functions to extract and format the data from ManyNames to create this figure.

## Version history
* **version 2.1**: Corrections to topname and domain definitions, inclusion of singleton responses (for details see [release notes](https://github.com/amore-upf/manynames/release_notes_v2.1.md))

* **version 2.0**: Integration of name verification data (for details see [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/))

* **version 1.0**: Initial release (for details see [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/))


## Citing ManyNames
Silberer, C., S. Zarrieß, G. Boleda. 2020. [Object Naming in Language and Vision: A Survey and a New Dataset](https://aclanthology.org/2020.lrec-1.710/). Proceedings of the 12th International Conference on Language Resources and Evaluation (LREC 2020).

```
@inproceedings{silberer2020manynames,
  title = {{Object Naming in Language and Vision: A Survey and a New Dataset}},
  author = {Silberer, Carina and Zarie{\ss}, Sina and Boleda, Gemma},
  booktitle = {Proceedings of the 12th International Conference on Language Resources and Evaluation (LREC 2020)},
  year = {2020},
  url = {https://aclanthology.org/2020.lrec-1.710/},
}
```

Silberer, C., S. Zarrieß, M. Westera, G. Boleda. 2020. [Humans meet models on object naming: A new dataset and analysis](https://aclanthology.org/2020.coling-main.172/). Proceedings of the 28th International Conference on Computational Linguistics.

```
@inproceedings{silberer-etal-2020-humans,
    title = "Humans Meet Models on Object Naming: A New Dataset and Analysis",
    author = "Silberer, Carina and Zarrie{\ss}, Sina and Westera, Matthijs and Boleda, Gemma",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    year = "2020",
    url = "https://aclanthology.org/2020.coling-main.172",
    doi = "10.18653/v1/2020.coling-main.172",
}
```

## About
ManyNames is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/), and based on  VisualGenome at [visualgenome.org](https://visualgenome.org).


This project has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 715154).
