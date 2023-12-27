################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
source('predictions_r/sourceUsedLibraries.r', chdir=TRUE)
source('predictions_r/sourceModelFunctions.r', chdir=TRUE)

################### DEFINE DATASETS ###################
# Import Datasets
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
set.seed(69)

# Split datasets
trainIndex <- createDataPartition(set$Gender, p=0.75, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### DEFINE PARAMETERS ###################
# SETTINGS
# TODO: Make train parameters dynamic if possible
models <- c('glm', 'glm.nb', 'lm', 'parRF', 'qrf', 'bridge', 'leapForward', 'leapBackward')
optimiseModel <- 'glm.nb'
p_factor <- 'Annual.Salary'

################### TRAIN MODELS ###################
train_models <- function(models, trainData, model_dict=list()) {
  for (model in models) {
    model_name <- paste0('model_', model)
    print(model_name)
    model <- try(train(Annual.Salary ~ Gender + Age + Department, data=trainData, method=model))
    try(model_dict[[model_name]] <- model)
    print(summary(model))
  }
  return(model_dict)
}

################### PREDICTION RESULTS ###################
plot(resultsPhase1 <- assign_results(models, set, train_models(models, set)))

################### COMBINED MEANDIAN ###################
plot(resultsMeandian <- combined_meandian(set, p_factor, resultsPhase1))

################### MODEL REWORK ###################
trainIndexOptimised <- createDataPartition(resultsMeandian$real, p=0.5, list=FALSE)
trainDataOptimised <- resultsMeandian[trainIndexOptimised,]

model_optimised <- try(train(real ~ p_mean + p_median + p_sd + p_var, data=trainDataOptimised, method=optimiseModel))

reworked_results <- function(df_set, p_factor) {
  results_final <- data.frame(df_set[[as.character(p_factor)]])
  names(results_final)[names(results_final)=='df_set..as.character.p_factor...'] <- 'real'
  results_final['p_optimised'] <- try(data.frame(round(predict(model_optimised, newdata=resultsMeandian), digits=0)))
  results_final['difference'] <- results_final$p_optimised - resultsMeandian$real
  print(summary(results_final))
  return(results_final)
}
plot(final <- reworked_results(set, p_factor))

################### SHOW RESULTS ###################
predicted_difference <- data.frame(set$Annual.Salary)
names(predicted_difference)[names(predicted_difference)=='set.Annual.Salary'] <- 'real'
predicted_difference['predicted'] <- final$p_optimised
