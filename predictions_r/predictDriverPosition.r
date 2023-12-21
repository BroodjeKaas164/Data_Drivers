################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))
library(quantregForest)
library(caret)
library(cvms)
library(tibble)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_results.csv', 
                                   sep=';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$resultId, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################
summary(model_qrf <- quantregForest(x=set, y=set$positionOrder, nthreads=4))
summary(model_lm <- lm(positionOrder ~ points + grid, data=set))
summary(model_rf <- randomForest(positionOrder ~ points + grid, data=set, proximity=TRUE))

################### PREDICTION RESULTS ###################
results_predicted <- data.frame(set$positionOrder)
names(results_predicted)[names(results_predicted)=='set.positionOrder'] <- 'pos_real'
results_predicted['pos_qrf'] <- data.frame(abs(round(predict(model_qrf, newdata=set), digits=0)))
results_predicted['pos_lm'] <- data.frame(abs(round(predict(model_lm, newdata=set), digits=0)))
results_predicted['pos_rf'] <- data.frame(abs(round(predict(model_rf, newdata=set), digits=0)))
plot(results_predicted)

################### COMBINED MEANDIAN ###################
results_mean <- data.frame(set$positionOrder)
# results_mean <- data.frame(abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0)))
names(results_mean)[names(results_mean)=='set.positionOrder'] <- 'real'
results_mean['mean_predicted'] <- abs(round(rowMeans(results_predicted, na.rm=TRUE), digits=0))
results_mean['median_predicted'] <- round(apply(results_predicted, 1, median, na.rm=TRUE), digits=0)
plot(results_mean)

################### CONFUSION MATRIX ###################
predictions <- tibble('target'=set$positionOrder, 'prediction'=results_mean$mean_predicted)
cf <- as_tibble(table(predictions))
plot_confusion_matrix(cf, target_col='target', prediction_col='prediction', counts_col='n', add_col_percentages=FALSE,add_normalized=FALSE,add_row_percentages=FALSE,palette='Reds')
