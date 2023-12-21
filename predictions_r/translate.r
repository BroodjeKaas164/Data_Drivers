################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(nnet)
library(tidyverse)
library(frbs)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Library/CloudStorage/OneDrive-StichtingHogeschoolUtrecht/Jaar 2/Semester 3/Speedway Dynamics/Practice/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(69)
trainIndex <- createDataPartition(set$Gender, p=0.69, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
models <- c('glm', 'glm.nb', 'parRF', 'rf', 'qrf')
model_dict <- list()

# TODO: Make train parameters dynamic
for (model in models) {
  model_name <- paste0('model_', model)
  model <- try(train(Annual.Salary ~ Gender + Age + Department, data=trainData, method=model))
  try(model_dict[[model_name]] <- model)
} 

################### PREDICTION RESULTS ###################
# TODO?: remove real values from set?
results_predicted <- data.frame(testData$Annual.Salary)
names(results_predicted)[names(results_predicted)=='testData.Annual.Salary'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=testData), digits=0))))
}
plot(results_predicted)

################### COMBINED MEANDIAN ###################
# TODO?: (van gemiddelde van alles) naar (gemiddelde van alles binnen 2*standaarddeviatie)???
results_mean <- data.frame(testData$Annual.Salary)
names(results_mean)[names(results_mean)=='testData.Annual.Salary'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] <-  round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)

################### MODEL REWORK ###################
testmodel <- try(train(real ~ mean_predicted + median_predicted, data=results_mean, method = 'qrf'))
testresults <- try(data.frame(predict(testmodel, data=results_mean)))
results_mean['combined_predicted'] <- testresults
plot(results_mean)
