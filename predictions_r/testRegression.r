################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
source('predictions_r/sourceUsedLibraries.r', chdir=TRUE)
source('predictions_r/sourceModelFunctions.r', chdir=TRUE)

################### DEFINE PARAMETERS ###################
# SETTINGS
# TODO: Make train parameters dynamic if possible
set.seed(69)
use_models <- c('glm', 'glm.nb', 'lm')
optimise_model <- 'glm.nb'
decimals <- 2
p_factor <- 'Annual.Salary'

# Import datasets
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', sep=';')))
# dataset <- try(data.frame(read.csv('predictions_r/PseudoData.csv', sep=',')))
alldata <- data_splitter(dataset, 0.7)
trainers <- alldata[['trainers']]
testers <- alldata[['testers']]

################### EXPORT MODELFUNCTIONS HERE FOR EXTERNAL USE ###################
# @here

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
trained_models <- train_models(use_models, trainers)

################### PREDICTION RESULTS ###################
plot(trainResultsAssigned <- assign_results(trainers, use_models, trained_models))

################### COMBINED MEANDIAN ###################
plot(trainResultsMeandian <- combined_meandian(trainers, trainResultsAssigned))

################### MODEL REWORK ###################
plot(final <- reworked_results(dataset))
