import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# style for the plots
plt.style.use('seaborn-v0_8')

# Task 1: Load and Explore the Dataset
print("TASK 1: LOADING AND EXPLORING THE DATASET")
print("-----------------------------------------")

try:
    # Load the Iris dataset from sklearn
    iris = load_iris()
    
    # Create a DataFrame with the iris data
    # Add column names from the dataset feature_names
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    
    # Add a 'species' column using the target and target_names
    df['species'] = [iris.target_names[i] for i in iris.target]
    
    print("Dataset loaded successfully!\n")
    
    # Display the first 5 rows of the dataset
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\n")
    
    # Check the structure of the dataset
    print("Dataset structure:")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    print("\n")
    
    # Check data types
    print("Data types:")
    print(df.dtypes)
    print("\n")
    
    # Check for missing values
    print("Missing values:")
    print(df.isnull().sum())
    print("\n")
    
    # Create a copy of the DataFrame to avoid modifying the original
    df_with_missing = df.copy()
    
    # Introduce some missing values randomly
    np.random.seed(42)
    for col in df.columns:
        mask = np.random.rand(len(df)) < 0.05  # 5% of values will be NaN
        df_with_missing.loc[mask, col] = np.nan
    
    print("After introducing some missing values:")
    print(df_with_missing.isnull().sum())
    print("\n")
    
    # Clean the dataset by filling missing values
    # For numerical columns, fill with mean
    for col in df_with_missing.select_dtypes(include='number').columns:
        df_with_missing[col].fillna(df_with_missing[col].mean(), inplace=True)
    
    # For categorical columns, fill with the most frequent value
    for col in df_with_missing.select_dtypes(include='object').columns:
        df_with_missing[col].fillna(df_with_missing[col].mode()[0], inplace=True)
    
    print("After cleaning missing values:")
    print(df_with_missing.isnull().sum())
    print("\n")
    
    # Task 2: Basic Data Analysis
    print("TASK 2: BASIC DATA ANALYSIS")
    print("--------------------------")
    
    # Compute basic statistics
    print("Basic statistics of numerical columns:")
    print(df.describe())
    print("\n")
    
    # Group by species and compute mean for each group
    print("Mean values grouped by species:")
    species_group = df.groupby('species').mean()
    print(species_group)
    print("\n")
    
    # Identify patterns or interesting findings
    print("Interesting findings:")
    print("- Setosa species has the smallest petal length and width but largest sepal width.")
    print("- Virginica species has the largest petal and sepal dimensions overall.")
    print("- Versicolor falls in the middle for most measurements.")
    print("\n")
    
    # Task 3: Data Visualization
    print("TASK 3: DATA VISUALIZATION")
    print("-------------------------")
    
    # Create a figure for all the plots
    plt.figure(figsize=(20, 15))
    
    # 1. Line Chart: Create a time-series-like visualization
    # We'll use the index as a proxy for time to demonstrate a line chart
    plt.subplot(2, 2, 1)
    
    # Get average measurements for each species and create an index for "time"
    df_avg_by_species = df.groupby('species').mean().reset_index()
    measurements = df_avg_by_species.columns[1:]  # Exclude 'species' column
    
    for species in df_avg_by_species['species']:
        species_data = df_avg_by_species[df_avg_by_species['species'] == species]
        plt.plot(measurements, species_data[measurements].values[0], marker='o', label=species)
    
    plt.title('Average Measurements by Species', fontsize=14)
    plt.xlabel('Measurement Type', fontsize=12)
    plt.ylabel('Value (cm)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 2. Bar Chart: Compare average sepal length across species
    plt.subplot(2, 2, 2)
    avg_sepal_length = df.groupby('species')['sepal length (cm)'].mean()
    
    bars = plt.bar(avg_sepal_length.index, avg_sepal_length.values, color=['blue', 'green', 'red'])
    plt.title('Average Sepal Length by Species', fontsize=14)
    plt.xlabel('Species', fontsize=12)
    plt.ylabel('Average Sepal Length (cm)', fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{height:.2f}', ha='center', va='bottom')
    
    # 3. Histogram: Distribution of petal length
    plt.subplot(2, 2, 3)
    for species, color in zip(iris.target_names, ['blue', 'green', 'red']):
        plt.hist(df[df['species'] == species]['petal length (cm)'], 
                 bins=10, alpha=0.5, label=species, color=color)
    
    plt.title('Distribution of Petal Length', fontsize=14)
    plt.xlabel('Petal Length (cm)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 4. Scatter Plot: Relationship between sepal length and petal length
    plt.subplot(2, 2, 4)
    for species, color in zip(iris.target_names, ['blue', 'green', 'red']):
        species_data = df[df['species'] == species]
        plt.scatter(species_data['sepal length (cm)'], species_data['petal length (cm)'], 
                   label=species, color=color, alpha=0.7)
    
    plt.title('Sepal Length vs. Petal Length', fontsize=14)
    plt.xlabel('Sepal Length (cm)', fontsize=12)
    plt.ylabel('Petal Length (cm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig('iris_data_visualizations.png')
    
    print("Data visualizations created successfully!")
    print("All visualizations have been saved as 'iris_data_visualizations.png'")
    
except Exception as e:
    print(f"An error occurred: {e}")
