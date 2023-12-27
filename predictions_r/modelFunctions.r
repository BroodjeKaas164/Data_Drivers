################### PREDICTION RESULTS ###################
# TODO?: remove real values from set?
assign_results <- function(char_models, df_dataset, model_dict) {
  results_predicted <- data.frame(real_values)
  names(results_predicted)[names(results_predicted)=='real_values'] <- 'real'
  
  for (model in char_models) {
    model_name <- paste0('model_', model)
    print(model_name)
    try(results_predicted[model] <- data.frame(abs(round(predict(model_dict[[model_name]], newdata=df_dataset), digits=0))))
  }
  print(summary(results_predicted))
  return(results_predicted)
}

################### COMBINED MEANDIAN ###################
combined_meandian <- function(df_set, p_factor, trained_results) {
  results_mean <- data.frame(df_set[[as.character(p_factor)]])
  names(results_mean)[names(results_mean)=='df_set..as.character.p_factor...'] <- 'real'
  results_mean['p_mean'] <- abs(round(rowMeans(trained_results, na.rm=TRUE), digits=0))
  results_mean['p_median'] <-  round(apply(trained_results, 1, median, na.rm=TRUE), digits=0)
  results_mean['p_sd'] <-  apply(trained_results, 1, sd, na.rm=TRUE)
  results_mean['p_var'] <- apply(trained_results, 1, var, na.rm=TRUE)
  print(summary(results_mean))
  return(results_mean)
}

################### MODEL REWORK ###################
