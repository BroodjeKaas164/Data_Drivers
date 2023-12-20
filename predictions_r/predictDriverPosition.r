################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(quantregForest)
library(caret)
library(cvms)
library(tibble)

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_results.csv', 
                                   sep = ';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$resultsId, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### Train Models ###################
summary(model_qrf <- quantregForest(x = set, y = set$positionOrder, nthreads = 4))
summary(model_lm <- lm(positionOrder ~ points + grid + fastestLapSpeed + statusId, data=set))
summary(model_rf <- randomForest(positionOrder ~ points + grid + fastestLapSpeed + statusId, data=set, proximity=TRUE))

################### Make Predictions ###################
prediction_results <- data.frame(set$positionOrder)
names(prediction_results)[names(prediction_results)=='set.positionOrder'] <- 'pos_real'
prediction_results['pos_qrf'] <- data.frame(abs(round(predict(model_qrf, newdata=set), digits=0)))
prediction_results['pos_lm'] <- data.frame(abs(round(predict(model_lm, newdata=set), digits=0)))
prediction_results['pos_rf'] <- data.frame(abs(round(predict(model_rf, newdata=set), digits=0)))
# plot(prediction_results)

################### "Gecombineerd Gemiddelde" ###################
mean_results <- data.frame(set$positionOrder)
mean_results['pos_predicted'] <- abs(round(rowMeans(prediction_results, na.rm=TRUE), digits=0))
names(mean_results)[names(mean_results)=='set.positionOrder'] <- 'pos_real'
# plot(mean_results)

################### Confusion Matrix ###################
predictions <- tibble('target' = set$positionOrder, 'prediction' = mean_results$pos_predicted)
cf <- as_tibble(table(predictions))
plot_confusion_matrix(cf, 
                      target_col = 'target', 
                      prediction_col = 'prediction', 
                      counts_col = 'n', 
                      add_col_percentages = FALSE,
                      add_normalized = FALSE,
                      add_row_percentages = FALSE,
                      palette = 'Reds'
)


