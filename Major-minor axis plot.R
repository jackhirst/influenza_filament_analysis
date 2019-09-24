rm(list = ls())
library(ggplot2)
library(reshape2)

theme_set(
  theme_light() + theme(legend.position = "top")
)

#setwd("")
myFile <- read.csv("YOURFILENAME.csv")
head(myFile)

gg <- ggplot(myFile, aes(x=Major, y = Minor))
gg + 
  facet_wrap(~ Condition, nrow = 3) +
  geom_point(size = 1, alpha = 0.2) +
  coord_cartesian(xlim = c(0, 30), ylim = c(0, 10), expand = (0.5)) +
  labs(x="Major axis (µm)", y="Minor axis (µm)", expand = FALSE) +
  theme(
    strip.text.x = element_text(size = 12, color = "black", face = "bold"),
    axis.text=element_text(size=14),
    axis.title=element_text(size = 14),
    panel.grid.minor = element_blank()
  )