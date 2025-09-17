library(vegan)
data <- read.csv("csvs/permanova/species_matrix_raw.csv")
rownames(data) <- data$pi_period
species_data <- data[, 4:ncol(data)]

# run permanova, stratified by three periods when the stimuli were shuffled
species_pa <- decostand(species_data, method = "pa")

# Run PERMANOVA (Jaccard, presence/absence), stratified by shuffle period
result <- adonis2(species_pa ~ color,
                  data   = data,
                  strata = data$period,
                  permutations = 9999,
                  method = "jaccard",
                  binary = TRUE)
print(result)

# Check for dispersion differences (PERMDISP)
dist_mat <- vegdist(species_pa, method = "jaccard", binary = TRUE)
mod <- betadisper(dist_mat, data$color)
anova(mod)