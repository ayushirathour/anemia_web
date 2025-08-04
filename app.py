import joblib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

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
    # This renders the index.html page if someone visits the site directly
    return render_template("index.html", prediction=prediction)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        hemoglobin = float(data["Hemoglobin"])
        mch = float(data["Mean_Corpuscular_Hemoglobin"])
        mchc = float(data["Mean_Corpuscular_Hemoglobin_Concentration"])
        mcv = float(data["Mean_Corpuscular_Volume"])
        input_data = [[hemoglobin, mch, mchc, mcv]]
        pred = model.predict(input_data)
        prediction = "Anemia" if pred[0] == 1 else "Healthy"
        return jsonify({"prediction": prediction})
    except Exception:
        return jsonify({"prediction": "Invalid input."})

if __name__ == "__main__":
    app.run(debug=True)
