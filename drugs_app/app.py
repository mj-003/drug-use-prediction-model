from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go


app = Flask(__name__)

# Wczytanie modelu i skalera
model = joblib.load('models/drug_use_model.pkl')
scaler = joblib.load('models/drug_use_scaler.pkl')

# Wczytanie nazw cech
with open('models/feature_names.json', 'r') as f:
    feature_names = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Zbieranie danych z formularza
            form_data = {}
            for feature in feature_names:
                if feature in request.form:
                    value = request.form[feature]
                    try:
                        # Konwersja na liczbę, jeśli to możliwe
                        value = float(value)
                    except ValueError:
                        pass
                    form_data[feature] = value
                else:
                    return jsonify({'error': f'Brakująca cecha: {feature}'}), 400
            
            # Przygotowanie danych do predykcji
            input_df = pd.DataFrame([form_data])
            
            # Upewnienie się, że kolumny są w prawidłowej kolejności
            input_df = input_df[feature_names]
            
            # Skalowanie danych
            input_scaled = scaler.transform(input_df)
            
            # Predykcja
            prediction = model.predict(input_scaled)[0]
            prediction_proba = model.predict_proba(input_scaled)[0][1]
            
            # Przygotowanie wyniku
            result = {
                'prediction': int(prediction),
                'probability': float(prediction_proba),
                'risk_level': 'High' if prediction_proba > 0.75 else 'Medium' if prediction_proba > 0.5 else 'Low'
            }
            
            return render_template('predict.html', result=result, form_data=form_data)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Jeśli metoda GET, wyświetl formularz
    return render_template('predict.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Pobranie danych JSON
        data = request.json
        
        # Sprawdzenie, czy wszystkie wymagane cechy są dostępne
        for feature in feature_names:
            if feature not in data:
                return jsonify({'error': f'Brakująca cecha: {feature}'}), 400
        
        # Przygotowanie danych do predykcji
        input_df = pd.DataFrame([data])
        
        # Upewnienie się, że kolumny są w prawidłowej kolejności
        input_df = input_df[feature_names]
        
        # Skalowanie danych
        input_scaled = scaler.transform(input_df)
        
        # Predykcja
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0][1]
        
        # Przygotowanie odpowiedzi
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
    # Tutaj możesz dodać kod do generowania wykresów
    # Przykład z Plotly
    
    # Dane przykładowe (zastąp swoimi)
    age_data = {
        'Age': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
        'User_Count': [320, 280, 210, 150, 90, 50],
        'NonUser_Count': [100, 130, 190, 220, 280, 310]
    }
    
    df_age = pd.DataFrame(age_data)
    df_age_melt = df_age.melt(id_vars=['Age'], var_name='User_Type', value_name='Count')
    
    fig = px.bar(df_age_melt, x='Age', y='Count', color='User_Type',
                 title='Liczba użytkowników narkotyków według wieku',
                 barmode='group')
    
    # Konwersja wykresu do JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('visualize.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)