import pandas as pd
import numpy as np

data = {
    'Name': ['Anu', 'Rahul', 'Priya', 'Kiran', 'Meena'],
    'Age': [25, 30, 22, 28, 24],
    'Department': ['AI', 'CSE', 'AI', 'ECE', 'CSE'],
    'Marks': [85, 90, 78, 92, 88]
}

df = pd.DataFrame(data)

print(" First 5 Rows of the Dataset:")
print(df.head())

print("\n Summary Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())

print("\n Unique Departments:")
print(df['Department'].unique())

df['Grade'] = np.where(df['Marks'] >= 90, 'A',
                       np.where(df['Marks'] >= 80, 'B', 'C'))

ai_students = df[df['Department'] == 'AI']
sorted_df = df.sort_values(by='Marks', ascending=False)

print("\n Data with New Grade Column:")
print(df)

print("\n Students from AI Department:")
print(ai_students)

print("\n Students Sorted by Marks:")
print(sorted_df)
