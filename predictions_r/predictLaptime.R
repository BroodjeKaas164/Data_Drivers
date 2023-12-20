################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(cvms)
library(tibble)
library(frbs)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_lap_times.csv', 
                                   sep = ';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$raceId, p=0.69, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### Train Models ###################
summary(model_glm <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method='glm')))
summary(model_DENFIS <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method='DENFIS')))

################### Make Predictions ###################
prediction_results <- data.frame(testData$milliseconds)
names(prediction_results)[names(prediction_results)=='testData.milliseconds'] <- 'mil_real'
prediction_results['mil_glm'] <- data.frame(abs(round(predict(model_glm, newdata=testData), digits=0)))
prediction_results['mil_DENFIS'] <- data.frame(abs(round(predict(model_DENFIS, newdata=testData), digits=0)))
plot(prediction_results)

################### "Gecombineerd Gemiddelde" ###################
mean_results <- data.frame(testData$milliseconds)
mean_results['mil_predicted'] <- abs(round(rowMeans(prediction_results, na.rm=TRUE), digits=0))
names(mean_results)[names(mean_results)=='testData.milliseconds'] <- 'mil_real'
plot(mean_results)
