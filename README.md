# ManyNames

Repository for the ManyNames dataset (version 2.0). ManyNames provides 36 name annotations for each of 25K objects in images selected from VisualGenome (for details see [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/)). In version 2.0 verification annotations were added to the dataset (for details see [Silberer, Zarrieß, Westera, & Boleda, 2020](https://aclanthology.org/2020.coling-main.172/)). The previous version of the dataset can be accessed as an older release in this repository.

## Notation
|Abbreviation | Description |
| -------- |  -------- |
|MN| ManyNames  |
|WN| WordNet  |
|VG| VisualGenome  |
|domain| Categorisation of objects into *people*, *animals_plants*, *vehicles*, *food*, *home*, *buildings*, and *clothing* |

For each domain, there exists at least one WordNet category out of *article of clothing*, *instrumentality, instrumentation*, *person*, *tableware*, *ware*, *food, nutrient*, *structure, construction*, *animal*, *tool*, *food, solid food*, *plant, flora, plant life*, *vehicle*.

## Data file: manynames.tsv

| Column | Type | Description |
| -------- | :-------: | -------- |
| vg_image_id | int | The VG id of the image |
| vg_object_id | int | The VG id of the object |
| url | str | The url to the image, with the object marked |
| topname | str | The most frequent name in the MN responses |
| domain | str | The MN domain of the MN object |
| responses | Counter | The collected MN names and their counts, i.e., the number of annotators responding them |
| same_object | dict | Mean same-object ratings for response pairs |
| adequacy_mean | dict | Mean adequacy ratings for MN responses |
| inadequacy_type | dict | Rated inadequacy rating for MN responses |
| incorrect | dict | Incorrect responses and their counts |
| singletons | dict | Contains all names which were given only once, i.e., with count=1. <br>Example: `{'sofa': 1, 'armchair': 1}` |
| vg_obj_name | str | The VG name of the object |
| vg_domain | str | The MN domain of the VG name, which may be a superset of its WN category (vg_cat). <br>Example: The MN domain *food* subsumes the WN categories *food, solid food* and *food, nutrient*. |
| vg_synset | str | The WN synset of the object, provided by VG |
| vg_same_object | dict | same object ratings for the vg_object_name
| vg_adequacy_mean | float | mean adequacy rating for the vg_object_name
| vg_inadequacy_type | dict | rated inadequacy type for the vg_object_name
| vg_image_name | str | The name of the VG image |
| bbox_xywh | list | The coordinates of the object in the image: [left x, bottom y, width, height] <br>(y=0 is at the top of the image)|
| vg_cat | str | The WordNet hypernym of the VG synset, corresponds roughly to one of the 7 MN domains.  |
| link_vg | str | The url to the image in VG |
| perc_top_v2 | float | The relative frequency of the topname (among correct responses)|

## Subfolder: scripts
### Package Requirements:
  * `pandas`
  * `skimage` (for `visualise.py`)
  * `matplotlib.pyplot` (for `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`)

### Usage:
When run from the command line, all scripts can be given as optional argument the path to the ManyNames dataset: `python <script-name> <path-to-manynames.tsv>`. By default this path is set to `../manynames.tsv` from the script directory.

* **`manynames.py`**
  *Loads the MN data into a pandas DataFrame.*<br>
* **`visualise.py`**
  *Provides a function to draw the bounding box around the target object and label it with its MN object names (and VG name).*
* **`agreement_table.py`**
  *Creates a summary table of name agreement indices (reproducing Table 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the v2.0 data).*<br>
* **`plot_distr_topnames.py`**
  *Creates a stacked box plot, showing the distribution of MN topnames per domain (reproducing Figure 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the v2.0 data).*<br>

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
