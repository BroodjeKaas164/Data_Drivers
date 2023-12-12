# Assign Data
usedata <- clean_employee_sample_data

table(summary(model_employees <- lm(Annual.Salary ~ Gender, data=usedata)))
plot(model_employees)

# Barchart to visualise difference in count of Males to Females
barchart(usedata["Gender"], usedata["EEID"])