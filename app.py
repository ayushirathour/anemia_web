import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# Load your model
model = joblib.load("disease_model (1).joblib")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Get values from frontend JSON
        hemoglobin = float(data.get("Hemoglobin", 0))
        mch = float(data.get("Mean_Corpuscular_Hemoglobin", 0))
        mchc = float(data.get("Mean_Corpuscular_Hemoglobin_Concentration", 0))
        mcv = float(data.get("Mean_Corpuscular_Volume", 0))

        # Prepare input for model
        features = [[hemoglobin, mch, mchc, mcv]]

        # Predict
        pred = model.predict(features)

        # Map prediction
        prediction_label = "Anemia" if pred[0] == 1 else "Healthy"

        return jsonify({"prediction": prediction_label})

    except Exception as e:
        return jsonify({"error": str(e)})

# Optional home route for testing
@app.route("/")
def home():
    return "Anemia Prediction API is running!"

if __name__ == "__main__":
    app.run(debug=True)
