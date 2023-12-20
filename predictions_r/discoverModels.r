################### IMPORT LIBRARIES ###################
library(caret)
library(nnet)
library(tidyverse)
library(frbs)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Library/CloudStorage/OneDrive-StichtingHogeschoolUtrecht/Jaar 2/Semester 3/Speedway Dynamics/Practice/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(20)
train_index <-  createDataPartition(set$Gender, p=0.69, list=FALSE)
train_data <- set[train_index,]
test_data <- set[-train_index,]

################### Dynamic Evolving Neural-Fuzzy Inference System (DENFIS) ###################
summary(model_DENFIS <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='DENFIS'))

################### Generalised Linear Model (glm) ###################
summary(model_glm <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='glm'))

################### Negative Binomial Generalized Linear Model (glm.nb) ###################
summary(model_glmnb <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='glm.nb'))

################### Parallel Random Forest (parRF) ###################
summary(model_parRF <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='parRF'))

################### Quantile Random Forest (qrf) ###################
summary(model_qrf <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='qrf'))

################### Random Forest (rf) ###################
summary(model_rf <- train(Annual.Salary ~ Gender + Ethnicity + Age + Country + City + Department, data=train_data, method='rf'))
# saveRDS(model_rf, file='/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_rf.rda')
# model_rf <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_rf.rda')

################### PREDICTION RESULTS ###################
prediction_results <- data.frame(test_data$Annual.Salary)
names(prediction_results)[names(prediction_results)=='test_data.Annual.Salary'] <- 'real'
prediction_results['pred_rf'] <- predict(model_rf, newdata=test_data)
prediction_results['pred_glm'] <- predict(model_glm, newdata=test_data)
prediction_results['pred_glmnb'] <- predict(model_glmnb, newdata=test_data)
prediction_results['pred_parRF'] <- predict(model_parRF, newdata=test_data)
prediction_results['pred_qrf'] <- predict(model_qrf, newdata=test_data)
prediction_results['pred_DENFIS'] <- predict(model_DENFIS, newdata=test_data)
plot(prediction_results)

################### GECOMBINEERD GEMIDDELDE ###################
# (van gemiddelde van alles) naar (gemiddelde van alles binnen 2*standaarddeviatie)???
mean_results <- data.frame(test_data$Annual.Salary)
mean_results['mean_predicted'] <- abs(round(rowMeans(prediction_results, na.rm=TRUE), digits=0))
mean_results$median_predicted = round(apply(prediction_results, 1, median, na.rm=TRUE), digits=0)
names(mean_results)[names(mean_results)=='test_data.Annual.Salary'] <- 'real'
plot(mean_results)
