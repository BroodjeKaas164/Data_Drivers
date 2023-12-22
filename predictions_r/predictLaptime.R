################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(cvms)
library(tibble)
library(frbs)
library(mgcv)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_lap_times.csv', 
                                   sep = ';')))
set <- na.omit(dataset)
set.seed(69)
trainIndex <- createDataPartition(set$raceId, p=0.69, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
models <- c('glm', 'BstLm')
model_dict <- list()

for (model in models) {
  model_name <- paste0('model_', model)
  model <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method=model))
  try(model_dict[[model_name]] <- model)
}

################### PREDICTION RESULTS ###################
results_predicted <- data.frame(testData$milliseconds)
names(results_predicted)[names(results_predicted)=='testData.milliseconds'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=testData), digits=0))))
}
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(testData$milliseconds)
names(results_mean)[names(results_mean)=='testData.milliseconds'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] = round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
plot(results_mean)
