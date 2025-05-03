from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import os

app = Flask(__name__)

# Load model and scaler
model = joblib.load('models/drug_use_model.pkl')
scaler = joblib.load('models/drug_use_scaler.pkl')

# Load feature names
with open('models/feature_names.json', 'r') as f:
    feature_names = json.load(f)

# Age mapping for visualization
age_groups = {
    0: '18-24',
    1: '25-34',
    2: '35-44',
    3: '45-54',
    4: '55-64',
    5: '65+'
}

# Gender mapping for visualization
gender_groups = {
    0: 'Female',
    1: 'Male'
}

@app.route('/')
def home():
    return render_template('index.html')

def load_data():
    """Load and prepare all data files for visualizations"""
    data = {}
    
    # Check if data directory exists
    if not os.path.exists('data'):
        # Return sample data if no data directory
        return {
            'age_distribution': pd.DataFrame({
                'Age': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
                'Non-users': [47, 117, 138, 169, 53, 16],
                'Users': [539, 324, 199, 116, 38, 2]
            }),
            'gender_distribution': pd.DataFrame({
                'Gender': ['Female', 'Male'],
                'Non-users': [280, 260],
                'Users': [545, 673]
            }),
            'feature_correlations': pd.Series({
                'SS': 0.42, 'Impulsive': 0.38, 'Nscore': 0.21, 
                'Escore': 0.19, 'Age': -0.35, 'Education': -0.12,
                'Mental health level': 0.28
            }),
        }

    data_files = {
        'age_distribution': 'data/age_distribution.csv',
        'gender_distribution': 'data/gender_distribution.csv',
        'education_distribution': 'data/education_distribution.csv',
        'mental_health_distribution': 'data/mental_health_distribution.csv',
        'feature_correlations': 'data/feature_correlations.csv',
    }
    
    data = {}
    
    # Load age data and convert numeric indices to meaningful labels
    if os.path.exists(data_files['age_distribution']):
        df_age = pd.read_csv(data_files['age_distribution'])
        
        # Check if the CSV format matches what you described
        # Your format: Age,Non-users,Users with Age being numeric codes
        if 'Age' in df_age.columns:
            # Convert numeric age codes to readable labels
            df_age['Age'] = df_age['Age'].astype(int).map(age_groups)
            data['age_distribution'] = df_age
        else:
            # Try to handle other possible formats
            if 'Unnamed: 0' in df_age.columns:
                df_age = df_age.rename(columns={'Unnamed: 0': 'Age'})
                if df_age['Age'].dtype != 'object':
                    df_age['Age'] = df_age['Age'].astype(int).map(age_groups)
            data['age_distribution'] = df_age
    
    # Load gender data and convert indices
    if os.path.exists(data_files['gender_distribution']):
        df_gender = pd.read_csv(data_files['gender_distribution'])
        if 'Gender' in df_gender.columns:
            # Convert numeric gender codes to text labels
            if df_gender['Gender'].dtype != 'object':
                df_gender['Gender'] = df_gender['Gender'].astype(int).map(gender_groups)
            data['gender_distribution'] = df_gender
        else:
            # Try to handle other possible formats
            if 'Unnamed: 0' in df_gender.columns:
                df_gender = df_gender.rename(columns={'Unnamed: 0': 'Gender'})
                if df_gender['Gender'].dtype != 'object':
                    df_gender['Gender'] = df_gender['Gender'].astype(int).map(gender_groups)
            data['gender_distribution'] = df_gender
    
    # Load education data
    if os.path.exists(data_files['education_distribution']):
        df_education = pd.read_csv(data_files['education_distribution'])
        # Map education levels
        education_mapping = {
            0: 'Left school before 16',
            1: 'Left school at 16',
            2: 'Left school at 17',
            3: 'Left school at 18',
            4: 'Some college',
            5: 'Professional certificate',
            6: 'University degree',
            7: 'Masters degree',
            8: 'Doctorate degree'
        }
        
        if 'Education' in df_education.columns:
            if df_education['Education'].dtype != 'object':
                df_education['Education'] = df_education['Education'].astype(int).map(education_mapping)
        elif 'Unnamed: 0' in df_education.columns:
            df_education = df_education.rename(columns={'Unnamed: 0': 'Education'})
            if df_education['Education'].dtype != 'object':
                df_education['Education'] = df_education['Education'].astype(int).map(education_mapping)
                
        data['education_distribution'] = df_education
    
    # Load mental health data
    if os.path.exists(data_files['mental_health_distribution']):
        df_mental = pd.read_csv(data_files['mental_health_distribution'])
        # Map mental health levels
        mental_health_mapping = {
            1: 'Low',
            2: 'Medium-Low',
            3: 'Medium-High',
            4: 'High'
        }
        
        if 'Mental health level' in df_mental.columns:
            if df_mental['Mental health level'].dtype != 'object':
                df_mental['Mental health level'] = df_mental['Mental health level'].astype(int).map(mental_health_mapping)
        elif 'Unnamed: 0' in df_mental.columns:
            df_mental = df_mental.rename(columns={'Unnamed: 0': 'Mental health level'})
            if df_mental['Mental health level'].dtype != 'object':
                df_mental['Mental health level'] = df_mental['Mental health level'].astype(int).map(mental_health_mapping)
                
        data['mental_health_distribution'] = df_mental
    
    # Load correlation data
    if os.path.exists(data_files['feature_correlations']):
        df_corr = pd.read_csv(data_files['feature_correlations'])
        # Convert to Series
        if len(df_corr.columns) >= 2:
            feature_name_col = df_corr.columns[0]
            correlation_col = df_corr.columns[1]
            corr_series = pd.Series(df_corr[correlation_col].values, index=df_corr[feature_name_col])
            data['feature_correlations'] = corr_series.sort_values(ascending=False)
    
    return data

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Collect form data
            form_data = {}
            for feature in feature_names:
                if feature in request.form:
                    value = request.form[feature]
                    try:
                        # Convert to number if possible
                        value = float(value)
                    except ValueError:
                        pass
                    form_data[feature] = value
                else:
                    return jsonify({'error': f'Missing feature: {feature}'}), 400
            
            # Prepare data for prediction
            input_df = pd.DataFrame([form_data])
            
            # Ensure columns are in the right order
            input_df = input_df[feature_names]
            
            # Scale data
            input_scaled = scaler.transform(input_df)
            
            # Make prediction
            prediction = model.predict(input_scaled)[0]
            prediction_proba = model.predict_proba(input_scaled)[0][1]
            
            # Prepare result
            result = {
                'prediction': int(prediction),
                'probability': float(prediction_proba),
                'risk_level': 'High' if prediction_proba > 0.75 else 'Medium' if prediction_proba > 0.5 else 'Low'
            }
            
            return render_template('predict.html', result=result, form_data=form_data)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # If GET method, display the form
    return render_template('predict.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Get JSON data
        data = request.json
        
        # Check if all required features are available
        for feature in feature_names:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
        
        # Prepare data for prediction
        input_df = pd.DataFrame([data])
        
        # Ensure columns are in the right order
        input_df = input_df[feature_names]
        
        # Scale data
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0][1]
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'probability': float(prediction_proba),
            'risk_level': 'High' if prediction_proba > 0.75 else 'Medium' if prediction_proba > 0.5 else 'Low'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize')
