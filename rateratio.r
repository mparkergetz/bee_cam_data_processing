library(rateratio.test)

data <- read.csv("csvs/grouped_counts_clover.csv")

n <- nrow(data)
results <- list()

for (i in 1:(n-1)) {
  for (j in (i+1):n) {
    test_result <- rateratio.test(
      x = c(data$Counts[i], data$Counts[j]),
      n = c(data$runtime_hours[i], data$runtime_hours[j])
    )
    results[[paste(data$color[i], "vs", data$color[j])]] <- test_result
  }
}

for (pair in names(results)) {
  cat("Comparison:", pair, "\n")
  print(results[[pair]])
  cat("\n")
}

comparison_results <- data.frame(
  Pair = character(),
  PValue = numeric(),
  stringsAsFactors = FALSE
)

for (pair in names(results)) {
  comparison_results <- rbind(comparison_results, data.frame(
    Pair = pair,
    PValue = formatC(results[[pair]]$p.value, format = "f", digits = 4)
  ))
}

print(comparison_results)

library(knitr)
library(kableExtra)

formatted_table <- kable(comparison_results, format = "html", col.names = c("Comparison Pair", "P-value"), align = c('l', 'r'), caption = "Pairwise Comparisons and P-Values") %>%
  kable_styling(bootstrap_options = c("striped", "hover", "condensed"), full_width = FALSE) %>%
  column_spec(1, bold = TRUE, width = "10em") %>%
  column_spec(2, width = "5em")

formatted_table

