# Assign Data
usedata <- data.frame(read.csv('/Users/delano/Library/CloudStorage/OneDrive-StichtingHogeschoolUtrecht/Jaar 2/Semester 3/Speedway Dynamics/Practice/clean_employee_sample_data.csv', sep = ';'))

summary(model_employees <- lm(Annual.Salary ~ Country + City + Age + Gender, data=usedata))
plot(model_employees)

# Barchart to visualise difference in count of Males to Females
barchart(usedata["Gender"], usedata["EEID"])