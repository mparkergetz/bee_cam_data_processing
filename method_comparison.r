library(iNEXT)

abundance_list <- fromJSON("csvs/abundance_list.json")
out <- iNEXT(abundance_list, q = c(0,1,2), datatype = "abundance", nboot=1000)

write.csv(out$AsyEst, "csvs/AsyEst.csv", row.names = FALSE)
write.csv(out$DataInfo, "csvs/DataInfo.csv", row.names = FALSE)
write.csv(out$iNextEst$size_based, "csvs/iNextEst_size_based.csv", row.names = FALSE)
write.csv(out$iNextEst$coverage_based, "csvs/iNextEst_coverage_based.csv", row.names = FALSE)
