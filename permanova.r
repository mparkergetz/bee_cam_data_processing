library(vegan)
data <- read.csv("csvs/permanova/species_matrix_raw.csv")
rownames(data) <- data$pi_period 
species_data <- data[, 4:ncol(data)] 

# run permanova, stratified by three periods when the stimuli were shuffled
result <- adonis2(species_data ~ color, data = data, strata = data$period, permutations = 9999, method = "bray")
print(result)

# calculate dispersion
dist_mat <- vegdist(species_data, method = "bray")
mod <- betadisper(dist_mat, data$color)
anova(mod)

# visualize with NMDS
ord <- metaMDS(species_data, distance = "bray")

ordiplot(ord, type = "n")
points(ord, display = "sites", col = as.factor(data$color), pch = 19)

ordiellipse(
  ord,
  groups = data$color,
  kind = "se",
  conf = 0.95,
  draw = "polygon", 
  col = 1:length(unique(data$color)),
  alpha = 63
)

legend("center",
       legend = unique(data$color),
       col = 1:length(unique(data$color)),
       pch = 19)

# boxplot
boxplot(mod, main = "Multivariate dispersion by color", ylab = "Distance to centroid")
TukeyHSD(mod)

# pcoa
pcoa <- cmdscale(dist_mat, k = 2, eig = TRUE)
plot(pcoa$points, col = as.factor(data$color), pch = 19,
     xlab = "PCoA1", ylab = "PCoA2", main = "Bray-Curtis PCoA")
legend("topright", legend = unique(data$color), col = 1:length(unique(data$color)), pch = 19)
