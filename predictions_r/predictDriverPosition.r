################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))
library(quantregForest)
library(caret)
library(cvms)
library(tibble)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_results.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(69)
trainIndex <- createDataPartition(set$resultId, p=0.85, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
models <- c('qrf', 'lm', 'rf')
model_dict <- list()

summary(model_dict[[paste0('model_', models[1])]] <- quantregForest(x=set, y=set$positionOrder, nthreads=4))
summary(model_dict[[paste0('model_', models[2])]] <- lm(positionOrder ~ points + grid, data=set))
summary(model_dict[[paste0('model_', models[3])]] <- randomForest(positionOrder ~ points + grid, data=set, proximity=TRUE))

################### PREDICTION RESULTS ###################
results_predicted <- data.frame(set$positionOrder)
names(results_predicted)[names(results_predicted)=='set.positionOrder'] <- 'pos_real'

for (model in models) {
    model_name <- paste0('model_', model)
    try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=set), digits=0))))
}
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(set$positionOrder)
# results_mean <- data.frame(abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0)))
names(results_mean)[names(results_mean)=='set.positionOrder'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] <- round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
results_mean['sd_predicted'] <- round(apply(results_predicted, 1, sd, na.rm=TRUE), digits=0)
results_mean['var_predicted'] <- round(apply(results_predicted, 1, var, na.rm=TRUE), digits=0)

# MODEL REWORK
testmodel <- try(train(real ~ mean_predicted + median_predicted + sd_predicted + var_predicted, data=results_mean, method = 'parRF'))
testresults <- try(data.frame(predict(testmodel, data=results_mean)))
results_mean['optimised'] <- testresults
plot(results_mean)
# plot(results_mean$real, results_mean$modelrework)

################### CONFUSION MATRIX ###################
predictions <- tibble('target'=set$positionOrder, 'prediction'=results_mean$mean_predicted)
cf <- as_tibble(table(predictions))
plot_confusion_matrix(cf, target_col='target', prediction_col='prediction', counts_col='n', add_col_percentages=FALSE,add_normalized=FALSE,add_row_percentages=FALSE,palette='Reds')
