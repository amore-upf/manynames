# **ManyNames interface**

## **General**
The web interface is publicly accessible under: https://amore-upf.github.io/manynames/.

The code behind the website lives in the folder `docs` in the [public repository for ManyNames](https://github.com/amore-upf/manynames/). The data source for the web interface are the files `manynames-en/zh.json` contained in folder *other-data/* of the public repo.

All computations on the website (counting images, filtering the data, etc.) is done with javascript and runs client-side. This allows us to host the site and the data files on Github while having the image files, which are too many and too large overall for GitHub, hosted by UPF [here](https://manynames.upf.edu/).

## **Folders and files**

### **assets/**
Intended for scripts and style sheets copied from an external source (open-source) for use on the website. Right now only contains `sortable.min.js` and `sortable.min.css` which enable the sorting functionality of the result table for the names search. 

### **css/**
Intended for custom style sheets. Contains the `main.css` which defines the size and color of the menu headers, some stylistic aspects of the names result table, etc.

### **img/**
Intended for images used on the website (team member portraits, logos...) with the exception of the ManyNames images as shown in the image search (these are read from the location given in `manynames-en/zh.json`).

### **js/**
Intended for custom .js-scripts. Contains the following files:

**names.js:** Enables the names search functionality. The script reads the input fields and updates the table accordingly. The general functionality is that the scripts reads `manynames-en/zh.json` and transforms the data into html-table rows for all names with their respective token count, image counts, top name counts and co-occurring names. This html-table is then inserted into `names.html` and filtered depending on user input (updating happens with each keystroke of the user). This is done by showing only table rows which fit the user input. 

**nav.js:** Contains the content of the navbar. Its main purpose is to only have to change one file when changing the names of elements of the navbar (or their location). 

**search.js:**
Enables the image search functionality. The script reads `manynames-en/zh.json` and contains the functions to gather the user input (after clicking the "Submit"-button). Based on this the html-code to build the search result section is created from the data (i.e, for showing the images, navigation buttons...). The general structure is the same as for `names.js` but somewhat more complex in terms of the helper functions to filter the data, format the text output under each image, and enable the pagination and download functionality of the search results. 

*Note. The search results are made up from smaller, thumbnail version of the images. These are hosted under `'http://manynames.upf.edu/small/'` instead of `'http://manynames.upf.edu/'` (file names are the same but with *_s* added for the small versions). This was done to improve loading speed of the webpage when skipping through the image results. This is not visible to the user. Clicking on the image opens the full scale version and the tooltip link on hover shows the url of the full scale version as well.*

### **html files**
The html files correspond to homepage (`index.html`) and the the menu items (`about.html`, `contact.html`, `search.html`...). The `search.html` and `names.html` call the corresponding custom js-scripts to create the dynamic content (the image search results, the name search results...). For this purpose, these .html contain empty placeholders sections which are marked with ids which the .js scripts are searching for when creating the content.