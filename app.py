import joblib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://anemiafastscan.netlify.app/"])  # Only allow your frontend

# Load your trained model
model = joblib.load("disease_model (1).joblib")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            hemoglobin = float(request.form["hemoglobin"])
            mch = float(request.form["mch"])
            mchc = float(request.form["mchc"])
            mcv = float(request.form["mcv"])
            # This part is only for local/form use, not Netlify
            features = [0.0] * 24
            features[2] = hemoglobin              # Hemoglobin
            features[7] = mcv                     # Mean Corpuscular Volume
            features[8] = mch                     # Mean Corpuscular Hemoglobin
            features[9] = mchc                    # Mean Corpuscular Hemoglobin Concentration
            input_data = [features]
            pred = model.predict(input_data)
            prediction = "Anemia" if pred[0] == 1 else "Healthy"
        except Exception:
            prediction = "Invalid input. Please enter correct numbers."
    return render_template("index.html", prediction=prediction)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data)  # For debugging/logging

        # Create a 24-feature list, default to 0.0
        features = [0.0] * 24
        features[2] = float(data.get("Hemoglobin", 0))
        features[7] = float(data.get("Mean_Corpuscular_Volume", 0))
        features[8] = float(data.get("Mean_Corpuscular_Hemoglobin", 0))
        features[9] = float(data.get("Mean_Corpuscular_Hemoglobin_Concentration", 0))
        
        input_data = [features]
        pred = model.predict(input_data)
        prediction = "Anemia" if pred[0] == 1 else "Healthy"
        return jsonify({"prediction": prediction})
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"prediction": "Invalid input."})

if __name__ == "__main__":
    app.run(debug=True)

