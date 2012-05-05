#refrences:
#http://www.r-tutor.com/gpu-computing/clustering/hierarchical-cluster-analysis
#http://gettinggeneticsdone.blogspot.com/2009/06/hierachical-clustering-in-r.html
#http://stat.ethz.ch/R-manual/R-devel/library/stats/html/hclust.html
####################### SAMPLE #######################

# preparing sample data:
hilbert <- function(n) { i <- 1:n; 1 / outer(i - 1, i, "+") }
X <- hilbert(9)[,1:6]
# now, X is a 9*6 matrix

###### general hierarchical clustering ######
d <- dist(as.matrix(X))   # find distance matrix 
hc <- hclust(d)           # apply hirarchical clustering 
plot(hc)                  # plot the dendrogram
memb <- cutree(hc, k = 4)
cent <- NULL
#for(k in 1:4){
#  cent <- rbind(cent, colMeans(X[memb == k, , drop = FALSE]))
#}
cent <- NULL
for(k in 1:4){
  cent <- rbind(cent, cbind(X[memb == k, , drop = FALSE], k))
}
write.csv(cent, "cluster.dat")

###### Birch ######
# create a CF-tree
birchObj <- birch(X, .008, keeptree = TRUE)
birchTree <- birch.getTree(birchObj)
# for viewing purposes:
length(birchTree$N) # this tells us that there are 5 subclusters
birchTree$members
# Calculate the distance matrix and perform an agglomerative hierarchical clustering, and feed in the # of clusters
bDist <- dist.birch(birchObj)
hc <- hclust(bDist)
clusters <- cutree(hc, 5)
birch.killTree(birchObj)


####################### REAL PROGRAM #######################
# we cannot use birch because there is a cap on it: 30 columns maximum
# we use kmeans with k being 10
svddata <- read.table("svd_no_header-50.csv", header=F, sep=",")
x <- data.matrix(svddata)
length(x)
cl <- kmeans(x,10)
plot(x,col=cl$cluster)
cent <- NULL
for(k in 1:10){
  cent <- rbind(cent, cbind(x[cluster == k, , drop = FALSE], k))
}
write.csv(cent, "cluster.dat")

###################### sample #################
sampledata <- read.table("sample.csv", header=F, sep=",")
part <- data.matrix(sampledata)
agn <- agnes(part)
plot(agn)
agn <- agnes(part,method="single")
plot(agn)


cl <- kmeans(part,10, nstart=20)
plot(part,col=cl$cluster)
write.csv(cl$cluster, "cluster.dat")
