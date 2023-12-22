################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))

################### DEFINE DATASETS ###################
dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
set <- na.omit(dataset)
trainIndex <- createDataPartition(set$resultId, p=0.7, list=FALSE)
trainData <- set[trainIndex,]
testData <- set[-trainIndex,]

################### TRAIN MODELS ###################

################### PREDICTION RESULTS ###################

################### COMBINED MEANDIAN ###################

################### CONFUSION MATRIX ###################
