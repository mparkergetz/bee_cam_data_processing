library(tidyverse)
library(iNEXT)
library(jsonlite)

abundance_list <- fromJSON("csvs/abundance_list.json")

n    <- sapply(abundance_list, sum)
sobs <- sapply(abundance_list, function(x) sum(x > 0))
f1   <- sapply(abundance_list, function(x) sum(x == 1))
f2   <- sapply(abundance_list, function(x) sum(x == 2))
n; sobs; f1; f2

out <- iNEXT(abundance_list, q = c(0,1,2), datatype = "abundance", nboot = 1000)
ggiNEXT(out, type = 3) 



endpoint <- floor(min(n) * 1.2)   # avoid long extrapolation tails
out <- iNEXT(
  abundance_list,
  q = c(0, 1, 2),
  datatype = "abundance",
  endpoint = endpoint,
  knots = 60,       # more points along each curve
  se = TRUE         # turn FALSE to remove ribbons for an even cleaner look
)

# Try different views:
p_size      <- ggiNEXT(out, type = 1)  # sample-size based
p_coverage  <- ggiNEXT(out, type = 2)  # coverage-based (often smoothest)
p_profile   <- ggiNEXT(out, type = 3)  # your original call
p_profile
