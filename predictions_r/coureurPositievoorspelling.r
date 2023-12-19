dataset <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_results.csv', 
                                   sep = ';')))
driver_standings <- try(data.frame(read.csv('/Users/delano/Documents/GitHub/Data_Drivers/data/clean_driver_standings.csv', 
                                            sep = ';')))

################### GECOMBINEERD GEMIDDELDE ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
library('quantregForest')
library('randomForest')

set <- na.omit(dataset)
model_qrf <- quantregForest(x = set, y = set$positionOrder, nthreads = 8)
model_lm <- lm(positionOrder ~ ., data=set)
model_rf <- randomForest(positionOrder ~ ., data=set, proximity=TRUE)

prediction_results <- data.frame(set$positionOrder)
names(prediction_results)[names(prediction_results)=='set.positionOrder'] <- 'pos_real'
summary(prediction_results['pos_qrf'] <- data.frame(abs(round(predict(model_qrf, newdata = set), digits = 0))))
summary(prediction_results['pos_lm'] <- data.frame(abs(round(predict(model_lm, newdata = set), digits = 0))))
summary(prediction_results['pos_rf'] <- data.frame(abs(round(predict(model_rf, newdata = set), digits = 0))))

mean_results <- data.frame(set$positionOrder)
mean_results$RowMeans <- abs(round(rowMeans(prediction_results, na.rm=TRUE), digits = 0))
names(mean_results)[names(mean_results)=='set.positionOrder'] <- 'pos_real'
names(mean_results)[names(mean_results)=='RowMeans'] <- 'pos_predicted'

plot(mean_results)
