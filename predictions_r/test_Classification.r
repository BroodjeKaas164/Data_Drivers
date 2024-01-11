################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$resultId, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################

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
plot(results_mean)

################### CONFUSION MATRIX ###################
predictions <- tibble('target'=set$positionOrder, 'prediction'=results_mean$mean_predicted)
cf <- as_tibble(table(predictions))
plot_confusion_matrix(cf, target_col='target', prediction_col='prediction', counts_col='n', add_col_percentages=FALSE,add_normalized=FALSE,add_row_percentages=FALSE,palette='Reds')
