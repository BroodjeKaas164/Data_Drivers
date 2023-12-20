################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_lap_times.csv', 
                                   sep = ';')))
set <- na.omit(dataset)

################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(quantregForest)
library(caret)
library(cvms)
library(tibble)

################### Train Models ###################
model_qrf <- quantregForest(x = set, y = set$milliseconds, nthreads = 2)
model_lm <- lm(milliseconds ~ driverId + raceId + position, data=set)
model_rf <- randomForest(milliseconds ~ driverId + raceId + position, data=set, proximity=TRUE)

################### Make Predictions ###################
prediction_results <- data.frame(set$milliseconds)
names(prediction_results)[names(prediction_results)=='set.milliseconds'] <- 'mil_real'
prediction_results['mil_qrf'] <- data.frame(abs(round(predict(model_qrf, newdata = set), digits = 0)))
prediction_results['mil_lm'] <- data.frame(abs(round(predict(model_lm, newdata = set), digits = 0)))
prediction_results['mil_rf'] <- data.frame(abs(round(predict(model_rf, newdata = set), digits = 0)))
plot(prediction_results)

################### "Gecombineerd Gemiddelde" ###################
mean_results <- data.frame(set$positionOrder)
mean_results['mil_predicted'] <- abs(round(rowMeans(prediction_results, na.rm=TRUE), digits = 0))
names(mean_results)[names(mean_results)=='set.milliseconds'] <- 'mil_real'
plot(mean_results)
