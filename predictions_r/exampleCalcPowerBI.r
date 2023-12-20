library('caret')

# Maakt een samenvatting van het model waarin {}
# waarin position wordt voorspeld op basis van points, raceId, driverId uit de dataset clean_driver_standings
summary(model_driver <- lm(position ~ ., data=data.frame(read.csv("/Users/delano/Documents/GitHub/Data_Drivers/clean_driver_standings.csv", sep = ";"))))

# Formule om te gebruiken voor documentatie
# y = (xi*[wins])+(xi*[raceId])+...+{(intercept)}

# maakt een nieuw tabel
df_driver <- data.frame(coef(model_driver))

# Hernoemt de kolomnaam van coef.model. naar coefficentes
names(df_driver)[names(df_driver)=="coef.model."] <- "coefficients"

# Voegt een nieuwe kolom toe die de waarden van de rijnamen overneemt
df_driver['variables'] <- row.names(df_driver)

# Geeft een samenvatting van tabel df
summary(df_driver)

# Plot de models (volkomen onzin)
plot(model_driver)
