################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(caret)
library(nnet)
library(tidyverse)
library(frbs)

################### DEFINE DATASETS ###################
# Import Datasets
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(420)

# Split datasets
trainIndex <- createDataPartition(set$Gender, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### DEFINE PARAMETERS ###################
# SETTINGS
# TODO: Make train parameters dynamic if possible
# c('glm', 'glm.nb', 'BstLm', 'parRF', 'rf', 'qrf', 'bridge')
models <- c('glm', 'glm.nb','parRF', 'qrf', 'bridge')
optimiseModel <- 'glm.nb'
p_factor <- 'Annual.Salary'

# INITIALISERS
model_dict <- list()
real_values <- set[[as.character(p_factor)]]
rename_real <- paste0('set.', as.character(p_factor))

################### TRAIN MODELS ###################
# Gender + Age + Department
for (model in models) {
  model_name <- paste0('model_', model)
  model <- try(train(Annual.Salary ~ Gender + Age + Department, data=trainData, method=model))
  try(model_dict[[model_name]] <- model)
  print(summary(model))
}

################### PREDICTION RESULTS ###################
# TODO?: remove real values from set?
results_predicted <- data.frame(real_values)
names(results_predicted)[names(results_predicted)=='real_values'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=set), digits=0))))
  print(summary(results_predicted[model]))
}
print(summary(results_predicted))
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(real_values)
names(results_mean)[names(results_mean)=='real_values'] <- 'real'
results_mean['p_mean'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['p_median'] <-  round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
results_mean['p_sd'] <-  apply(results_predicted, 1, sd, na.rm=TRUE)
results_mean['p_var'] <- apply(results_predicted, 1, var, na.rm=TRUE)
plot(results_mean)

# MODEL REWORK
trainIndexOptimised <- createDataPartition(results_mean$real, p=0.6, list=FALSE)
trainDataOptimised <- results_mean[trainIndexOptimised,]

model_optimised <- try(train(real ~ p_mean + p_median, data=trainDataOptimised, method=optimiseModel))

results_final <- data.frame(real_values)
names(results_final)[names(results_final)=='real_values'] <- 'real'
results_final['p_optimised'] <- try(data.frame(round(predict(model_optimised, newdata=results_mean), digits=0)))
results_final['difference'] <- results_final$p_optimised - results_mean$real
plot(results_final)

# TODO: How do I actually use the models?
