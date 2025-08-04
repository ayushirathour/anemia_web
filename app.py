import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# Model load karo
model = joblib.load("disease_model (1).joblib")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            # Form se values lo (example biomarkers)
            hemoglobin = float(request.form["hemoglobin"])
            mch = float(request.form["mch"])
            mchc = float(request.form["mchc"])
            mcv = float(request.form["mcv"])

            # Predict
            data = [[hemoglobin, mch, mchc, mcv]]
            pred = model.predict(data)

            prediction = "Anemia" if pred[0] == 1 else "Healthy"
        except:
            prediction = "Invalid input. Please enter correct numbers."

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
