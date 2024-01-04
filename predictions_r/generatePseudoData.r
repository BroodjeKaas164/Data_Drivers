################### IMPORT LIBRARIES ###################
options(repos=c(CRAN="https://cloud.r-project.org"))

dataset <- try(data.frame(read.csv('data/clean_employee_sample_data.csv', 
                                   sep=';')))
dataset <- na.omit(dataset)

################### DEFINE PARAMETERS ###################
importset <- TRUE
new_size <- 10000

################### GET DATATYPES ###################
types <- data.frame(t(data.frame(sapply(dataset, class))))
rownames(types) <- NULL

################### CREATE PSEUDODATA ###################
new_data <- data.frame(sample(1:new_size, size=new_size))
names(new_data)[names(new_data)=='sample.1.new_size..size...new_size.'] <- 'newID'
new_data[order(new_data[['newID']], decreasing=FALSE),]

for (column_name in colnames(dataset)) {
  print(column_name)
  if (types[[column_name]]=='integer') {
    minimals <- min(dataset[[column_name]])
    maximals <- max(dataset[[column_name]])
    new_data[[column_name]] <- sample(minimals:maximals, size=nrow(new_data), replace=TRUE)
    print(summary(new_data[[column_name]]))
  }
  if (types[[column_name]]=='character') {
    unique_values <- unique(dataset[[column_name]])
    new_data[[column_name]] <- sample(unique_values, size=nrow(new_data), replace=TRUE)
  }
}
print(summary(new_data))
