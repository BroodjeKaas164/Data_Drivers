if(!require('caret')) {
  install.packages('caret')
  library('caret')
}

dataset <- data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/clean_results.csv', 
                               sep = ';'))

set.seed(30)
train_index <-  createDataPartition(dataset$resultId, p = 0.7, list = FALSE)
train_data <- dataset[train_index,]
test_data <- dataset[-train_index,]

na.omit(dataset)
options('na.action')
model <- train(na.pass(position ~ position + raceId + driverId, 
                       data = train_data, 
                       method = 'glm'))
