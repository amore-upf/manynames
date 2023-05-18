#!/usr/bin/env Rscript

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## - creates a folder "images" and downloads the images specified in the csv 
##   downloaded from the ManyNames website into it
## - can be run on the command line with:
##   "[R Path]bin\Rscript.exe" download_Manynames_images.r
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# read csv
imgdat <- read.table('ManyNames_data.csv', header=TRUE, sep=",")

#make image folder
dir_name <- 'images/'
if (!dir.exists(dir_name)) {
  dir.create(dir_name)  
}

#download unique image files
img_links <- unique(imgdat$link_mn)
sapply(img_links, function(url) {
  file_path <- gsub('http://object-naming-amore.upf.edu//', dir_name, url)
  download.file(url, file_path)  
})
