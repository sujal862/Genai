import arrow  # Importing the Arrow library (better alternative to datetime)

# Get current UTC time (Coordinated Universal Time)
brewing_time = arrow.utcnow()

# Convert UTC time to Europe/Rome timezone
brewing_time.to("Europe/Rome")

print("UTC Time:", brewing_time)
print("Rome Time:", rome_time)