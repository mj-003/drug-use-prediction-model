# Drug Consumption Analysis and Prediction Project

## Demo Video


https://github.com/user-attachments/assets/463c9a54-6068-44ef-a852-bc7276e21b3d


## Project Overview
This project aims to explore data analysis methods in the context of drug use, utilizing advanced predictive models based on demographic, personality, and mental health-related data. We analyze these factors and their interconnections to identify determinants of drug use risk and predict such behavior based on available features.

### The project combines:

- Data analysis and visualization of drug consumption patterns
- Predictive modeling using machine learning algorithms
- Interactive web application for showcasing results and making predictions

The machine learning model developed through this research achieves over 80% accuracy in classifying drug users versus non-users based on personality traits and other factors.

## Web Application
The project includes a complete web application built with Flask that allows:

- Prediction Interface: Input demographic and personality trait information to receive a risk assessment
- Data Visualization: Interactive charts showing drug use patterns across different demographics and personality traits
- Profile Analysis: Synthetic user profile generation and visualization

## Dataset
The model uses data including:

- Demographics (age, gender, education, country)
- Big Five personality traits (Neuroticism, Extraversion, Openness, Agreeableness, Conscientiousness)
- Impulsivity and Sensation Seeking scores
- Mental health indicators by age group
- Drug consumption history across three categories (opioids, ecstasy, benzodiazepines)

## Libraries and Technologies Used
### Backend

- Python - Core programming language
- NumPy - Numerical operations and handling arrays/matrices
- Pandas - Data manipulation and analysis
- Flask - Web application framework
- Joblib - Model serialization

### Machine Learning

- Scikit-learn - Feature processing, model evaluation, and utilities
- XGBoost - Gradient boosting implementation for classification
- TensorFlow/Keras - Neural network implementation (alternative model)

### Frontend

- HTML/CSS/JavaScript - Web interface structure and styling
- Bootstrap - Responsive design components
- Plotly.js - Interactive data visualizations
- Font Awesome - Icon library
