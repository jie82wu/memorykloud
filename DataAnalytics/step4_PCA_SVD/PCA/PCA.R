data <- read.table("maxtrix_no_headers.csv", header=F, sep=",")
pca <- prcomp(data, scale=TRUE)
summary(pca)
top10 <- pca$rotation[,10]