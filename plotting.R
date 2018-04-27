#!/usr/bin/Rscript
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  print(args[1])
}
pca <- read.table(args[1])
library(ggplot2)
# plot(pca$V3, pca$V4)
# ggplot(pca, aes(x=V3, y=V4, col=V23))
# ggplot(pca, aes(x=V3, y=V4, col=V23)) + geom_point()
ggplot(pca, aes(x=V3, y=V4, col=V23)) + geom_point() + xlab("PC1") + ylab("PC2")