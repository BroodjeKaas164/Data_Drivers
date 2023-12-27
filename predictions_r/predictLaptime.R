################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
source('predictions_r/sourceUsedLibraries.r', chdir=TRUE)
source('predictions_r/sourceModelFunctions.r', chdir=TRUE)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_lap_times.csv', 
                                   sep = ';')))
set <- na.omit(dataset)
set.seed(69)
# SPEEDY BOIS
trainIndex <- createDataPartition(set$raceId, p=0.007, list=FALSE)
trainIndex2 <- createDataPartition(set$raceId, p=0.5, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex2,]

################### DEFINE PARAMETERS ###################
# SETTINGS
models <- c('glm', 'rf', 'leapForward', 'leapBackward')
optimiseModel <- 'glm'
p_factor <- 'milliseconds'

# INITIALISERS
model_dict <- list()
real_values <- set[[as.character(p_factor)]]
rename_real <- paste0('set.', as.character(p_factor))

################### TRAIN MODELS ###################
for (model in models) {
  model_name <- paste0('model_', model)
  print(model_name)
  model <- try(train(milliseconds ~ driverId + raceId + position, data=trainData, method=model))
  print(summary(model))
  try(model_dict[[model_name]] <- model)
}

################### PREDICTION RESULTS ###################
results_predicted <- data.frame(real_values)
names(results_predicted)[names(results_predicted)=='real_values'] <- 'real'

for (model in models) {
  model_name <- paste0('model_', model)
  print(model_name)
  try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=set), digits=0))))
}
print(summary(results_predicted))
# plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(real_values)
names(results_mean)[names(results_mean)=='real_values'] <- 'real'
results_mean['p_mean'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['p_median'] <-  round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
results_mean['p_sd'] <-  apply(results_predicted, 1, sd, na.rm=TRUE)
results_mean['p_var'] <- apply(results_predicted, 1, var, na.rm=TRUE)
print(summary(results_mean))

# MODEL REWORK
trainIndexOptimised <- createDataPartition(results_mean$real, p=0.6, list=FALSE)
trainDataOptimised <- results_mean[trainIndexOptimised,]

model_optimised <- try(train(real ~ p_mean + p_median, data=trainDataOptimised, method=optimiseModel))

results_final <- data.frame(real_values)
names(results_final)[names(results_final)=='real_values'] <- 'real'
results_final['p_optimised'] <- try(data.frame(round(predict(model_optimised, newdata=results_mean), digits=0)))
results_final['difference'] <- results_final$p_optimised - results_mean$real
print(summary(results_final))
plot(results_final)
