library(lme4)
library(tidyverse)

visits <- read_csv("csvs/visit_counts_by_period.csv")
visits <- visits %>%
  mutate(
    pi = factor(pi),
    color = factor(color),
    period = factor(period)
  )

table(visits$pi, visits$color) # Quick check that no one location was imbalanced by chance

# Fit model with counts as response relative to fixed effect (color) and random effects (pi=location, period=shuffle period)
m1 <- glmer(count ~ color + (1|pi) + (1|period),
            data = visits, family = "poisson")
summary(m1)

# Fit model without location and compare to m1 with Likelihood Ratio Test
m0 <- glmer(count ~ color + (1|period), family = "poisson", data = visits)
anova(m0, m1, test = "LRT")

library(DHARMa) # Check for overdispersion (confirm) Poisson is appropriate)
simres <- simulateResiduals(m1)
plot(simres) # No overdispersion
