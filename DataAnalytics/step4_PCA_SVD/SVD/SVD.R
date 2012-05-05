data <- read.table("maxtrix_no_headers.csv", header=F, sep=",")
s<-svd(data, 300, 300)
write.csv(s$u, file ="svd.csv")