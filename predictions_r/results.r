if(!require('caret')) {
  install.packages('caret')
  library('caret')
}
if(!require('nnet')) {
  install.packages('nnet')
  library('nnet')
}
if(!require('tidyverse')) {
  install.packages('tidyverse')
  library('tidyverse')
}

dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_results.csv', 
                                   sep = ';')))
driver_standings <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_driver_standings.csv', 
                                            sep = ';')))

set.seed(40)
train_index <-  createDataPartition(dataset$resultId, p = 0.7, list = FALSE)
train_data <- dataset[train_index,]
test_data <- dataset[-train_index,]

# train_data_af_na <- train_data
train_data_af_na <- na.omit(train_data)
test_data_af_na <- na.omit(test_data)

################### Random Forest (rf) ###################
# summary(model_rf <- train(positionOrder ~ points + grid, data = train_data_af_na, method = 'rf'))
# saveRDS(model_rf, file = '/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_rf.rda')
model_rf <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_rf.rda')

################### Generalised Linear Model (glm) ###################
summary(model_glm <- train(positionOrder ~ points + grid, data = train_data_af_na, method = 'glm'))
saveRDS(model_glm, file = '/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_glm.rda')
model_glm <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_glm.rda')

################### Negative Binomial Generalized Linear Model (glm.nb) ###################
summary(model_glmnb <- train(positionOrder ~ points + grid, data = train_data_af_na, method = 'glm.nb'))
saveRDS(model_glmnb, file = '/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_glmnb.rda')
model_glmnb <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_glmnb.rda')

################### Parallel Random Forest (parRF) ###################
# summary(model_parRF <- train(positionOrder ~ points + grid, data = train_data_af_na, method = 'parRF'))
# saveRDS(model_parRF, file = '/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_parRF.rda')
model_parRF <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_parRF.rda')

################### Quantile Random Forest (qrf) ###################
# summary(model_qrf <- train(positionOrder ~ points + grid, data = train_data_af_na, method = 'qrf'))
# saveRDS(model_qrf, file = '/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_qrf.rda')
model_qrf <- readRDS('/Users/delano/Documents/GitHub/Data_Drivers/predictions_r/model_qrf.rda')

################### Predictions ###################
prediction_results <- data.frame(test_data_af_na$positionOrder)
names(prediction_results)[names(prediction_results)=='test_data_af_na.positionOrder'] <- 'pos_real'
prediction_results['pos_pred_rf'] <- predict(model_rf, newdata = test_data_af_na)
prediction_results['pos_pred_glm'] <- predict(model_glm, newdata = test_data_af_na)
prediction_results['pos_pred_glmnb'] <- predict(model_glmnb, newdata = test_data_af_na)
prediction_results['pos_pred_parRF'] <- predict(model_parRF, newdata = test_data_af_na)
prediction_results['pos_pred_qrf'] <- predict(model_qrf, newdata = test_data_af_na)

plot(prediction_results)

# confusionMatrix(predict(model_results, newdata = test_data), test_data$positionOrder)