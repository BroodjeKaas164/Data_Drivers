library(caret)

# Stap 3
set.seed(20)  # Voor reproduceerbaarheid
trainIndex <- createDataPartition(clean_constructor_standings$position, p = 0.8, list=FALSE)
train_data <- clean_constructor_standings[trainIndex, ]
test_data <- clean_constructor_standings[-trainIndex, ]

# Stap 4 | Voorbeeld: Train een beslissingsboommodel
model <- train(position ~ ., data=train_data, method="rpart")

# Stap 5
predictions <- predict(model, newdata=test_data)
confusionMatrix(predictions, test_data$Species)

# Stap 6 | Optioneel | Voorbeeld: Grid search voor hyperparameteroptimalisatie
grid <- expand.grid(cp=seq(0.01, 0.1, by = 0.01))
tuned_model <- train(Species ~ ., data = train_data, method="rpart", tuneGrid=grid)
