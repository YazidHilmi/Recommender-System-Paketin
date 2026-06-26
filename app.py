from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

preprocessor = joblib.load('preprocessor_trans.joblib')
model = joblib.load('model_trans.joblib')
encoder_label = joblib.load('encoder_label_trans.joblib')


@app.route('/', methods=['GET'])
def home():
    """Halaman Utama API"""
    return "<h1>API Prediksi Model Berjalan! Kirim POST ke /predict</h1>"


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint untuk melakukan prediksi"""
    try:
        
        data = request.json
        
        all_cols = [
            "plan_type", "device_brand",
            "avg_data_usage_gb", "pct_video_usage", "avg_call_duration",
            "sms_freq", "monthly_spend", "topup_freq", 
            "travel_score", "complaint_count"
        ]
        
        input_df = pd.DataFrame([data], columns=all_cols)
        fitur_final = preprocessor.transform(input_df)
        pred = model.predict(fitur_final)[0]
        label_pred = encoder_label.inverse_transform([pred])[0]

        return jsonify({
            "prediction_value": int(pred),
            "label_prediction": label_pred
        })

    except Exception as e:
        return jsonify({"error": str(e), "message": "Terjadi kesalahan saat memproses data."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)