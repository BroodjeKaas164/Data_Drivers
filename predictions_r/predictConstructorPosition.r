################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))
library(caret)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_constructor_standings.csv', 
                                   sep=';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$constructorStandingsId, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
models <- c('glm', 'lm')
model_dict <- list()

for (model in models) {
  model_name <- paste0('model_', model)
  model <- try(train(points ~ raceId + constructorId + position + wins, data=trainData, method=model))
  try(model_dict[[model_name]] <- model)
}

############## PREDICTION RESULTS ###################
results_predicted <- data.frame(set$points)
names(results_predicted)[names(results_predicted)=='set.points'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=set), digits=0))))
}
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(set$points)
names(results_mean)[names(results_mean)=='set.points'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] <-  round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
results_mean['sd_predicted'] <-  apply(results_predicted, 1, sd, na.rm=TRUE)
results_mean['var_predicted'] <- apply(results_predicted, 1, var, na.rm=TRUE)

# MODEL REWORK
testmodel <- try(train(real ~ mean_predicted + median_predicted + sd_predicted + var_predicted, data=results_mean, method = 'glm'))
testresults <- try(data.frame(predict(testmodel, data=results_mean)))
results_mean['optimised'] <- testresults
plot(results_mean)
