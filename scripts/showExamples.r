## ---- DEPENDENCIES
library(magick)
library(jsonlite)
source("scripts/functions_showExamples.r")

## ---- READ MANYNAMES DATA
mn <- jsonlite::read_json(path = 'manynames.json')

## ---- EXAMPLE 1: PERCENTAGES - ONLY CORRECT
#STEP 1: get random sample of 6 images
set.seed(1)
idx <- sample(seq_along(mn), size = 6)

#STEP 2: annotate images (percentages, only correct responses)
pars = list(type = "pct", incl = "correct")
res <- sapply(mn[idx], FUN = function(x) {do.call(annotateImage, c(list(x), pars))})

#STEP 3: arrange the image in grid (with 3 columns)
#note: parameters type and incl need to be set here to get the correct caption
res <- do.call(arrangeImages, c(list(res, nCols = 3), pars))

#STEP 4: save image
image_write(res, path = "mn_images_example1.png")


## ---- EXAMPLE 2: COUNTS - INCLUDING SINGLETONS AND INCORRECT
#STEP 1: get random sample of 6 images
set.seed(1)
idx <- sample(seq_along(mn), size = 6)

#STEP 2: annotate images (counts, all responses)
pars = list(type = "count", incl = "all")
res <- sapply(mn[idx], FUN = function(x) {do.call(annotateImage, c(list(x), pars))})

#STEP 3: arrange the image in grid (with 3 columns)
#note: parameters type and incl need to be set here to get the correct caption
res <- do.call(arrangeImages, c(list(res, nCols = 3), pars))

#STEP 4: save image
image_write(res, path = "mn_images_example2.png")

 
## ---- EXAMPLE 3: COUNTS - INCLUDING SINGLETONS AND INCORRECT - ONLY TOPNAME MAN
#STEP 1: get random sample of 6 images from images with topname "man
set.seed(1)
tn.man = sapply(mn, function(x) {x$topname == "man"})
idx <- sample(which(tn.man), size = 6)

#STEP 2: annotate images (counts, all responses)
pars = list(type = "count", incl = "all")
res <- sapply(mn[idx], FUN = function(x) {do.call(annotateImage, c(list(x), pars))})

#STEP 3: arrange the image in grid (with 3 columns)
#note: parameters type and incl need to be set correctly (here by just passing pars) to get the correct caption
res <- do.call(arrangeImages, c(list(res, nCols = 3), pars))

#STEP 4: save image
image_write(res, path = "mn_images_example3.png")

