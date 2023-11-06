import pickle
from flask import Flask, render_template, request
from sklearn.preprocessing import normalize
import pandas as pd
app = Flask(__name__)

with open('train_data.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    uploaded_file = request.files['excel_file']
    excel_data = pd.read_excel(uploaded_file) 

    input_features = excel_data.iloc[:, 0:178].values.flatten().tolist()

    normalized_features = normalize([input_features])
    prediction = model.predict(normalized_features)
    result = "Seizure Detected" if prediction[0] == 1 else "No Seizure Detected"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
