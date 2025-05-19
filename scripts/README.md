# Scripts

## Python scripts
The python scripts require the following packages:
  * `pandas` for `manynames.py`, `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`
  * `skimage` (for `visualise.py`)
  * `matplotlib.pyplot` (for `agreement_table.py`, `plot_distr_topnames.py` and `visualise.py`)
  * `PIL` (for `create_MN_images.py`, `download_MN_images.py`)
  * `tqdm` (for `create_MN_images.py`, `download_MN_images.py`)

The scripts can be run from the command line. Use `python <script-name> -h` for more information.

* **`manynames.py`**
  loads the ManyNames data into a pandas DataFrame.
* **`visualise.py`**
  provides a function to draw the bounding box around the target object and label it with its ManyNames names.
* **`agreement_table.py`**
  creates a summary table of name agreement indices (reproducing Table 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with the current data).
* **`plot_distr_topnames.py`**
  creates a stacked box plot, showing the distribution of ManyNames topnames per domain (reproducing Figure 3 in [Silberer, Zarrieß, & Boleda (2020)](https://aclanthology.org/2020.lrec-1.710/) with current data).
* **`create_MN_images.py`**
  creates the images as stored under manynames.upf.edu from their VisualGenome source.
* **`download_MN_images.py`**
  downloads a subset of images from manynames.upf.edu.
* **`showExamples.py`**
  annotates and displays subsets of ManyNames images.
* **`add_lexical_info.py`**
  add measures from file `lexical-info-{lang}.tsv` to the main file `manynames-{lang}.tsv` in a dict format.

## R scripts
The R-script **`download_MN_images.r`** can be used, as its Python counterpart, to download a subset of images from [manynames.upf.edu](https://manynames.upf.edu/).
