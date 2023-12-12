# Source: ChatGPT
# Stap 1
# install.packages("caret")
library(caret)

# Stap 2 | Voorbeeld: Laad een dataset (bijv. iris-dataset)
data(iris) # Voorbeeld dataset

# Stap 3
set.seed(20)  # Voor reproduceerbaarheid
trainIndex <- createDataPartition(iris$Species, p = 0.8, list=FALSE)
train_data <- iris[trainIndex, ]
test_data <- iris[-trainIndex, ]

# Stap 4 | Voorbeeld: Train een beslissingsboommodel
model <- train(Species ~ ., data=train_data, method="rpart")

# Stap 5
predictions <- predict(model, newdata=test_data)
confusionMatrix(predictions, test_data$Species)

# Stap 6 | Optioneel | Voorbeeld: Grid search voor hyperparameteroptimalisatie
grid <- expand.grid(cp=seq(0.01, 0.1, by = 0.01))
tuned_model <- train(Species ~ ., data = train_data, method="rpart", tuneGrid=grid)
