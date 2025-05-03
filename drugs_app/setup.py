"""
Script to set up the project directory structure for the Drug Analysis web application.
"""

import os
import shutil

def create_directory_structure():
    """Create the basic directory structure for the project."""
    # Create the main directories
    directories = [
        'models',
        'data',
        'static/css',
        'static/js',
        'static/img',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_sample_csv():
    """Create sample CSV files for testing."""
    # Age distribution data
    age_csv = """Age,Non-users,Users
0,47,539
1,117,324
2,138,199
3,169,116
4,53,38
5,16,2
"""
    
    # Gender distribution data
    gender_csv = """Gender,Non-users,Users
0,280,545
1,260,673
"""
    
    # Feature correlations data
    correlations_csv = """Feature,Correlation
SS,0.42
Impulsive,0.38
Nscore,0.21
Mental health level,0.28
Escore,0.19
Cscore,-0.08
Education,-0.12
Age,-0.35
"""
    
    # Write the files
    with open('data/age_distribution.csv', 'w') as f:
        f.write(age_csv)
    
    with open('data/gender_distribution.csv', 'w') as f:
        f.write(gender_csv)
    
    with open('data/feature_correlations.csv', 'w') as f:
        f.write(correlations_csv)
    
    print("Created sample CSV files in data directory.")

def create_sample_model_files():
    """Create placeholder files for the models."""
    # Sample feature names JSON
    feature_names = """[
    "Age", 
    "Gender", 
    "Education", 
    "Country", 
    "Ethnicity", 
    "Nscore", 
    "Escore", 
    "Oscore", 
    "AScore", 
    "Cscore", 
    "Impulsive",
    "SS",
    "Mental health level"
]"""
    
    with open('models/feature_names.json', 'w') as f:
        f.write(feature_names)
    
    print("Created placeholder model files in models directory.")

def copy_files():
    """Copy the app files to the correct locations."""
    # Define source files and their destinations
    files = {
        'app.py': './',
        'updated_script.js': 'static/js/script.js',
        'style.css': 'static/css/style.css',
        'index.html': 'templates/index.html',
        'predict.html': 'templates/predict.html',
        'updated_visualize.html': 'templates/visualize.html'
    }
    
    # Create a placeholder for missing files
    for dest in files.values():
        dir_path = os.path.dirname(dest)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
    
    # If the file exists in the current directory, copy it
    for source, dest in files.items():
        if os.path.exists(source):
            shutil.copy(source, dest)
            print(f"Copied {source} to {dest}")
        else:
            print(f"Warning: Source file {source} not found, skipping")

def main():
    print("Setting up project directory structure...")
    create_directory_structure()
    create_sample_csv()
    create_sample_model_files()
    copy_files()
    print("\nProject setup complete!")
    print("\nNote: You will need to have model files (drug_use_model.pkl and drug_use_scaler.pkl) in the models directory.")
    print("To run the application, execute: python app.py")

if __name__ == "__main__":
    main()