def visualize():
    # Load all the data
    all_data = load_data()
    
    # Create age distribution visualization
    if 'age_distribution' in all_data:
        df_age = all_data['age_distribution']
        # Melt the dataframe for Plotly Express
        df_age_melt = pd.melt(df_age, id_vars=['Age'], var_name='User_Type', value_name='Count')
        # Create the figure
        fig_age = px.bar(
            df_age_melt, 
            x='Age', 
            y='Count', 
            color='User_Type',
            title='Distribution of Drug Users by Age Group',
            barmode='group',
            color_discrete_map={'Users': 'rgba(187, 134, 252, 0.8)', 'Non-users': 'rgba(3, 218, 198, 0.8)'}
        )
        # Update layout for dark theme
        fig_age.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    else:
        # Create sample visualization if data is not available
        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(
            x=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            y=[539, 324, 199, 116, 38, 2],
            name='Users',
            marker_color='rgba(187, 134, 252, 0.8)'
        ))
        fig_age.add_trace(go.Bar(
            x=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            y=[47, 117, 138, 169, 53, 16],
            name='Non-users',
            marker_color='rgba(3, 218, 198, 0.8)'
        ))
        fig_age.update_layout(
            title='Distribution of Drug Users by Age Group',
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    
    # Create gender distribution visualization
    if 'gender_distribution' in all_data:
        df_gender = all_data['gender_distribution']
        # Melt the dataframe for Plotly Express
        df_gender_melt = pd.melt(df_gender, id_vars=['Gender'], var_name='User_Type', value_name='Count')
        # Create the figure
        fig_gender = px.bar(
            df_gender_melt, 
            x='Gender', 
            y='Count', 
            color='User_Type',
            title='Distribution of Drug Users by Gender',
            barmode='group',
            color_discrete_map={'Users': 'rgba(187, 134, 252, 0.8)', 'Non-users': 'rgba(3, 218, 198, 0.8)'}
        )
        # Update layout for dark theme
        fig_gender.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    else:
        # Create sample visualization if data is not available
        fig_gender = go.Figure()
        fig_gender.add_trace(go.Bar(
            x=['Female', 'Male'],
            y=[545, 673],
            name='Users',
            marker_color='rgba(187, 134, 252, 0.8)'
        ))
        fig_gender.add_trace(go.Bar(
            x=['Female', 'Male'],
            y=[280, 260],
            name='Non-users',
            marker_color='rgba(3, 218, 198, 0.8)'
        ))
        fig_gender.update_layout(
            title='Distribution of Drug Users by Gender',
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    
    # Create feature correlation visualization
    if 'feature_correlations' in all_data:
        corr_series = all_data['feature_correlations']
        
        # Get the top correlations (positive and negative)
        # Sort by absolute value to get features with strongest correlation (positive or negative)
        top_correlations = corr_series.abs().sort_values(ascending=False).head(10)
        # Get the original values for these features
        top_corr_features = corr_series[top_correlations.index]
        
        # Create color list for bars (positive = purple, negative = red)
        colors = ['rgba(187, 134, 252, 0.8)' if val > 0 else 'rgba(207, 102, 121, 0.8)' 
                 for val in top_corr_features]
        
        # Create the figure
        fig_corr = go.Figure()
        fig_corr.add_trace(go.Bar(
            x=top_corr_features.index,
            y=top_corr_features.values,
            marker_color=colors
        ))
        fig_corr.update_layout(
            title='Feature Correlations with Drug Use',
            xaxis_tickangle=-45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    else:
        # Create sample correlation visualization if data is not available
        fig_corr = go.Figure()
        fig_corr.add_trace(go.Bar(
            x=['SS', 'Impulsive', 'Nscore', 'Mental health level', 'Escore', 'Cscore', 'Education', 'Age'],
            y=[0.42, 0.38, 0.21, 0.28, 0.19, -0.08, -0.12, -0.35],
            marker_color=['rgba(187, 134, 252, 0.8)', 'rgba(187, 134, 252, 0.8)', 
                         'rgba(187, 134, 252, 0.8)', 'rgba(187, 134, 252, 0.8)',
                         'rgba(187, 134, 252, 0.8)', 'rgba(207, 102, 121, 0.8)',
                         'rgba(207, 102, 121, 0.8)', 'rgba(207, 102, 121, 0.8)']
        ))
        fig_corr.update_layout(
            title='Feature Correlations with Drug Use',
            xaxis_tickangle=-45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'}
        )
    
    # Convert figures to JSON for the template
    graph_json = json.dumps(fig_age, cls=plotly.utils.PlotlyJSONEncoder)
    gender_json = json.dumps(fig_gender, cls=plotly.utils.PlotlyJSONEncoder)
    corr_json = json.dumps(fig_corr, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('visualize.html', 
                          graphJSON=graph_json,
                          genderJSON=gender_json,
                          corrJSON=corr_json)

if __name__ == '__main__':
    app.run(debug=True)