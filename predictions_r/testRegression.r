################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(nnet)
library(tidyverse)
library(frbs)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(420)
trainIndex <- createDataPartition(set$Gender, p=0.75, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
models <- c('glm', 'glm.nb', 'BstLm', 'parRF', 'rf', 'qrf', 'bridge')
model_dict <- list()

# TODO: Make train parameters dynamic if possible
p_factor <- 'Annual.Salary'

for (model in models) {
  model_name <- paste0('model_', model)
  model <- try(train(Annual.Salary ~ Gender + Age + Department, data=trainData, method=model))
  try(model_dict[[model_name]] <- model)
}

################### PREDICTION RESULTS ###################
# TODO?: remove real values from set?
results_predicted <- data.frame(set$Annual.Salary)
names(results_predicted)[names(results_predicted)=='set.Annual.Salary'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=set), digits=0))))
}
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(set$Annual.Salary)
names(results_mean)[names(results_mean)=='set.Annual.Salary'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] <-  round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
results_mean['sd_predicted'] <-  apply(results_predicted, 1, sd, na.rm=TRUE)
results_mean['var_predicted'] <- apply(results_predicted, 1, var, na.rm=TRUE)

# MODEL REWORK
testmodel <- try(train(real ~ mean_predicted + median_predicted, data=results_mean, method = 'parRF'))
testresults <- try(data.frame(round(predict(testmodel, data=results_mean), digits=0)))
results_mean['optimised'] <- testresults
plot(results_mean)

df_predicted <- data.frame(set$Annual.Salary)
names(df_predicted)[names(df_predicted)=='set.Annual.Salary'] <- 'real'
df_predicted['predicted'] <- testresults
df_predicted['verschil'] <- round(apply(df_predicted, 1, sd, na.rm=TRUE), digits=0)
plot(df_predicted)

# TODO: How do I actually use the models?
