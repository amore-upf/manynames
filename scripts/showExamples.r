## ---- DEPENDENCIES
library(magick)
library(jsonlite)
source("functions_showExamples.r")

## ---- READ MANYNAMES DATA
mn <- jsonlite::read_json(path = '../manynames.json')

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
image_write(res, path = "../examples/mn_images_example1.png")

## ---- EXAMPLE 2: COUNTS - INCLUDING INCORRECT
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
image_write(res, path = "../examples/mn_images_example2.png")

## ---- EXAMPLE 3: COUNTS - INCLUDING INCORRECT - ONLY TOPNAME MAN
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
image_write(res, path = "../examples/mn_images_example3.png")

## ---- EXAMPLE 4: FIGURE1 FROM SILBERER ET AL 2020
#STEP 1: get image sample
ids <- c(2327551, 2358126, 2366945, 713859, 2359569, 
         2393177, 2371995, 2357939, 2341844)
idx <- sapply(ids, function(x){
  which(sapply(mn, function(y) {y$vg_image_id == x}))
})

#STEP 2: annotate images (counts, all responses)
pars = list(type = "count", incl = "correct")
res <- sapply(mn[idx], FUN = function(x) {do.call(annotateImage, c(list(x), pars))})

#STEP 3: arrange the image in grid (with 3 columns)
#note: parameters type and incl need to be set correctly (here by just passing pars) to get the correct caption
res <- do.call(arrangeImages, c(list(res, nCols = 3), pars))

#STEP 4: save image
image_write(res, path = "../examples/mn_images_example4.png")



