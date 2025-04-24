#!/usr/bin/env Rscript

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## - downloads the images specified in the input file into "../MN_images" 
## - takes a .tsv (like manynames-en.tsv from GitHub) or .csv (like ManyNames_data.csv 
##   created from the search interface) as input. File needs to contain a column
##   labelled "link_mn" with the image urls
## - can be run on the command line with:
##   "[R Path]bin\Rscript.exe" download_MN_images.r
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# read csv
# imgdat <- read.table('ManyNames_data.csv', header=TRUE, sep=",")

# read tsv
imgdat <- read.table('../manynames-en.tsv', header=TRUE, sep="\t")

#make image folder
dir_name <- 'MN_images/'
if (!dir.exists(dir_name)) {
  dir.create(dir_name)  
}

#download unique image files
img_links <- unique(imgdat$link_mn)
sapply(img_links, function(url) {
  file_name <- gsub('http://manynames.upf.edu/', '', url)
  file_path <- paste(dir_name, file_name, sep='')
  if (file.exists(file_path)) {
    print(paste('skipping:', file_path, 'because it already exists', sep = ' '))
  } else {
    download.file(url, file_path, mode = 'wb')
    }
})
