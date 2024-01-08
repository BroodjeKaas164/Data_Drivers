################### DEFINE DATASETS ###################
data_splitter <- function(df_set, float_index, return_data=list()) {
  # Truncate empty values
  tempset <- na.omit(df_set)
  
  # Split data to traindata and testdata
  trainIndex <- try(createDataPartition(tempset[[p_factor]], p=float_index, list=FALSE))
  return_data[['trainers']] <- tempset[trainIndex,]
  return_data[['testers']] <- tempset[-trainIndex,]
  return(return_data)
}

################### PREDICTION RESULTS ###################
assign_results <- function(df_set, models, model_dict) {
  # Creating the table
  results_predicted <- data.frame(df_set[[p_factor]])
  names(results_predicted)[names(results_predicted)=='df_set..p_factor..'] <- 'real'
  
  # Predicts the outcome for all models trained
  for (model in models) {
    model_name <- paste0('model_', model)
    print(model_name)
    if(decimals < 0) {
      try(results_predicted[model] <- data.frame(abs(predict(model_dict[[model_name]], newdata=df_set))))
    } else {
      try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=df_set), digits=decimals))))
    }
  }
  
  # Show results
  print('Predicted results')
  print(summary(results_predicted))
  return(results_predicted)
}

################### COMBINED MEANDIAN ###################
combined_meandian <- function(df_set, trained_results) {
  # Creating the table
  results_mean <- data.frame(df_set[[p_factor]])
  names(results_mean)[names(results_mean)=='df_set..p_factor..'] <- 'real'

  # Calculates the statistics per predicted row for all models
  results_mean['p_mean'] <- rowMeans(trained_results, na.rm=TRUE)
  results_mean['p_median'] <-  apply(trained_results, 1, median, na.rm=TRUE)
  results_mean['p_var'] <- apply(trained_results, 1, var, na.rm=TRUE)
  results_mean['p_sd'] <-  apply(trained_results, 1, sd, na.rm=TRUE)
  
  # Show results
  print('Mean results')
  print(summary(results_mean))
  return(results_mean)
}

################### MODEL REWORK ###################
reworked_results <- function(df_set) {
  # Model based on the statistics of previous model outcomes
  temp_median <- combined_meandian(df_set, assign_results(df_set, use_models, trained_models))
  model_optimised <- try(train(real ~ p_mean + p_median + p_sd + p_var, data=temp_median, method=optimise_model))
  
  # Creating the table
  results_final <- data.frame(df_set[[p_factor]])
  names(results_final)[names(results_final)=='df_set..p_factor..'] <- 'real'
  if (decimals < 0) {
    try(results_final['p_optimised'] <- data.frame(abs(predict(model_optimised, newdata=temp_median))))
  } else {
    try(results_final['p_optimised'] <- data.frame(abs(round(predict(model_optimised, newdata=temp_median), digits=decimals))))
  }
  results_final['difference'] <- results_final$p_optimised - temp_median$real
  
  # Show results
  print('optimised results')
  print(summary(results_final))
  return(results_final)
}

################### CONFUSION MATRIX ###################
create_confusion_matrix <- function(df_set) {
  predictions <- tibble('target'=df_set$positionOrder, 'prediction'=reworked_results(df_set)$p_optimised)
  cf <- as_tibble(table(predictions))
  plot_confusion_matrix(cf, target_col='target', prediction_col='prediction', counts_col='n', add_col_percentages=FALSE, add_normalized=FALSE, add_row_percentages=FALSE, palette='Reds')
}
