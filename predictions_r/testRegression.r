################### IMPORT LIBRARIES ###################
options(repos = c(CRAN = "https://cloud.r-project.org"))
source('predictions_r/sourceUsedLibraries.r', chdir=TRUE)
source('predictions_r/sourceModelFunctions.r', chdir=TRUE)

################### DEFINE PARAMETERS ###################
# SETTINGS
# TODO: Make train parameters dynamic if possible
set.seed(69)
use_models <- c('glm', 'glm.nb', 'lm', 'parRF', 'qrf', 'bridge')
optimise_model <- 'glm.nb'
p_factor <- 'Annual.Salary'

# Import datasets
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
alldata <- data_splitter(dataset, 0.8)
trainers <- alldata[['trainers']]
testers <- alldata[['testers']]

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
plot(final <- reworked_results(testers))