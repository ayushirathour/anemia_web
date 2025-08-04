import joblib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow API calls from your frontend

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
            data = [[hemoglobin, mch, mchc, mcv]]
            pred = model.predict(data)
            prediction = "Anemia" if pred[0] == 1 else "Healthy"
        except Exception:
            prediction = "Invalid input. Please enter correct numbers."
    return render_template("index.html", prediction=prediction)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data)  # For debugging
        hemoglobin = float(data["Hemoglobin"])
        mch = float(data["Mean_Corpuscular_Hemoglobin"])
        mchc = float(data["Mean_Corpuscular_Hemoglobin_Concentration"])
        mcv = float(data["Mean_Corpuscular_Volume"])
        input_data = [[hemoglobin, mch, mchc, mcv]]
        pred = model.predict(input_data)
        prediction = "Anemia" if pred[0] == 1 else "Healthy"
        return jsonify({"prediction": prediction})
    except Exception as e:
        print("ERROR:", str(e))  # For debugging
        return jsonify({"prediction": "Invalid input."})

if __name__ == "__main__":
    app.run(debug=True)
