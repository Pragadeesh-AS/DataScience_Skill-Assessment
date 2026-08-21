import pandas as pd
import numpy as np
df = pd.read_csv("Q26_emergency_department.csv")
print(df.head())
print(df.info())
print(df.describe())
df['arrival_time'] = pd.to_datetime(
    df['arrival_time'], errors='coerce'
)
df['doctor_consultation_time'] = pd.to_datetime(
    df['doctor_consultation_time'], errors='coerce'
)
df['discharge_time'] = pd.to_datetime(
    df['discharge_time'], errors='coerce'
)
df = df.dropna(
    subset=[
        'arrival_time',
        'doctor_consultation_time',
        'discharge_time'
    ]
)
df = df.drop_duplicates(
    subset='patient_visit_id'
)
df['triage_category'] = (
    df['triage_category']
    .astype(str)
    .str.strip()
    .str.title()
)
df['total_hospital_time'] = (
    df['discharge_time'] -
    df['arrival_time']
).dt.total_seconds() / 60
df['total_waiting_time'] = (
    df['total_hospital_time'] -
    df['treatment_duration_min']
)
df = df[df['total_waiting_time'] >= 0]
df['emergency_priority'] = df['triage_category'].map({
    'Red': 'High',
    'Orange': 'Medium',
    'Yellow': 'Low'
})
df['weekday'] = df['arrival_time'].dt.day_name()
df['arrival_hour'] = df['arrival_time'].dt.hour
triage_wait = df.groupby(
    'triage_category'
)['total_waiting_time'].mean()

print("\nAverage Waiting Time by Triage Category:")
print(triage_wait)
weekday_wait = df.groupby(
    'weekday'
)['total_waiting_time'].mean()

print("\nAverage Waiting Time by Weekday:")
print(weekday_wait)
hour_wait = df.groupby(
    'arrival_hour'
)['total_waiting_time'].mean()
print("\nAverage Waiting Time by Arrival Hour:")
print(hour_wait)
print("\nEmergency Priority Category:")
print(df[
    [
        'patient_visit_id',
        'triage_category',
        'emergency_priority',
        'total_waiting_time'
    ]
])
excessive_wait = df[
    df['total_waiting_time'] > 60
]
print("\nPatients with Excessive Waiting:")
print(excessive_wait[
    [
        'patient_visit_id',
        'triage_category',
        'emergency_priority',
        'total_waiting_time'
    ]
])