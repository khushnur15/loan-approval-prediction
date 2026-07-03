import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load dataset
df = pd.read_csv("../data/train.csv")

# Remove Loan_ID column
df.drop("Loan_ID", axis=1, inplace=True)

# Fill missing categorical values with mode
categorical_cols = ["Gender", "Married", "Dependents", "Self_Employed"]

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Fill missing numerical values with median
numerical_cols = ["LoanAmount", "Loan_Amount_Term", "Credit_History"]

for col in numerical_cols:
    df[col] = df[col].fillna(df[col].median())

# Convert text columns into numbers
encoder = LabelEncoder()

for col in df.select_dtypes(include="object").columns:
    df[col] = encoder.fit_transform(df[col])

# Separate features and target
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save trained model
joblib.dump(model, "loan_model.pkl")

print("\nModel saved successfully!")