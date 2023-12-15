if(!require('caret')) {
  install.packages('caret')
  library('caret')
}
if(!require('tidyverse')) {
  install.packages('tidyverse')
  library('tidyverse')
}

data(GermanCredit)

set.seed(200)
trainIndex <- createDataPartition(GermanCredit$Amount, p = 0.85, list=FALSE)
# Used in Confusion Matrices
train_data <- GermanCredit[trainIndex,]
test_data <- GermanCredit[-trainIndex,]

summary(model <- train(Amount ~ ., data=train_data, method="lm"))

predicted_creditscore <- data.frame(GermanCredit$Amount)
names(predicted_creditscore)[names(predicted_creditscore)=="GermanCredit.Amount"] <- "CS_amount"
predicted_creditscore['CS_predicted'] <- predict(model, newdata=GermanCredit)

plot(predicted_creditscore)

summary(linmod <- lm(CS_predicted ~ ., data=predicted_creditscore))
plot(linmod)
