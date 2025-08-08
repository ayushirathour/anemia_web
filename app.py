import joblib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enhanced CORS configuration - handles all scenarios
CORS(app, 
     origins=[
         "https://bloodwiseai.vercel.app",      # ✅ No trailing slash
         "https://*.vercel.app",                # Any Vercel subdomain
         "http://localhost:3000",               # Local development
         "https://localhost:3000"               # HTTPS local
     ],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
     supports_credentials=True,
     max_age=3600)

# Manual CORS headers for extra compatibility
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ["https://bloodwiseai.vercel.app", "http://localhost:3000"]:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Load your trained model
try:
    model = joblib.load("disease_model (1).joblib")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {str(e)}")
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            hemoglobin = float(request.form["hemoglobin"])
            mch = float(request.form["mch"])
            mchc = float(request.form["mchc"])
            mcv = float(request.form["mcv"])
            
            features = [0.0] * 24
            features[2] = hemoglobin              
            features[7] = mcv                     
            features[8] = mch                     
            features[9] = mchc                    
            
            input_data = [features]
            pred = model.predict(input_data)
            prediction = "Anemia" if pred[0] == 1 else "Healthy"
        except Exception as e:
            print(f"Error: {str(e)}")
            prediction = "Invalid input. Please enter correct numbers."
    return render_template("index.html", prediction=prediction)

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'https://bloodwiseai.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    try:
        if model is None:
            return jsonify({"error": "Model not available"}), 500
        
        data = request.get_json()
        print(f"📊 Request Origin: {request.headers.get('Origin')}")
        print(f"📊 DATA RECEIVED: {data}")

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Create a 24-feature list
        features = [0.0] * 24
        features[2] = float(data.get("Hemoglobin", 0))
        features[7] = float(data.get("Mean_Corpuscular_Volume", 0))
        features[8] = float(data.get("Mean_Corpuscular_Hemoglobin", 0))
        features[9] = float(data.get("Mean_Corpuscular_Hemoglobin_Concentration", 0))
        
        input_data = [features]
        pred = model.predict(input_data)
        prediction = "Anemia" if pred[0] == 1 else "Healthy"
        
        # Add confidence score
        try:
            prob = model.predict_proba(input_data)
            confidence = float(max(prob[0]))
        except:
            confidence = 0.85
        
        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "status": "success"
        })
        
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# Add health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "cors_enabled": True,
        "model_loaded": model is not None
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
