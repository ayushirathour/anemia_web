@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data)  # DEBUG print to Render logs
        
        hemoglobin = float(data["Hemoglobin"])
        mch = float(data["Mean_Corpuscular_Hemoglobin"])
        mchc = float(data["Mean_Corpuscular_Hemoglobin_Concentration"])
        mcv = float(data["Mean_Corpuscular_Volume"])
        input_data = [[hemoglobin, mch, mchc, mcv]]
        pred = model.predict(input_data)
        prediction = "Anemia" if pred[0] == 1 else "Healthy"
        return jsonify({"prediction": prediction})
    except Exception as e:
        print("ERROR:", str(e))  # DEBUG print to Render logs
        return jsonify({"prediction": "Invalid input."})
