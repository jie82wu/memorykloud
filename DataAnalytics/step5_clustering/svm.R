# load library, class, a dependence for the SVM library
library(class)

# load library, SVM  
library(e1071) 


# load data
dataset <- read.table("svd_no_header-10_clustered.csv", header=T, sep=",")

# get the index of all data
index <- 1:nrow(dataset)

# generate test index
testindex <- sample(index, trunc(length(index)/10))

# generate test set
testset <- dataset[testindex, ]

# generate trainin set
trainset <- dataset[-testindex,] 

# train svm on the training set
# cost=100: the penalizing parameter for C-classication
# gamma=1: the radial basis function-specific kernel parameter
# Output values include SV, index, coefs, rho, sigma, probA, probB

# svm(x, y = NULL, scale = TRUE, type = NULL, kernel =
# "radial", degree = 3, gamma = if (is.vector(x)) 1 else 1 / ncol(x),
# coef0 = 0, cost = 1, nu = 0.5,
# class.weights = NULL, cachesize = 40, tolerance = 0.001, epsilon = 0.1,
# shrinking = TRUE, cross = 0, probability = FALSE, fitted = TRUE, seed = 1L,
# ..., subset, na.action = na.omit)
# tolerance controls when the algorithm stops
svm.model <- svm(Label~ ., data = trainset, cost = 100, gamma = 1)

# show output coefficients
svm.model$coefs

# generate a scatter plot of the data of a svm fit for classification model in two dimensions: RI and Na
# plot(svm.model, trainset, V1~V2)

# a vector of predicted values, for classification: a vector of labels
svm.pred <- round(predict(svm.model, testset[, -12]))

# a cross-tabulation of the true versus the predicted values
table(pred = svm.pred, true = testset[, 12])