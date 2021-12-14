## ---- RESPONSE FORMATTING
refrmtResp <- function(x, type, incl, linewidth, asterisks) {
  
  #which responses to include
  resp = x$responses
  if (incl == "singletons") {
    if (asterisks & length(x$singletons) > 0) {
      names(x$singletons) = paste0(names(x$singletons), "*")}
    resp = append(resp, x$singletons)
  } else if (incl == "incorrect") {
    if (asterisks & length(x$incorrect) > 0) {
      names(x$íncorrect) = paste0(names(x$incorrect), "**")}
    resp = append(resp, x$incorrect)
  } else if (incl == "all") {
    if (asterisks & length(x$singletons) > 0) {
      names(x$singletons) = paste0(names(x$singletons), "*")}
    if (asterisks & length(x$incorrect) > 0) {
      names(x$incorrect) = paste0(names(x$incorrect), "**")} 
    resp = append(resp, append(x$singletons, x$incorrect))}
  
  #order by count
  resp = resp[order(-unlist(resp))] 
  
  #calculate values (count vs. percent)
  if (type == "count") {
    values = sapply(resp, function(y) {paste0("(", y, "),")})
  } else if (type == "pct") {
    values = sapply(resp, function(y, total = as.numeric(sum(unlist(resp)))) {
      yval = round(y / total  * 100)
      paste0("(", as.character(yval), "),")})
  }
  
  #combine to one string
  y = paste(c(rbind(names(resp), values)), collapse = " ")
  
  #split into 3 lines, line breaks at commas
  xcom1 = gregexpr(pattern = ',', y)[[1]]
  line1 = paste0(substr(y, 1, max(xcom1[xcom1 < linewidth])), "\n")
  y = substr(y, max(xcom1[xcom1 < linewidth]) + 2, nchar(y))
  
  xcom2 = gregexpr(pattern = ',', y)[[1]]
  line2 = paste0(substr(y, 1, max(xcom2[xcom2 < linewidth]) ), "\n")
  line3 = substr(y, max(xcom2[xcom2 < linewidth]) + 2, nchar(y))
  
  #if line 3 too long end with "..."
  if (nchar(line3) > linewidth) {
    line3 = substr(line3, 1, linewidth - 3)
    line3 = paste0(substr(line3, 1, max(gregexpr(pattern = ', ', line3)[[1]])), " ...,")
  } 
  
  #combine 3 lines again
  y = paste0(line1, line2, line3)

  #remove last comma
  xcom3 = gregexpr(pattern = ',', y)[[1]]
  substr(y, max(xcom3), max(xcom3)+1) = " "
  
  return(y)
}

## ---- ANNOTATE IMAGE
annotateImage <- function(x, type = c("count", "pct"),
                          incl = c("correct", "singletons", "incorrect", "all"), 
                          asterisks = TRUE, 
                          linewidth = 39, 
                          txtsize = 40) {
  
  #dependencies
  require(magick)
  
  #check arguments
  type = match.arg(type)
  incl = match.arg(incl)

  #format string of responses
  txt = refrmtResp(x, type, incl, linewidth, asterisks)
  
  #read image
  img = image_read(path = x$link_mn)
  
  #expand canvas
  canvas = image_blank(width = 640, height = 480 + txtsize*4, color = "white")
  img = image_composite(canvas, img)
  
  #annotate with responses
  img = image_annotate(image = img, text = txt, gravity = "north",
                       location = "+0+480", size = txtsize)
  
  return(img)
}

## ---- ARRANGE IMAGES
arrangeImages <- function(x, type = c("count", "pct"),
                          incl = c("correct", "singletons", "incorrect", "all"), 
                          asterisks = TRUE, 
                          nCols = 3,
                          linewidth = 39, 
                          capsize = 40,
                          addCaption = TRUE) {
  
  #dependencies
  require(magick)
  
  #check arguments
  type = match.arg(type)
  incl = match.arg(incl)
  
  #arrange in grid (with nCols)
  x = do.call(c, x)
  x = split(x, ceiling(seq_along(x)/nCols))
  x = lapply(x, image_append)
  x = do.call(c, x)
  x = image_append(x, stack = TRUE)  
  
  #add caption
  if (addCaption) {
    
    #check arguments
    type = match.arg(type)
    incl = match.arg(incl)
    
    caption = image_blank(width = image_info(x)$width, 
                          height = image_info(x)$height + capsize*1.5, 
                          color = "white")
    
    captxtA = "Note. "
    captxtB = ifelse(type == "count", 
                     "Numbers in parentheses are counts.", 
                     "Numbers in parentheses are percentages.") 
    
    if (asterisks) {
      captxtC = ifelse(incl == "singletons", 
                       "Includes singleton responses (marked with *).", 
                       ifelse(incl == "incorrect", "Includes incorrect responses (marked with **).", 
                              ifelse(incl == "all", "Includes singletons (marked with *) and incorrect responses (marked with **).", 
                                     "")))
    } else {
      captxtC = ifelse(incl == "singletons", 
                       "Includes singleton responses", 
                       ifelse(incl == "incorrect", "Includes incorrect responses.", 
                              ifelse(incl == "all", "Includes singletons and incorrect responses.", 
                                     "")))
    }
    
    
    captxt = paste(strwrap(paste(captxtA, captxtB, captxtC, sep = " "), 
                           width = image_info(x)$width), collapse = "\n")
    
    
    caption = image_annotate(image = caption, text = captxt, 
                             gravity = "northwest", 
                             location = paste0("+20+", as.character(image_info(x)$height + 20)),
                             size = capsize/1.5, style = "italic")
    
    
    x = image_composite(caption, x)
    x = image_append(x, stack = TRUE)
  }
  
  #return image arrangement
  return(x)
}
