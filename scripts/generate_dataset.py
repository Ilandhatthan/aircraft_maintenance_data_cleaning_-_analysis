import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Seed
random.seed(42)
np.random.seed(42)

n_records = 5000

# Intentionally messy categorical values
aircraft_types = ['B737', 'A320', 'B777', 'A350', 'B787', 'b737', 'A-320']
maintenance_types = ['Scheduled', 'Unscheduled', 'Emergency', 'Preventive', 'scheduled']
maintenance_categories = ['Engine', 'Avionics', 'LandingGear', 'Hydraulics', 'Electrical', 'Structure']
vendors = ['V-A', 'V-B', 'V-C', 'InHouse', 'inhouse']
priorities = ['Critical', 'High', 'Medium', 'Low']
status = ['Completed', 'InProgress', 'Delayed', 'Cancelled', 'completed']

# 15 CITIES (GLOBAL FOCUS, FEW INDIAN)
locations = [
    'NewYork', 'LosAngeles', 'Chicago', 'Dallas', 'Atlanta',
    'London', 'Paris', 'Frankfurt', 'Amsterdam',
    'Dubai', 'Singapore', 'Tokyo',
    'Toronto',
    'Chennai', 'Mumbai'
]

data = []

for i in range(n_records):
    scheduled_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
    actual_start = scheduled_date + timedelta(days=random.randint(-3, 12))
    completion = actual_start + timedelta(hours=random.randint(3, 150))

    budgeted = random.randint(5000, 150000)
    actual = int(budgeted * random.uniform(0.7, 1.5))

    row = {
        'Maintenance_ID': f'M{str(i+1).zfill(3)}',
        'Aircraft_ID': f'A{random.randint(1, 60):02}',
        'Aircraft_Type': random.choice(aircraft_types),
        'Maintenance_Type': random.choice(maintenance_types),
        'Maintenance_Category': random.choice(maintenance_categories),
        'Scheduled_Date': scheduled_date.strftime('%Y-%m-%d'),
        'Actual_Start_Date': actual_start.strftime('%Y-%m-%d'),
        'Completion_Date': completion.strftime('%Y-%m-%d'),
        'Budgeted_Cost': budgeted,
        'Actual_Cost': actual,
        'Labor_Hours': random.randint(5, 220),
        'Parts_Cost': random.randint(1000, 90000),
        'Vendor': random.choice(vendors),
        'Priority': random.choice(priorities),
        'Status': random.choice(status),
        'Location': random.choice(locations),
        'Downtime_Hours': random.randint(5, 150),
        'Technician_Count': random.randint(1, 10),
        'Cost_Variance': actual - budgeted,
        'Cost_Variance_Percent': round(((actual - budgeted) / budgeted) * 100, 2)
    }

    data.append(row)

df = pd.DataFrame(data)

# Add missing values (25–40%)
columns_to_null = df.columns.tolist()[2:]

for col in columns_to_null:
    null_ratio = random.uniform(0.25, 0.40)
    null_rows = random.sample(range(len(df)), int(len(df) * null_ratio))
    df.loc[null_rows, col] = np.nan

# Add duplicates (800)
duplicates = df.sample(800, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Info
print("=" * 60)
print("UNCLEANED AIRCRAFT MAINTENANCE DATASET (15 CITIES)")
print("=" * 60)
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nMissing values per column:")
print(df.isnull().sum())

# Save files
df.to_csv("aircraft_maintenance_uncleaned.csv", index=False)
df.to_excel("aircraft_maintenance_uncleaned.xlsx", index=False)

print("\nFILES SAVED:")
print("✓ aircraft_maintenance_uncleaned.csv")
print("✓ aircraft_maintenance_uncleaned.xlsx")
