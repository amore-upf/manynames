# ManyNames

Repository for the ManyNames dataset (version 1.0). ManyNames provides 36 name annotations for each of 25K objects in images selected from VisualGenome. For details see [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/).

## Notation
|Abbreviation | Description |
| -------- |  -------- |
|MN| ManyNames  |
|WN| WordNet  |
|VG| VisualGenome  |
|domain| Categorisation of objects into *people*, *animals_plants*, *vehicles*, *food*, *home*, *buildings*, and *clothing* |

For each domain, there exists at least one WordNet category out of *article of clothing*, *instrumentality, instrumentation*, *person*, *tableware*, *ware*, *food, nutrient*, *structure, construction*, *animal*, *tool*, *food, solid food*, *plant, flora, plant life*, *vehicle*.

## Data files
### manynames.tsv

| Column | Type | Description |
| -------- | :-------: | -------- |
| vg_image_id | int | The VG id of the image |
| vg_object_id | int | The VG id of the object |
| url | str | The url to the image, with the object marked |
| topname | str | The most frequent name in the MN responses |
| domain | str | The MN domain of the MN object |
| N | float | The number of types in the MN responses |
| perc_top | float | The relative frequency of the most frequent response (in percent) |
| H | float | The H agreement measure from (Snodgrass and Vanderwart, 1980) |
| responses | Counter | The collected MN names and their counts, i.e., the number of annotators responding them |
| singletons | dict | Contains all names which were given only once, i.e., with count=1. <br>Example: `{'sofa': 1, 'armchair': 1}` |
| vg_obj_name | str | The VG name of the object |
| vg_domain | str | The MN domain of the VG name, which may be a superset of its WN category (vg_cat, see `images.tsv`). <br>Example: The MN domain *food* subsumes the WN categories *food, solid food* and *food, nutrient*. |
| vg_synset | str | The WN synset of the object, provided by VG |

### images.tsv
| Column | Type | Description |
| -------- | :-------: | -------- |
| vg_image_id | int | The VG id of the image |
| vg_image_name | str | The name of the VG image |
| vg_object_id | int | The VG id of the object |
| vg_obj_name | str | The VG name of the object |
| bbox_xywh | list | The coordinates of the object in the image: [left x, bottom y, width, height] <br>(y=0 is at the top of the image)|
| vg_synset | str | The WN synset of the object, provided by VG |
| vg_cat | str | The WordNet hypernym of the VG synset, corresponds roughly to one of the 7 MN domains.  |

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
  *Creates a summary table of name agreement indices (Table 3 in [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/)).*<br>
* **`plot_distr_topnames.py`**
  *Creates a stacked box plot, showing the distribution of MN topnames per domain (Figure 3 in [Silberer, Zarrieß, & Boleda, 2020](https://aclanthology.org/2020.lrec-1.710/)).*<br>

## Subfolder: images
Contains sample images (from VG) which are used in the demo of `visualise.py`.

## Citing ManyNames
Silberer, C., S. Zarrieß, G. Boleda. 2020. [Object Naming in Language and Vision: A Survey and a New Dataset](https://aclanthology.org/2020.lrec-1.710/). Proceedings of the Twelfth International Conference on Language Resources and Evaluation (LREC 2020).

```
@inproceedings{ silberer2020manynames,
  title = {{Object Naming in Language and Vision: A Survey and a New Dataset}},
  author = {Silberer, Carina and Zarie{\ss}, Sina and Boleda, Gemma},
  booktitle = {Proceedings of the Twelfth International Conference on Language Resources and Evaluation (LREC 2020)},
  year = {2020},
  url = {https://aclanthology.org/2020.lrec-1.710/},
}
```

## About
ManyNames is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/), and based on VisualGenome at [visualgenome.org](https://visualgenome.org).

This project has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 715154).
