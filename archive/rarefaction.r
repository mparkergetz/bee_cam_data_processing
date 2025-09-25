library(tidyverse)
library(iNEXT)
library(jsonlite)

abundance_list <- fromJSON("csvs/abundance_list.json")

n    <- sapply(abundance_list, sum)
sobs <- sapply(abundance_list, function(x) sum(x > 0))
f1   <- sapply(abundance_list, function(x) sum(x == 1))
f2   <- sapply(abundance_list, function(x) sum(x == 2))
n; sobs; f1; f2


out <- iNEXT(
  abundance_list,
  q = c(2),
  datatype = "abundance",
  knots = 60,
  se = TRUE
)

p_size      <- ggiNEXT(out, type = 1)
p_coverage  <- ggiNEXT(out, type = 2)
p_profile   <- ggiNEXT(out, type = 3)
