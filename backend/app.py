from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("model/loan_model.pkl")


@app.route("/")
def home():
    return "Loan Prediction API Running"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        features = np.array([[
            data["Gender"],
            data["Married"],
            data["Dependents"],
            data["Education"],
            data["Self_Employed"],
            data["ApplicantIncome"],
            data["CoapplicantIncome"],
            data["LoanAmount"],
            data["Loan_Amount_Term"],
            data["Credit_History"],
            data["Property_Area"]
        ]])

        prediction = model.predict(features)

        result = "Approved" if prediction[0] == 1 else "Rejected"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)