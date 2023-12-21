################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(cvms)
library(tibble)
library(frbs)
library(mgcv)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_lap_times.csv', 
                                   sep = ';')))
set <- na.omit(dataset)
set.seed(69)
trainIndex <- createDataPartition(set$raceId, p=0.69, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
summary(model_glm <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method='glm')))
summary(model_bam <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method='bam')))

################### PREDICTION RESULTS ###################
results_predicted <- data.frame(testData$milliseconds)
names(results_predicted)[names(results_predicted)=='testData.milliseconds'] <- 'real'
results_predicted['glm'] <- data.frame(abs(round(predict(model_glm, newdata=testData), digits=0)))
results_predicted['bam'] <- data.frame(abs(round(predict(model_bam, newdata=testData), digits=0)))
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(testData$milliseconds)
names(results_mean)[names(results_mean)=='testData.milliseconds'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] = round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
plot(results_mean)
