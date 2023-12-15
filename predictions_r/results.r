if(!require('caret')) {
  install.packages('caret')
  library('caret')
}

if(!require('nnet')) {
  install.packages('nnet')
  library('nnet')
}

if(!require('neuralnet')) {
  install.packages('neuralnet')
  library('neuralnet')
}

if(!require('randomGLM')) {
  install.packages('randomGLM')
  library('randomGLM')
}

dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/clean_results.csv', 
                                   sep = ';')))
driver_standings <- try(data.frame(read.csv('/Users/delano/Library/CloudStorage/OneDrive-StichtingHogeschoolUtrecht/Jaar 2/Semester 3/Speedway Dynamics/Speedway Dynamics - Datasemester/DATA/3_Cleaned/clean_driver_standings.csv', 
                                            sep = ';')))

set.seed(10)
train_index <-  createDataPartition(dataset$resultId, p = 0.7, list = FALSE)
train_data <- dataset[train_index,]
test_data <- dataset[-train_index,]

data_af_na <- na.omit(dataset)
model_results <- train(positionOrder ~ statusId + points + grid, data = data_af_na, method = 'lm')
summary(model_results)

results <- data.frame(data_af_na$positionOrder)
names(results)[names(results)=='data_af_na.positionOrder'] <- 'pos_real'
results['pos_pred'] <- predict(model_results, newdata = data_af_na)

plot(results)

confusionMatrix(predict(model_results, newdata = test_data), test_data$positionOrder)