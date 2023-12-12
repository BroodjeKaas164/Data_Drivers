# Maakt een samenvatting van het model waarin {}
# waarin position wordt voorspeld op basis van points, raceId, driverId uit de dataset clean_driver_standings
summary(model_driver <- lm(position ~ points + raceId + driverId, data=clean_driver_standings))
summary(model_constructors <- lm(position ~ wins + raceId + constructorId + points, data=clean_constructor_standings))

# Formule om te gebruiken voor documentatie
# y = (xi*[wins])+(xi*[raceId])+...+{(intercept)}

# maakt een nieuw tabel  
df_driver <- data.frame(coef(model_driver))
df_constructor <- data.frame(coef(model_constructors))

# Hernoemt de kolomnaam van coef.model. naar coefficentes
names(df_driver)[names(df_driver)=="coef.model."] <- "coefficients"
names(df_constructor)[names(df_constructor)=="coef.model."] <- "coefficients"

# Voegt een nieuwe kolom toe die de waarden van de rijnamen overneemt
df_driver['variables'] <- row.names(df_driver)
df_constructor['variables'] <- row.names((df_constructor))

# Geeft een samenvatting van tabel df
summary(df_driver)
summary(df_constructor)

# Plot de models (volkomen onzin)
plot(model_driver)
plot(model_constructors)