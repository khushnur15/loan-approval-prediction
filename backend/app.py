from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import os

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

app.secret_key = "loan_prediction_secret_key"

CORS(app, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Load ML model
model = joblib.load("model/loan_model.pkl")


# ---------------- DATABASE ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))


with app.app_context():
    db.create_all()


# ---------------- FRONTEND ROUTES ---------------- #

@app.route("/")
def home():
    return app.send_static_file("login.html")


@app.route("/register")
def register_page():
    return app.send_static_file("register.html")


@app.route("/dashboard")
def dashboard():
    return app.send_static_file("index.html")

@app.route("/result")
def result_page():
    return app.send_static_file("result.html")


# ---------------- AUTH ---------------- #

@app.route("/api/register", methods=["POST"])
def register():

    data = request.json

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "message": "User already exists"
        })

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(
            data["password"]
        )
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Registration Successful"
    })


@app.route("/api/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if user and check_password_hash(
        user.password,
        data["password"]
    ):

        session["user"] = user.email

        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Credentials"
    })


@app.route("/api/logout")
def logout():

    session.pop("user", None)

    return jsonify({
        "message": "Logged Out"
    })


# ---------------- PREDICTION ---------------- #

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return jsonify({
            "message": "Please login first"
        }), 401

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

        confidence = 80

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(features)
            confidence = round(
                max(probability[0]) * 100,
                2
            )

        result = (
            "Approved"
            if prediction[0] == 1
            else "Rejected"
        )

        reasons = []

        if data["Credit_History"] == 1:
            reasons.append(
                "Strong credit history improved approval probability."
            )
        else:
            reasons.append(
                "Limited credit history increased financial risk."
            )

        total_income = (
            data["ApplicantIncome"] +
            data["CoapplicantIncome"]
        )

        if total_income >= 5000:
            reasons.append(
                "Combined household income supports the requested loan."
            )
        else:
            reasons.append(
                "Income level may not fully support repayment obligations."
            )

        if data["LoanAmount"] <= 200:
            reasons.append(
                "Requested loan amount is within acceptable limits."
            )
        else:
            reasons.append(
                "Loan amount is relatively high compared to similar applications."
            )

        if data["Education"] == 1:
            reasons.append(
                "Graduate profile aligned with historically approved applications."
            )

        if data["Property_Area"] == 2:
            reasons.append(
                "Urban property applications often demonstrate strong repayment trends."
            )

        risk = (
            "Low Risk"
            if result == "Approved"
            else "High Risk"
        )

        return jsonify({
            "prediction": result,
            "confidence": confidence,
            "risk": risk,
            "reasons": reasons
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })
    
    print("Starting Flask Server...")

if __name__ == "__main__":
    app.run(debug=True)

