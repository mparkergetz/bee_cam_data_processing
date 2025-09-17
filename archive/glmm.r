library(lme4)
library(emmeans)
library(performance)
library(glmmTMB)
library(dplyr)

df <- read.csv("/home/misha/repos/bee_cam/csvs/loc_color_counts.csv")

# glmm_pois <- glmer(Counts ~ Treatment * Location + (1 | Trap), data = df, family = poisson)
# glmm_pois <- glmer(Counts ~ Treatment + Location + (1 | Trap), data = df, family = poisson)

df_clover <- subset(df, Location == "clover")
# df_bare <- subset(df, Location == "bare")

glm_clover <- glm(Counts ~ Treatment, 
                   offset = log(runtime), 
                   family = poisson, 
                   data = df_clover)

glmm_clover <- glmer(Counts ~ Treatment + (1 | Trap), 
                     offset = log(runtime), 
                     family = poisson, 
                     data = df_clover)










glmm_clover <- glmer(Counts ~ Treatment + (1 | Trap), data = df_clover, family = poisson)
glmm_bare <- glmer(Counts ~ Treatment + (1 | Trap), data = df_bare, family = poisson)
glmm_bare <- glm(Counts ~ Treatment, data = df_bare, family = poisson)

# Summarize raw counts by treatment
df_clover %>%
  group_by(Treatment) %>%
  summarise(Total_Counts = sum(Counts),
            Mean_Counts = mean(Counts),
            Variance_Counts = var(Counts))



glmm_no_offset <- glm(Counts ~ Treatment, family = poisson, data = df_clover)

# Model with offset
glmm_with_offset <- glm(Counts ~ Treatment, 
                        offset = log(runtime), 
                        family = poisson, 
                        data = df_clover)

# Compare AICs to evaluate model fit
AIC(glmm_no_offset, glmm_with_offset)


df_clover <- df_clover %>%
  mutate(Rate = Counts / runtime)

ggplot(df_clover, aes(x = Treatment, y = Rate)) +
  geom_boxplot() +
  labs(title = "Bee Visit Rates by Treatment in Clover Location",
       y = "Bee Visits per Unit Time",
       x = "Treatment") +
  theme_minimal()

df_clover$fitted <- predict(glmm_clover, type = "response")

ggplot(df_clover, aes(x = Treatment, y = fitted)) +
  geom_boxplot() +
  labs(title = "Predicted Bee Visit Rates by Treatment in Clover Location",
       y = "Predicted Bee Visits per Unit Time",
       x = "Treatment") +
  theme_minimal()


glmm_combined <- glm(Counts ~ Treatment * Location, 
                     offset = log(runtime), 
                     family = poisson, 
                     data = df)
summary(glmm_combined)
